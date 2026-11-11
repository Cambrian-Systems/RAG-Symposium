"""Test rag-sessions: each session format, redaction, summary mode and a full run.

Every session here is made up. tests/fixtures/sessions/home is a pretend home
folder laid out the way each agent stores its sessions; the OpenCode databases
are SQL text that each test loads into a temporary opencode.db. The full run
points HOME at a temporary copy of that folder and searches the published
records with the server's own RecordStore.
"""
import contextlib
import io
import os
import shutil
import sqlite3
import sys
import tempfile
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from rag_symposium import sessions
from rag_symposium.ingest import read_document
from rag_symposium.store import RecordStore

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "sessions"
HOME = FIXTURES / "home"
FAKE_KEY = "sk-FAKEtestKEY0123456789abcdef"
FAKE_CARD = "4111 1111 1111 1111"  # The standard Luhn-valid test card number.
# Clear the variables that would send discovery to a real agent folder.
CLEAN_ENVIRONMENT = {"CLAUDE_CONFIG_DIR": "", "CODEX_HOME": "", "XDG_DATA_HOME": ""}


def kinds(item):
    return [kind for kind, _ in item["entries"]]


def texts(item, kind=None):
    return [text for k, text in item["entries"] if kind in (None, k)]


class SessionTestCase(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.folder = Path(folder.name)
        patcher = mock.patch.dict(os.environ, CLEAN_ENVIRONMENT)
        patcher.start()
        self.addCleanup(patcher.stop)

    def database(self, sql_name):
        """Load a fixture SQL file into a temporary opencode.db and return its folder."""
        data_dir = self.folder / "opencode"
        data_dir.mkdir(exist_ok=True)
        connection = sqlite3.connect(data_dir / "opencode.db")
        connection.executescript((FIXTURES / sql_name).read_text(encoding="utf-8"))
        connection.commit()
        connection.close()
        return data_dir


class FormatTests(SessionTestCase):
    def test_claude_code_keeps_typed_messages_and_tool_calls(self):
        """Injected, meta, sidechain and thinking text are left out; bad lines are skipped."""
        path = next((HOME / ".claude" / "projects").glob("*/*.jsonl"))
        item = sessions.claude_code_session(path)
        self.assertEqual(item["tool"], "claude")
        self.assertEqual(item["key"], "11111111-aaaa-4bbb-8ccc-000000000001")
        self.assertEqual(kinds(item), ["you", "agent", "call", "output", "agent", "you", "agent"])
        self.assertIn("[tool: Bash] uv sync --locked", texts(item, "call"))
        self.assertEqual(texts(item, "output"), ["error: The lockfile needs to be updated"])
        everything = " ".join(texts(item))
        for left_out in ("Caveat", "Injected", "SIDECHAIN", "PRIVATE THINKING"):
            self.assertNotIn(left_out, everything)
        self.assertEqual(item["started"], datetime(2026, 11, 9, 10, 0, 1, tzinfo=timezone.utc))
        self.assertTrue(item["source_url"].startswith("file://"))

    def test_codex_skips_instructions_and_subagents(self):
        files = sorted((HOME / ".codex" / "sessions").glob("**/*.jsonl"))
        item = sessions.codex_session(files[0])
        self.assertEqual(kinds(item), ["you", "call", "output", "call", "output", "agent"])
        self.assertEqual(texts(item, "you"), ["Why does rag-check fail on the embedding model?"])
        self.assertEqual(texts(item, "call")[0], "[tool: exec_command] uv run rag-check")
        self.assertEqual(texts(item, "output")[1], "Success. Updated README.md")
        self.assertIsNone(sessions.codex_session(files[1]))  # A sub-agent session.

    def test_opencode_newest_database(self):
        """session_v2 + session_message: reasoning and child sessions are left out."""
        found = sessions.opencode_db_sessions(self.database("opencode-v2.sql") / "opencode.db")
        self.assertEqual([item["key"] for item in found], ["ses_v2demo"])
        item = found[0]
        self.assertEqual(kinds(item), ["you", "call", "output", "agent"])
        self.assertEqual(texts(item, "call"), ["[tool: rag_search_documents] AI literacy"])
        self.assertNotIn("PRIVATE REASONING", " ".join(texts(item)))
        self.assertTrue(item["source_url"].endswith("opencode.db#ses_v2demo"))

    def test_opencode_earlier_database_and_storage_folder(self):
        """session + message + part rows, and the storage/ JSON files before them."""
        found = sessions.opencode_db_sessions(self.database("opencode-v1.sql") / "opencode.db")
        item = found[0]
        self.assertEqual(kinds(item), ["you", "call", "output", "agent"])
        self.assertEqual(texts(item, "output"), ["uv: command not found"])
        self.assertNotIn("SYNTHETIC", " ".join(texts(item)))
        stored = sessions.opencode_storage_sessions(HOME / ".local" / "share" / "opencode" / "storage")
        self.assertEqual([s["key"] for s in stored], ["ses_storage1"])
        self.assertEqual(texts(stored[0], "call"), ["[tool: read] /tmp/demo/opencode.jsonc"])

    def test_opencode_unknown_database_is_skipped(self):
        data_dir = self.folder / "opencode"
        data_dir.mkdir()
        sqlite3.connect(data_dir / "opencode.db").execute("CREATE TABLE other (id text)").connection.close()
        self.assertEqual(sessions.local_sessions("opencode", data_dir, None, []), [])

    def test_gemini_cli(self):
        path = next((HOME / ".gemini" / "tmp").glob("*/chats/*.json"))
        item = sessions.gemini_session(path)
        self.assertEqual(kinds(item), ["you", "agent", "call", "output", "agent"])
        self.assertIn("1847 records", texts(item, "output")[0])
        self.assertNotIn("INFO LINE", " ".join(texts(item)))

    def test_chatgpt_export_follows_the_shown_branch(self):
        """Only the branch ending at current_node is kept; hidden system text is not."""
        found = sessions.export_sessions(FIXTURES / "exports" / "chatgpt" / "conversations.json")
        item = found[0]
        self.assertEqual(item["tool"], "chatgpt")
        self.assertEqual(kinds(item), ["you", "call", "output", "agent"])
        self.assertEqual(texts(item, "call"), ["[tool: python] print('[OMB-M-24-10-p3]')"])
        self.assertNotIn("OLD BRANCH ANSWER", " ".join(texts(item)))

    def test_claude_ai_export_prefers_content_blocks(self):
        """The "text" field's tool placeholder never appears; it fills in when content is empty."""
        found = sessions.export_sessions(FIXTURES / "exports" / "claude-ai" / "conversations.json")
        item = found[0]
        self.assertEqual(item["tool"], "claude-ai")
        self.assertEqual(kinds(item), ["you", "agent", "call", "output", "agent", "you"])
        self.assertEqual(texts(item, "call"), ["[tool: web_search] OMB AI governance memo"])
        self.assertNotIn("not supported", " ".join(texts(item)))
        self.assertEqual(texts(item, "you")[-1], "Thanks, that answers it.")

    def test_export_zip_is_read_and_detected(self):
        archive = self.folder / "export.zip"
        with zipfile.ZipFile(archive, "w") as stream:
            stream.write(FIXTURES / "exports" / "claude-ai" / "conversations.json", "conversations.json")
            stream.writestr("users.json", "[]")
        found = sessions.export_sessions(archive)
        self.assertEqual([item["tool"] for item in found], ["claude-ai"])
        self.assertTrue(found[0]["source_url"].startswith(archive.resolve().as_uri() + "#"))


class DocumentTests(unittest.TestCase):
    def test_redaction_replaces_a_fake_key_and_a_luhn_valid_number(self):
        text, count = sessions.scrub(f"key {FAKE_KEY} and card {FAKE_CARD}")
        self.assertEqual(text, "key [REDACTED] and card [REDACTED]")
        self.assertEqual(count, 2)

    def test_redaction_other_patterns_and_what_it_leaves_alone(self):
        text, count = sessions.scrub(
            "Authorization: Bearer abcdefghijklmnop1234\nexport GITHUB_TOKEN=ghp_" + "a" * 36 +
            "\npassword = hunter2hunter2\nAKIAABCDEFGHIJKLMNOP\n"
            "-----BEGIN RSA PRIVATE KEY-----\nMIIfake\n-----END RSA PRIVATE KEY-----")
        self.assertEqual(count, 5)
        self.assertIn("Bearer [REDACTED]", text)
        self.assertIn("GITHUB_TOKEN=[REDACTED]", text)
        self.assertIn("password = [REDACTED]", text)
        self.assertNotIn("MIIfake", text)
        untouched = ("max_tokens: 4000; token = None; order 4111 1111 1111 1112; "
                     "timestamp 1794222000000; built 20261110093000")
        self.assertEqual(sessions.scrub(untouched), (untouched, 0))

    def test_summary_is_much_smaller_than_raw(self):
        """Long tool output fills raw pages; summary mode keeps one short page."""
        entries = [("you", "Why does setup fail?")]
        for step in range(40):
            entries += [("call", f"[tool: shell] step {step}"), ("output", "log line " * 150)]
        entries += [("you", "Try again"), ("agent", "Fixed: the lockfile was stale.")]
        started = datetime(2026, 11, 9, tzinfo=timezone.utc)
        item = {"tool": "codex", "key": "k", "source_url": "file:///tmp/k.jsonl", "entries": entries,
                "started": started, "updated": started}
        _, raw, _ = sessions.render(item, "raw", set())
        doc_id, summary, _ = sessions.render(item, "summary", set())
        self.assertLess(len(summary) * 20, len(raw))
        self.assertEqual(summary.count("<!-- page"), 1)
        self.assertIn("Turns: 2", summary)
        self.assertIn("Fixed: the lockfile was stale.", summary)
        # Raw pages break roughly every PAGE_SIZE characters.
        self.assertGreater(raw.count("<!-- page"), len(raw) // (sessions.PAGE_SIZE * 2))
        self.assertTrue(doc_id.startswith("SESSION-CODEX-2026-11-09-"))

    def test_document_header_matches_the_corpus_format(self):
        started = datetime(2026, 11, 9, tzinfo=timezone.utc)
        item = {"tool": "claude", "key": "k", "source_url": "file:///tmp/k.jsonl", "started": started,
                "updated": started, "entries": [("you", "A " * 100 + "<!-- page 9 --> quoted"), ("agent", "ok")]}
        doc_id, content, _ = sessions.render(item, "raw", set())
        path = Path(tempfile.mkdtemp()) / f"{doc_id}.md"
        self.addCleanup(shutil.rmtree, path.parent)
        path.write_text(content, encoding="utf-8")
        header, pages = read_document(path)
        self.assertEqual(set(header), {"id", "title", "issuer", "published", "status", "source_url"})
        self.assertEqual((header["issuer"], header["published"], header["status"]),
                         ("Claude Code", "2026-11-09", "session"))
        self.assertLessEqual(len(header["title"]), sessions.TITLE_LENGTH + 3)
        self.assertEqual([n for n, _ in pages], [1])  # Marker text in a message is not a page.
        self.assertEqual(sessions.render(item, "raw", set())[0], doc_id)  # Same session, same ID.


class EndToEndTests(SessionTestCase):
    def run_command(self, home, *arguments):
        """Run `rag-sessions` with HOME pointed at home; return what it printed."""
        printed = io.StringIO()
        environment = {"HOME": str(home), "USERPROFILE": str(home)}
        with mock.patch.dict(os.environ, environment), \
                mock.patch.object(sys, "argv", ["rag-sessions", *arguments]), \
                contextlib.redirect_stdout(printed):
            sessions.main()
        return printed.getvalue()

    def test_summary_mode_keeps_the_full_transcript_beside_the_summary(self):
        """Summaries are searched; the full transcripts are kept, named in the summary, and not searched."""
        home = self.folder / "home"
        shutil.copytree(HOME, home)
        out, output = self.folder / "sessions" / "docs", self.folder / "data" / "sessions.jsonl"
        kept = self.folder / "sessions" / "transcripts"
        kept.mkdir(parents=True)
        (kept / "SESSION-OLD-2020-01-01-000000.md").write_text("left from an earlier run")
        printed = self.run_command(home, "--out", str(out), "--output", str(output), "--mode", "summary",
                                   "--tools", "claude,codex")
        self.assertIn(f"Kept 2 full transcripts in {kept.as_posix()}", printed)
        summaries, transcripts = sorted(out.glob("*.md")), sorted(kept.glob("*.md"))
        self.assertEqual([p.name for p in summaries], [p.name for p in transcripts])
        self.assertEqual(len(summaries), 2)
        for short, full in zip(summaries, transcripts):
            self.assertIn(f"Full transcript: {full.as_posix()}", short.read_text(encoding="utf-8"))
            self.assertNotIn("Full transcript:", full.read_text(encoding="utf-8"))
            self.assertNotIn("Turns:", full.read_text(encoding="utf-8"))
            self.assertNotIn(FAKE_KEY, full.read_text(encoding="utf-8"))
        # Only the summaries are published for search.
        self.assertEqual(RecordStore(output, "bm25").status()["record_count"], 2)
        # Raw mode writes no transcripts folder of its own.
        other = self.folder / "raw" / "docs"
        self.run_command(home, "--out", str(other), "--output", str(output), "--tools", "claude")
        self.assertFalse((self.folder / "raw" / "transcripts").exists())

    def test_full_run_publishes_searchable_records(self):
        home = self.folder / "home"
        shutil.copytree(HOME, home)
        connection = sqlite3.connect(home / ".local" / "share" / "opencode" / "opencode.db")
        connection.executescript((FIXTURES / "opencode-v2.sql").read_text(encoding="utf-8"))
        connection.close()
        out, output = self.folder / "docs", self.folder / "data" / "sessions.jsonl"
        out.mkdir()
        (out / "SESSION-OLD-2020-01-01-000000.md").write_text("left from an earlier run")
        printed = self.run_command(home, "--out", str(out), "--output", str(output),
                                   "--export", str(FIXTURES / "exports" / "chatgpt" / "conversations.json"))
        for line in ("Claude Code  1", "Codex        1", "OpenCode     2", "Gemini CLI   1", "ChatGPT      1",
                     "Wrote 6 documents (raw mode)", "Redacted 2 likely secrets",
                     f'rag-search "what went wrong during setup?" --data {output.as_posix()} --mode bm25'):
            self.assertIn(line, printed)
        documents = sorted(out.glob("*.md"))
        self.assertEqual(len(documents), 6)
        written = "".join(path.read_text(encoding="utf-8") for path in documents)
        self.assertNotIn(FAKE_KEY, written)
        self.assertNotIn(FAKE_CARD, written)
        store = RecordStore(output, "bm25")
        self.assertEqual(store.status()["record_count"], len(documents))
        result = store.search("lockfile setup")
        self.assertTrue(result["matches"][0]["id"].startswith("SESSION-CLAUDE-2026-11-09-"))
        self.assertEqual(result["matches"][0]["metadata"]["status"], "session")

        # The same sessions get the same documents; --tools and --max-sessions narrow them.
        again = self.folder / "again"
        self.run_command(home, "--out", str(again), "--output", str(output),
                         "--export", str(FIXTURES / "exports" / "chatgpt" / "conversations.json"))
        self.assertEqual([p.read_text(encoding="utf-8") for p in sorted(again.glob("*.md"))],
                         [p.read_text(encoding="utf-8") for p in documents])
        self.run_command(home, "--out", str(out), "--output", str(output), "--tools", "codex,opencode",
                         "--max-sessions", "2", "--mode", "summary")
        self.assertEqual(sorted(p.name.split("-")[1] for p in out.glob("*.md")), ["CODEX", "OPENCODE"])

    def test_empty_home_says_no_sessions_found(self):
        output = self.folder / "data" / "sessions.jsonl"
        printed = self.run_command(self.folder, "--out", str(self.folder / "docs"), "--output", str(output))
        self.assertIn("No sessions found", printed)
        self.assertFalse(output.exists())
        self.assertFalse((self.folder / "docs").exists())

    def test_since_keeps_recent_sessions(self):
        """build() takes "now", so --since can be tested against fixed fixture dates."""
        now = datetime(2026, 11, 10, 12, tzinfo=timezone.utc)
        summary = sessions.build(HOME, self.folder / "docs", self.folder / "s.jsonl", since=1.5, now=now,
                                 tools=["claude", "codex", "opencode", "gemini"])
        # The storage/ session is from 2026-11-06; the others are from 2026-11-09.
        self.assertEqual(summary["found"]["opencode"], 0)
        self.assertEqual(summary["documents"], 3)


if __name__ == "__main__":
    unittest.main()
