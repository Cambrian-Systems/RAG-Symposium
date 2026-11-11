"""Turn your own AI-agent session history into documents you can search.

Reads the session files that coding agents keep on this computer (Claude Code,
Codex, OpenCode, Gemini CLI) and any web-chatbot data export you name
(ChatGPT or Claude.ai), writes one corpus-format Markdown document per session
to sessions/docs/, and publishes them with the same ingestion code as the
workshop corpus. No model is involved, nothing leaves the computer, and the
original session files are only read, never changed.

Two modes show why chunking matters:
- summary (the default): one short page per session built from its messages.
  The full transcript is kept next to it in a transcripts/ folder that search
  does not read, and the summary names that file.
- raw: every message, tool call and tool output, all searched. Long and noisy.

Likely secrets (API keys, tokens, private keys, card numbers) are replaced with
[REDACTED] before anything is written.
"""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .ingest import ingest

# Each source: the name used with --tools, and the issuer shown on its documents.
TOOLS = {"claude": "Claude Code", "codex": "Codex", "opencode": "OpenCode",
         "gemini": "Gemini CLI", "chatgpt": "ChatGPT", "claude-ai": "Claude.ai"}

PAGE_SIZE = 3000          # Characters per <!-- page N --> section, roughly.
TITLE_LENGTH = 80
CALL_LENGTH = 300         # A tool call is one line, cut to this many characters.
SUMMARY_FIRST = 600       # Summary mode: the first message, the final reply,
SUMMARY_OTHER = 160       # and up to SUMMARY_OTHER_COUNT other messages, each cut.
SUMMARY_OTHER_COUNT = 12
NEXT_QUERY = "what went wrong during setup?"

# Input fields that best describe a tool call in one line, in order of preference.
CALL_FIELDS = ("command", "cmd", "code", "query", "pattern", "file_path", "filePath",
               "path", "url", "prompt", "description")


# --- Redaction ---------------------------------------------------------------

# Applied in this order. Each pattern's replacement keeps any label in front of
# the secret ("Bearer ", "password = ") so the text still reads naturally.
SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?(?:-----END [A-Z ]*PRIVATE KEY-----|\Z)", re.S),
     "[REDACTED]"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"), "[REDACTED]"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), "[REDACTED]"),
    (re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"), "[REDACTED]"),
    (re.compile(r"\b(Bearer\s+)[A-Za-z0-9._~+/=-]{16,}", re.I), r"\1[REDACTED]"),
]
# A name ending in password/secret/token/api key, then = or :, then a value.
# "max_tokens: 4000" does not match: the name must end in the keyword.
ASSIGNMENT = re.compile(
    r"\b([\w.-]*(?:password|passwd|secret|token|api[_-]?key))([\"']?\s*[:=]\s*[\"']?)"
    r"(?![\[$<{(*%])([^\s\"'`,;]{3,})", re.I)
PLACEHOLDER_VALUES = {"none", "null", "true", "false", "str", "string", "undefined", "required"}
# 13-19 digits, optionally grouped with spaces or dashes, as card numbers are.
# Cards start with 2-6; numbers starting 0 or 1 (padded IDs, epoch timestamps)
# and 14-digit dates such as 20261110093000 are left alone.
CARD_NUMBER = re.compile(r"(?<![\w-])[2-6](?:[ -]?\d){12,18}(?![\w-])")
DATE_STAMP = re.compile(r"20\d{12}")


def luhn_valid(digits: str) -> bool:
    """The checksum every payment card number passes; random numbers pass 1 in 10."""
    total = 0
    for position, digit in enumerate(reversed(digits)):
        value = int(digit) * (2 if position % 2 else 1)
        total += value - 9 if value > 9 else value
    return total % 10 == 0


def scrub(text: str) -> tuple[str, int]:
    """Replace likely secrets with [REDACTED]; return the text and how many were replaced."""
    count = 0
    for pattern, replacement in SECRET_PATTERNS:
        text, replaced = pattern.subn(replacement, text)
        count += replaced

    def assignment(match):
        nonlocal count
        if match.group(3).lower() in PLACEHOLDER_VALUES:
            return match.group(0)
        count += 1
        return match.group(1) + match.group(2) + "[REDACTED]"

    def card(match):
        nonlocal count
        digits = re.sub(r"\D", "", match.group(0))
        if 13 <= len(digits) <= 19 and luhn_valid(digits) and not DATE_STAMP.fullmatch(digits):
            count += 1
            return "[REDACTED]"
        return match.group(0)

    text = ASSIGNMENT.sub(assignment, text)
    text = CARD_NUMBER.sub(card, text)
    return text, count


# --- Small helpers shared by the readers --------------------------------------

def parse_time(value) -> datetime | None:
    """Read an ISO timestamp or epoch seconds/milliseconds as a UTC datetime."""
    try:
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            # Anything this large is milliseconds; seconds pass it in the year 5138.
            return datetime.fromtimestamp(value / 1000 if value > 1e11 else value, timezone.utc)
        if isinstance(value, str) and value:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return (parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)
    except (ValueError, OverflowError, OSError):
        pass
    return None


def injected(text: str) -> bool:
    """True for text an agent adds to the user's side itself, not typed by the person.

    Agents wrap such text in a tag (<environment_context>, <system-reminder>,
    <command-name>) or paste project instructions ("# AGENTS.md instructions").
    """
    stripped = text.strip()
    return (stripped.startswith("<") and stripped.endswith(">")) or stripped.startswith("# AGENTS.md")


def call_line(name: str, arguments) -> str:
    """Describe one tool call on one line: "[tool: shell] uv sync --locked"."""
    if isinstance(arguments, str):
        try:
            arguments = json.loads(arguments)
        except ValueError:
            pass
    summary = arguments
    if isinstance(arguments, dict):
        field = next((f for f in CALL_FIELDS if arguments.get(f)), None)
        summary = arguments[field] if field else (json.dumps(arguments, ensure_ascii=False, sort_keys=True)
                                                  if arguments else "")
    if isinstance(summary, list):
        summary = " ".join(str(item) for item in summary)
    return f"[tool: {name or 'unknown'}] {trim(str(summary or ''), CALL_LENGTH)}".rstrip()


def trim(text: str, limit: int) -> str:
    """Collapse whitespace and cut at a word boundary, marking the cut with "..."."""
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text.rfind(" ", limit // 2, limit)
    return text[:cut if cut > 0 else limit].rstrip() + "..."


def block_text(content) -> str:
    """Text from a string or a list of content blocks; images become "[image]"."""
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        content = [content]
    pieces = []
    for block in content if isinstance(content, list) else []:
        if isinstance(block, str):
            pieces.append(block)
        elif isinstance(block, dict):
            if isinstance(block.get("text"), str):
                pieces.append(block["text"])
            elif "image" in str(block.get("type", "")):
                pieces.append("[image]")
            elif isinstance(block.get("content"), (str, list)):
                pieces.append(block_text(block["content"]))
    return "\n".join(piece for piece in pieces if piece)


def session(tool: str, key: str, source_url: str, entries: list, times: list) -> dict | None:
    """Package one parsed session; None if it has nothing a person said or read.

    entries are (kind, text) pairs: kind is "you", "agent", "call" or "output".
    """
    entries = [(kind, text.strip()) for kind, text in entries if isinstance(text, str) and text.strip()]
    times = sorted(t for t in times if t)
    if not any(kind in ("you", "agent") for kind, _ in entries) or not times:
        return None
    return {"tool": tool, "key": key, "source_url": source_url, "entries": entries,
            "started": times[0], "updated": times[-1]}


def read_jsonl(path: Path):
    """Yield each JSON object in a JSONL file, skipping lines that are not JSON."""
    with path.open(encoding="utf-8", errors="replace") as stream:
        for line in stream:
            try:
                item = json.loads(line)
            except ValueError:
                continue
            if isinstance(item, dict):
                yield item


# --- Local agents -------------------------------------------------------------

def claude_code_session(path: Path) -> dict | None:
    """One Claude Code session file: a JSONL line per message or event."""
    entries, times, key = [], [], path.stem
    for item in read_jsonl(path):
        if item.get("type") not in ("user", "assistant") or item.get("isSidechain") or item.get("isMeta"):
            continue
        key = item.get("sessionId") or key
        times.append(parse_time(item.get("timestamp")))
        content = (item.get("message") or {}).get("content")
        if isinstance(content, str):
            content = [{"type": "text", "text": content}]
        for block in content if isinstance(content, list) else []:
            kind = block.get("type") if isinstance(block, dict) else None
            if kind == "text" and not (item["type"] == "user" and injected(block.get("text", ""))):
                entries.append(("you" if item["type"] == "user" else "agent", block.get("text")))
            elif kind == "tool_use":
                entries.append(("call", call_line(block.get("name"), block.get("input"))))
            elif kind == "tool_result":
                entries.append(("output", block_text(block.get("content"))))
    return session("claude", key, path.resolve().as_uri(), entries, times)


def codex_session(path: Path) -> dict | None:
    """One Codex rollout file: a JSONL line per item, the item under "payload"."""
    entries, times, key = [], [], path.stem
    for line in read_jsonl(path):
        # Older Codex versions wrote items directly instead of under "payload".
        item = line.get("payload") if isinstance(line.get("payload"), dict) else line
        kind = item.get("type") or line.get("type")
        if line.get("type") == "session_meta":
            # Sub-agent sessions are left out: the parent session shows the call
            # that started them.
            if isinstance(item.get("source"), dict) and "subagent" in item["source"]:
                return None
            key = item.get("id") or key
        times.append(parse_time(line.get("timestamp")))
        if kind == "message" and item.get("role") in ("user", "assistant"):
            for block in item.get("content") or []:
                text = block.get("text") if isinstance(block, dict) else None
                if not isinstance(text, str) or (item["role"] == "user" and injected(text)):
                    continue
                entries.append(("you" if item["role"] == "user" else "agent", text))
        elif kind == "function_call":
            entries.append(("call", call_line(item.get("name"), item.get("arguments"))))
        elif kind == "custom_tool_call":
            entries.append(("call", call_line(item.get("name"), item.get("input"))))
        elif kind in ("function_call_output", "custom_tool_call_output"):
            entries.append(("output", block_text(item.get("output"))))
    return session("codex", key, path.resolve().as_uri(), entries, times)


def gemini_session(path: Path) -> dict | None:
    """One Gemini CLI chat file: a JSON object with a "messages" list."""
    data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    if not isinstance(data, dict) or not isinstance(data.get("messages"), list):
        return None
    entries, times = [], [parse_time(data.get("startTime")), parse_time(data.get("lastUpdated"))]
    for message in data["messages"]:
        if not isinstance(message, dict):
            continue
        times.append(parse_time(message.get("timestamp")))
        if message.get("type") == "user":
            entries.append(("you", block_text(message.get("content"))))
        elif message.get("type") == "gemini":
            entries.append(("agent", block_text(message.get("content"))))
            for call in message.get("toolCalls") or []:
                entries.append(("call", call_line(call.get("name"), call.get("args"))))
                entries.append(("output", gemini_result(call)))
    return session("gemini", data.get("sessionId") or path.stem, path.resolve().as_uri(), entries, times)


def gemini_result(call: dict) -> str:
    """A Gemini tool result: functionResponse parts, or the text shown on screen."""
    pieces = []
    for part in call.get("result") or []:
        response = part.get("functionResponse", {}).get("response") if isinstance(part, dict) else None
        if isinstance(response, dict):
            value = response.get("output", response.get("error", response))
            pieces.append(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False))
        elif isinstance(part, dict) and isinstance(part.get("text"), str):
            pieces.append(part["text"])
    if not pieces and isinstance(call.get("resultDisplay"), str):
        pieces.append(call["resultDisplay"])
    return "\n".join(pieces)


def opencode_part_entries(part: dict, role: str) -> list:
    """Entries for one OpenCode message part (database v1 and storage/ JSON)."""
    kind = part.get("type")
    if kind == "text" and not part.get("synthetic"):
        return [("you" if role == "user" else "agent", part.get("text"))]
    if kind == "tool":
        state = part.get("state") or {}
        output = state.get("output") if state.get("output") is not None else state.get("error")
        return [("call", call_line(part.get("tool"), state.get("input"))),
                ("output", output if isinstance(output, str) else block_text(output) or json.dumps(output))]
    return []


def opencode_db_sessions(db: Path) -> list:
    """Sessions from opencode.db, opened read-only. Two table layouts are known:

    - session_v2 + session_message: each message's data holds its text, or for
      the agent a "content" list of text, reasoning and tool blocks.
    - session + message + part: each message's text and tool calls are rows in part.
    """
    found = []
    connection = sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if {"session_v2", "session_message"} <= tables:
            rows = connection.execute("SELECT id, time_created, time_updated FROM session_v2 "
                                      "WHERE parent_id IS NULL ORDER BY id").fetchall()
            for session_id, created, updated in rows:
                entries, times = [], [parse_time(created), parse_time(updated)]
                for kind, data in connection.execute(
                        "SELECT type, data FROM session_message WHERE session_id = ? ORDER BY seq",
                        (session_id,)):
                    data = json.loads(data)
                    if kind == "user":
                        entries.append(("you", data.get("text")))
                    elif kind == "assistant":
                        for block in data.get("content") or []:
                            if block.get("type") == "text":
                                entries.append(("agent", block.get("text")))
                            elif block.get("type") == "tool":
                                state = block.get("state") or {}
                                entries.append(("call", call_line(block.get("name"), state.get("input"))))
                                output = state.get("content") or state.get("error") or ""
                                entries.append(("output", output if isinstance(output, str)
                                                else block_text(output) or json.dumps(output)))
                found.append(session("opencode", session_id, f"{db.resolve().as_uri()}#{session_id}",
                                     entries, times))
        if {"session", "message", "part"} <= tables:
            rows = connection.execute("SELECT id, time_created, time_updated FROM session "
                                      "WHERE parent_id IS NULL ORDER BY id").fetchall()
            for session_id, created, updated in rows:
                entries, times = [], [parse_time(created), parse_time(updated)]
                messages = connection.execute(
                    "SELECT id, data FROM message WHERE session_id = ? ORDER BY time_created, id",
                    (session_id,)).fetchall()
                for message_id, data in messages:
                    role = json.loads(data).get("role")
                    for (part,) in connection.execute(
                            "SELECT data FROM part WHERE message_id = ? ORDER BY time_created, id", (message_id,)):
                        entries.extend(opencode_part_entries(json.loads(part), role))
                found.append(session("opencode", session_id, f"{db.resolve().as_uri()}#{session_id}",
                                     entries, times))
    finally:
        connection.close()
    return found


def opencode_storage_sessions(storage: Path) -> list:
    """Sessions from older OpenCode's storage/ folder of small JSON files:
    session/<project>/<session>.json, message/<session>/<message>.json and
    part/<message>/<part>.json."""
    found = []
    for info_path in sorted(storage.glob("session/*/*.json")):
        info = json.loads(info_path.read_text(encoding="utf-8", errors="replace"))
        if not isinstance(info, dict) or info.get("parentID"):
            continue
        session_id = info.get("id") or info_path.stem
        times = [parse_time((info.get("time") or {}).get("created")),
                 parse_time((info.get("time") or {}).get("updated"))]
        messages = [json.loads(p.read_text(encoding="utf-8", errors="replace"))
                    for p in storage.glob(f"message/{session_id}/*.json")]
        messages.sort(key=lambda m: ((m.get("time") or {}).get("created") or 0, m.get("id", "")))
        entries = []
        for message in messages:
            parts = sorted((json.loads(p.read_text(encoding="utf-8", errors="replace"))
                            for p in storage.glob(f"part/{message.get('id')}/*.json")),
                           key=lambda part: part.get("id", ""))
            for part in parts:
                entries.extend(opencode_part_entries(part, message.get("role")))
        found.append(session("opencode", session_id, info_path.resolve().as_uri(), entries, times))
    return found


def local_sources(home: Path) -> dict:
    """Where each local agent keeps its sessions, honouring the same settings it does."""
    environ = os.environ
    claude = Path(environ["CLAUDE_CONFIG_DIR"]) if environ.get("CLAUDE_CONFIG_DIR") else home / ".claude"
    codex = Path(environ["CODEX_HOME"]) if environ.get("CODEX_HOME") else home / ".codex"
    data = Path(environ["XDG_DATA_HOME"]) if environ.get("XDG_DATA_HOME") else home / ".local" / "share"
    return {"claude": claude / "projects", "codex": codex / "sessions",
            "opencode": data / "opencode", "gemini": home / ".gemini" / "tmp"}


def local_sessions(tool: str, folder: Path, cutoff: datetime | None, problems: list) -> list:
    """Read one local agent's sessions. A file that cannot be read is noted and skipped."""
    if tool == "opencode":
        readers = []
        if (folder / "opencode.db").is_file():
            readers.append((folder / "opencode.db", opencode_db_sessions))
        if (folder / "storage" / "session").is_dir():
            readers.append((folder / "storage", opencode_storage_sessions))
        found = {}
        for path, reader in readers:
            try:
                for item in reader(path):
                    # A database and a storage/ folder can hold the same session.
                    if item and item["key"] not in found:
                        found[item["key"]] = item
            except (OSError, ValueError, KeyError, AttributeError, TypeError, sqlite3.Error) as exc:
                problems.append(f"{path}: {exc.__class__.__name__}")
        return list(found.values())
    pattern, reader = {"claude": ("*/*.jsonl", claude_code_session),
                       "codex": ("**/*.jsonl", codex_session),
                       "gemini": ("*/chats/*.json", gemini_session)}[tool]
    found = []
    for path in sorted(folder.glob(pattern)):
        try:
            # A file not changed since the cutoff cannot hold newer messages,
            # so --since skips it unread.
            if cutoff and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) < cutoff:
                continue
            item = reader(path)
        except (OSError, ValueError, KeyError, AttributeError, TypeError) as exc:
            problems.append(f"{path}: {exc.__class__.__name__}")
            continue
        if item:
            found.append(item)
    return found


# --- Web chatbot exports ------------------------------------------------------

def chatgpt_session(conversation: dict, source_url: str) -> dict | None:
    """One ChatGPT conversation: a "mapping" tree of message nodes.

    Editing or regenerating a message starts a new branch. current_node is the
    last message of the branch shown on screen; following parent links back to
    the root gives that branch, which is then read from the start.
    """
    mapping = conversation.get("mapping") or {}
    node_id, branch, visited = conversation.get("current_node"), [], set()
    if node_id not in mapping:
        # No current_node: take the newest child at each step from the root.
        node_id = next((k for k, v in mapping.items() if not v.get("parent")), None)
        while node_id in mapping and mapping[node_id].get("children"):
            node_id = mapping[node_id]["children"][-1]
    while node_id in mapping and node_id not in visited:
        visited.add(node_id)
        branch.append(mapping[node_id])
        node_id = mapping[node_id].get("parent")
    entries = []
    times = [parse_time(conversation.get("create_time")), parse_time(conversation.get("update_time"))]
    for node in reversed(branch):
        message = node.get("message") or {}
        content = message.get("content") or {}
        role = (message.get("author") or {}).get("role")
        if (message.get("metadata") or {}).get("is_visually_hidden_from_conversation"):
            continue
        times.append(parse_time(message.get("create_time")))
        text = "\n".join(p for p in content.get("parts") or [] if isinstance(p, str))
        text = text or content.get("text") or content.get("result") or ""
        if content.get("content_type") in ("thoughts", "reasoning_recap", "user_editable_context"):
            continue
        if role == "user":
            entries.append(("you", text))
        elif role == "assistant" and message.get("recipient", "all") != "all":
            entries.append(("call", call_line(message["recipient"], text)))
        elif role == "assistant":
            entries.append(("agent", text))
        elif role == "tool":
            entries.append(("output", text))
    key = conversation.get("conversation_id") or conversation.get("id") or ""
    return session("chatgpt", key, f"{source_url}#{key}", entries, times)


def claude_ai_session(conversation: dict, source_url: str) -> dict | None:
    """One Claude.ai conversation: a flat "chat_messages" list.

    Each message's "content" blocks hold the text and any tool calls. Its "text"
    field repeats the words but puts a placeholder where a tool ran, so it is
    only used when a message has no content blocks.
    """
    entries = []
    times = [parse_time(conversation.get("created_at")), parse_time(conversation.get("updated_at"))]
    for message in conversation.get("chat_messages") or []:
        speaker = "you" if message.get("sender") == "human" else "agent"
        times.append(parse_time(message.get("created_at")))
        blocks = message.get("content") or [{"type": "text", "text": message.get("text", "")}]
        for block in blocks:
            if block.get("type") == "text":
                entries.append((speaker, block.get("text")))
            elif block.get("type") == "tool_use":
                entries.append(("call", call_line(block.get("name"), block.get("input"))))
            elif block.get("type") == "tool_result":
                entries.append(("output", block_text(block.get("content"))))
    key = conversation.get("uuid") or ""
    return session("claude-ai", key, f"{source_url}#{key}", entries, times)


def export_sessions(path: Path) -> list:
    """Sessions from a ChatGPT or Claude.ai export: the .zip itself or its conversations.json.

    Both put a list of conversations in conversations.json; the fields of a
    conversation say which service it came from.
    """
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            names = sorted(n for n in archive.namelist() if re.fullmatch(r"conversations[\w-]*\.json",
                           n.rsplit("/", 1)[-1]) and not n.startswith("__MACOSX"))
            lists = [json.loads(archive.read(name).decode("utf-8", errors="replace")) for name in names]
    else:
        lists = [json.loads(path.read_text(encoding="utf-8", errors="replace"))]
    source_url = path.resolve().as_uri()
    found = []
    for conversations in lists:
        for conversation in conversations if isinstance(conversations, list) else []:
            if isinstance(conversation, dict) and "mapping" in conversation:
                found.append(chatgpt_session(conversation, source_url))
            elif isinstance(conversation, dict) and "chat_messages" in conversation:
                found.append(claude_ai_session(conversation, source_url))
    return [item for item in found if item]


# --- Writing documents --------------------------------------------------------

def split_long(paragraph: str, size: int) -> list[str]:
    """Cut a paragraph longer than size at line breaks or spaces."""
    pieces = []
    while len(paragraph) > size:
        cut = max(paragraph.rfind("\n", size // 2, size), paragraph.rfind(" ", size // 2, size))
        cut = cut if cut > 0 else size
        pieces.append(paragraph[:cut].rstrip())
        paragraph = paragraph[cut:].lstrip()
    return pieces + [paragraph]


def paginate(paragraphs: list[str], size: int = PAGE_SIZE) -> list[str]:
    """Group paragraphs into pages of about size characters, breaking between paragraphs."""
    pages, current = [], ""
    for paragraph in paragraphs:
        for piece in split_long(paragraph, size):
            if current and len(current) + len(piece) + 2 > size:
                pages.append(current)
                current = ""
            current = f"{current}\n\n{piece}" if current else piece
    return pages + [current] if current else pages


LABELS = {"you": "You: ", "agent": "Agent: ", "call": "", "output": "Tool output: "}


def raw_pages(item: dict) -> list[str]:
    """Every entry in order: "You:" and "Agent:" paragraphs, tool calls, tool output."""
    return paginate([LABELS[kind] + text for kind, text in item["entries"]])


def summary_pages(item: dict, title: str, date: str, transcript: str | None = None) -> list[str]:
    """One short page: what was asked, what else was said, how it ended, and where the full transcript is."""
    yours = [text for kind, text in item["entries"] if kind == "you"]
    replies = [text for kind, text in item["entries"] if kind == "agent"]
    lines = [f"Session: {title}", f"Tool: {TOOLS[item['tool']]}", f"Date: {date}",
             f"Turns: {len(yours)}"]
    if transcript:
        lines.append(f"Full transcript: {transcript}")
    lines.append("")
    if yours:
        lines += [f"You first asked: {trim(yours[0], SUMMARY_FIRST)}", ""]
    if len(yours) > 1:
        lines.append("You also said:")
        lines += [f"- {trim(text, SUMMARY_OTHER)}" for text in yours[1:1 + SUMMARY_OTHER_COUNT]]
        if len(yours) - 1 > SUMMARY_OTHER_COUNT:
            lines.append(f"- (and {len(yours) - 1 - SUMMARY_OTHER_COUNT} more messages)")
        lines.append("")
    if replies:
        lines.append(f"The agent's final message: {trim(replies[-1], SUMMARY_FIRST)}")
    return ["\n".join(lines).strip()]


def document_id(item: dict, date: str, taken: set) -> str:
    """SESSION-<TOOL>-<date>-<6 hex characters>, the same on every run for the same session."""
    digest = hashlib.sha1(f"{item['tool']}:{item['key']}:{item['source_url']}".encode()).hexdigest()
    prefix = f"SESSION-{item['tool'].upper().replace('-', '')}-{date}-"
    for length in (6, 10, 40):
        candidate = prefix + digest[:length]
        if candidate not in taken:
            taken.add(candidate)
            return candidate
    raise ValueError(f"Two sessions share the ID {candidate}")


def render(item: dict, mode: str, taken: set, transcript: str | None = None) -> tuple[str, str, int]:
    """Return (document ID, corpus-format Markdown, redactions made) for one session.

    transcript is the path a summary names as its full transcript.
    """
    redactions, entries = 0, []
    for kind, text in item["entries"]:
        text, count = scrub(text)
        redactions += count
        # Text that looks like a page marker would split the document in the
        # wrong place, so it is changed before writing.
        entries.append((kind, text.replace("<!-- page", "<!-- quoted page")))
    item = {**item, "entries": entries}
    date = item["started"].strftime("%Y-%m-%d")
    first = next((text for kind, text in entries if kind == "you"), "")
    title = trim(first, TITLE_LENGTH) or f"{TOOLS[item['tool']]} session {date}"
    doc_id = document_id(item, date, taken)
    pages = summary_pages(item, title, date, transcript) if mode == "summary" else raw_pages(item)
    header = {"id": doc_id, "title": title, "issuer": TOOLS[item["tool"]], "published": date,
              "status": "session", "source_url": item["source_url"]}
    body = "\n\n".join(f"<!-- page {n} -->\n{text}" for n, text in enumerate(pages, 1))
    content = ("---\n" + "".join(f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k, v in header.items())
               + "---\n\n" + body + "\n")
    return doc_id, content, redactions


def build(home: Path, out: Path, output: Path, mode: str = "summary", since: float | None = None,
          tools: list[str] | None = None, max_sessions: int | None = None,
          exports: list[Path] = (), now: datetime | None = None) -> dict:
    """Find sessions, write one document each to out, and publish them to output."""
    tools = tools or list(TOOLS)
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=since) if since else None
    problems, sessions = [], []
    sources = local_sources(home)
    for tool, folder in sources.items():
        if tool in tools and folder.exists():
            sessions.extend(local_sessions(tool, folder, cutoff, problems))
    for path in exports:
        try:
            sessions.extend(item for item in export_sessions(path) if item["tool"] in tools)
        except (OSError, ValueError, KeyError, AttributeError, TypeError, zipfile.BadZipFile) as exc:
            problems.append(f"{path}: {exc.__class__.__name__}")
    if cutoff:
        sessions = [item for item in sessions if item["updated"] >= cutoff]
    found = {tool: sum(item["tool"] == tool for item in sessions) for tool in TOOLS}
    # --max-sessions keeps the most recent sessions.
    sessions.sort(key=lambda item: (item["updated"], item["tool"], item["key"]), reverse=True)
    sessions = sorted(sessions[:max_sessions] if max_sessions else sessions,
                      key=lambda item: (item["started"], item["tool"], item["key"]))
    # Summary mode keeps every full transcript beside the summaries, in a folder
    # search does not read.
    transcripts = out.parent / "transcripts" if mode == "summary" else None
    summary = {"found": found, "documents": 0, "redactions": 0, "records": 0, "problems": problems,
               "transcripts": str(transcripts) if transcripts else None,
               "looked_in": [str(sources[t]) for t in sources if t in tools] + [str(p) for p in exports]}
    if not sessions:
        return summary
    out.mkdir(parents=True, exist_ok=True)
    # Documents from an earlier run are replaced, so the folder and the export
    # hold exactly this run's sessions. Only files this command names are removed.
    for old in out.glob("SESSION-*.md"):
        old.unlink()
    if transcripts:
        transcripts.mkdir(parents=True, exist_ok=True)
        for old in transcripts.glob("SESSION-*.md"):
            old.unlink()
    taken, taken_full = set(), set()
    for item in sessions:
        link = None
        if transcripts:
            full_id, full, _ = render(item, "raw", taken_full)
            path = transcripts / f"{full_id}.md"
            path.write_text(full, encoding="utf-8", errors="replace", newline="\n")
            link = path.as_posix()
        doc_id, content, redactions = render(item, mode, taken, link)
        (out / f"{doc_id}.md").write_text(content, encoding="utf-8", errors="replace", newline="\n")
        summary["documents"] += 1
        summary["redactions"] += redactions
    summary["records"] = ingest(out, output, mode="page")["records"]
    return summary


def main():
    """Parse options, build the session documents and print a plain-English report."""
    parser = argparse.ArgumentParser(
        description="Turn your AI-agent session history into searchable documents")
    parser.add_argument("--mode", choices=("summary", "raw"), default="summary",
                        help="summary (default): one short page per session, with the full transcript kept beside it "
                             "in a transcripts folder that is not searched; raw: every message and tool output, all searched")
    parser.add_argument("--since", type=float, metavar="DAYS",
                        help="Only sessions active in the last DAYS days (default: all)")
    parser.add_argument("--tools", default=",".join(TOOLS),
                        help=f"Comma-separated sources to read (default: all of {','.join(TOOLS)})")
    parser.add_argument("--max-sessions", type=int, metavar="N", help="Keep only the N most recent sessions")
    parser.add_argument("--export", type=Path, action="append", default=[], metavar="PATH",
                        help="A ChatGPT or Claude.ai data export (.zip or conversations.json); repeatable")
    parser.add_argument("--out", type=Path, default=Path("sessions/docs"),
                        help="Folder for the session documents (default: sessions/docs)")
    parser.add_argument("--output", type=Path, default=Path("data/sessions.jsonl"),
                        help="Export path for search (default: data/sessions.jsonl)")
    args = parser.parse_args()
    tools = [name.strip() for name in args.tools.split(",") if name.strip()]
    unknown = sorted(set(tools) - set(TOOLS))
    if unknown or not tools:
        parser.error(f"--tools takes names from: {', '.join(TOOLS)}")
    if args.since is not None and args.since <= 0:
        parser.error("--since must be a positive number of days")
    if args.max_sessions is not None and args.max_sessions < 1:
        parser.error("--max-sessions must be at least 1")
    for path in args.export:
        if not path.is_file():
            parser.error(f"--export: {path} is not a file")

    summary = build(Path.home(), args.out, args.output, args.mode, args.since, tools,
                    args.max_sessions, args.export)
    total = sum(summary["found"].values())
    if total == 0:
        print("No sessions found, so nothing was written.")
        print("Looked in:")
        for place in summary["looked_in"]:
            print(f"  {place}")
    else:
        print("Sessions found:")
        for tool, count in summary["found"].items():
            if count:
                print(f"  {TOOLS[tool]:<12} {count}")
        print(f"Wrote {summary['documents']} documents ({args.mode} mode) to {args.out}")
        if summary["transcripts"]:
            print(f"Kept {summary['documents']} full transcripts in {Path(summary['transcripts']).as_posix()} "
                  "(not searched; each summary names its file)")
        print(f"Redacted {summary['redactions']} likely secrets (replaced with [REDACTED])")
        print(f"Published {summary['records']} records to {args.output}")
    if summary["problems"]:
        print(f"Skipped {len(summary['problems'])} files that could not be read:")
        for problem in summary["problems"]:
            print(f"  {problem}")
    if total:
        print("\nNext, try:")
        print(f'  uv run rag-search "{NEXT_QUERY}" --data {args.output.as_posix()} --mode bm25')


if __name__ == "__main__":
    main()
