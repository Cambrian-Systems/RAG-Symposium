# Instructions for AI agents

This is a local search tool over 62 official U.S. AI documents, used in a
workshop. The user may not program. Do the work yourself, keep explanations
short, and show command output unchanged.

## Setup

When the user asks you to set this project up, run these steps yourself, in
order. Keep what you tell them short, and stop and show the exact error if a
step fails. Do not edit `src/` or `corpus/` during setup.

### 1. Get the folder

Skip this if you are already inside the folder that contains this file and
`pyproject.toml`.

```bash
git clone https://github.com/Cambrian-Systems/RAG-Symposium
```

If git is not installed, download
<https://github.com/Cambrian-Systems/RAG-Symposium/archive/refs/heads/main.zip>,
unzip it and rename the folder to `RAG-Symposium`. Put it somewhere the person
can find again, such as their Documents folder. Work inside that folder from
here on, and note its full path.

### 2. Make sure uv is installed

Run `uv --version`. If it is missing, install it for this user only, with no
administrator rights:

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

A shell that was already open may not see it yet. Find the full path of the
`uv` program (often `~/.local/bin/uv`, or `%USERPROFILE%\.local\bin\uv.exe` on
Windows) and use that full path from here on.

### 3. Install the project and load the documents

```bash
uv sync --locked
uv run rag-ingest
uv run rag-check
```

`rag-ingest` should publish 1,847 records from 62 documents. `rag-check` should
print four lines that start with `PASS`. Nothing here needs a download beyond
the Python packages: the embedding model is in the `models/` folder.

### 4. Connect the search server to the agent the person will use

The server is a local MCP server that the agent launches itself. Do not start
it in the background and do not run it as an HTTP service.

**OpenCode:** nothing to add. `opencode.jsonc` in this folder connects it when
the folder is opened. If OpenCode cannot find `uv`, replace every `"uv"` in
`opencode.jsonc` (there are two) with the full path from step 2.

**Any other agent (Codex, Claude Code, Cursor, VS Code, Gemini CLI and so
on):** add two local stdio MCP servers, `rag` and `sessions`, to your own MCP
settings for this folder, in whatever way your app documents (for Claude Code,
`claude mcp add` with project scope, or a `.mcp.json` in this folder).
[mcp.example.json](mcp.example.json) shows the shape. Use full paths, not
relative ones:

- command: the full path of `uv`
- arguments for `rag`: `run`, `--directory`, the full path of this folder,
  `--locked`, `rag-symposium`, `--search`, `bm25`, `--data`, the full path of
  `data/documents.jsonl` in this folder
- arguments for `sessions`: the same, except the last one is the full path of
  `data/sessions.jsonl`. That file does not exist yet; it is created later in
  the workshop, and the server reports 0 records until then.

Each argument is a separate item. Do not join them into one string. If your
app asks the person to approve a project's MCP servers (Claude Code does), tell
them to say yes; declining leaves them with no search tools.

If your app does not load `AGENTS.md` by itself in a new session, make it do
so for this folder in the way your app documents (for older Gemini CLI
versions, a `GEMINI.md` in this folder containing the line `@AGENTS.md`).

### 5. Say whether web search is on

In the workshop, answers should come from the documents in this folder.
`opencode.jsonc` switches OpenCode's web tools off. In any other agent, tell
the person whether you have web search or web browsing available, and how to
switch it off for this project if that is possible. Do not change their global
settings without asking.

### 6. Tell the person what to do next

Finish with a short message that says:

1. Whether every `rag-check` line said PASS, and the record count.
2. Where the folder is.
3. To open the `RAG-Symposium` folder in their agent and start a **new
   session**, so the search tools load.
4. To ask in that new session: `What tools do you have, and is the data loaded?`
   The answer should name three tools, `data_status`, `search_documents` and
   `get_document` (often with a prefix such as `rag_` or `mcp__rag__`), and
   report 1,847 records in bm25 mode. The same three tools for `sessions` show
   0 records; they are for later in the workshop.
5. That the Workshop section of [README.md](README.md#workshop) has the
   prompts for the rest of the session.

## Answering questions

For AI rules, policies, or guidance, call `search_documents` first. Read the
results, use `get_document` for more text, and answer only from those records,
citing record IDs. Do not answer from memory or the web. If the documents do
not answer the question, say so. Use the `sessions` search tools the same way
for questions about the user's own AI sessions. If the tools are unavailable,
say so and tell the user to start a new session from this folder.

## Working in this project

- [README.md](README.md) has the [workshop prompts](README.md#workshop),
  commands, and file locations.
- Check readiness with `uv run rag-check`: expect four PASS lines and 1,847
  records for the workshop corpus. Run evals with `uv run rag-eval` and show
  the output unchanged.
- After changing server settings or `src/rag_symposium/server.py`, tell the
  user to start a new session. The running server cannot be reconnected from
  inside a session.
- For session imports, run `uv run rag-sessions`, show its report unchanged,
  and tell the user to start a new session. Search the summaries; open the
  linked full transcript when details are needed. If no sessions are found,
  say so and suggest a chatbot export or pairing with a neighbour.
