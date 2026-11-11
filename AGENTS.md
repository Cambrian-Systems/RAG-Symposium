# Notes for AI agents working in this folder

This is a small search tool over 62 official U.S. documents about AI, used in
a workshop. The person you are helping may not program. Do what they ask
yourself, keep explanations short, and show command output as printed.

## Answering questions

For any question about AI rules, policies or guidance, call `search_documents`
first, read what it returns (use `get_document` for more of a page), and answer
only from that, citing the record ID. Do not answer from memory or the web. If
the documents do not contain the answer, say so plainly. Questions about the
person's own AI sessions go to the `sessions` search tools in the same way. If
you have no search tools, say so and tell the person to start a new session
from this folder.

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
  `--export PATH`, a ChatGPT or Claude.ai export) into one short summary page
  per session in `sessions/docs/` and publishes them to `data/sessions.jsonl`,
  with likely secrets redacted. It keeps each full transcript in
  `sessions/transcripts/`, which search does not read; each summary names that
  file, so open it when the user asks for details. `--mode raw` searches every
  message and tool output instead. Search it with
  `uv run rag-search "question" --data data/sessions.jsonl --mode bm25`, or
  through the `sessions` search server (in `opencode.jsonc`, or in the agent's
  own MCP settings; see `mcp.example.json`). Show its report unchanged. If it
  finds no sessions, say so plainly and suggest a chatbot export or pairing
  with a neighbour. After it runs, tell the person to start a new session.

After any change to the server's settings or to `server.py`, tell the person
to start a new session: the running server does not pick up changes, and it
cannot be reconnected from inside a session.
