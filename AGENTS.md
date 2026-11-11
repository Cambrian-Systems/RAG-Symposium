# Notes for AI agents working in this folder

This is a small search tool over 62 official U.S. documents about AI, used in
a workshop. The person you are helping may not program. Do what they ask
yourself, keep explanations short, and show command output as printed.

Where things are:

- **Setup:** follow [SETUP.md](SETUP.md).
- **Is the data loaded?** Run `uv run rag-check`. It should print four PASS
  lines and 1,847 records.
- **The search server** is a local MCP server named `rag`. In OpenCode it is
  defined in `opencode.jsonc` in this folder; in other agents it is in the
  agent's own MCP settings (see `mcp.example.json`).
- **Search mode:** the value after `--search` in that server's arguments:
  `keyword`, `bm25` or `hybrid`. To switch, change that one word.
- **The search tool's description and instructions:** `src/rag_symposium/server.py`.
  The description of `search_documents` is the first line of its docstring.
- **Test questions ("the evals"):** `evals/starter.jsonl`, one JSON object per
  line: `id`, `category`, `question`, `expect` (a list of document IDs, or `[]`
  if the documents cannot answer) and optionally `pages`. Run them with
  `uv run rag-eval` and show its output unchanged.
- **Documents:** one text file each in `corpus/docs/`, named `<ID>.md`, with a
  header between `---` lines and `<!-- page N -->` markers. To add one, write a
  new file there (only `id`, `title` and `source_url` are required in the
  header; see "Using your own documents" in README.md), then run
  `uv run rag-ingest`.
- **Trying a search by hand:** `uv run rag-search "question" --mode bm25`.
- **Searching your own AI sessions:** `uv run rag-sessions` turns this
  computer's Claude Code, Codex, OpenCode and Gemini CLI sessions (and, with
  `--export PATH`, a ChatGPT or Claude.ai export) into documents in
  `sessions/docs/` and publishes `data/sessions.jsonl`, with likely secrets
  redacted. `--mode summary` writes one short page per session. Search it with
  `uv run rag-search "question" --data data/sessions.jsonl --mode bm25`, or
  through the `sessions` server in `opencode.jsonc`. Show its report unchanged.

After any change to the server's settings or to `server.py`, tell the person
to start a new session: the running server does not pick up changes, and it
cannot be reconnected from inside a session.
