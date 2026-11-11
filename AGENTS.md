# Instructions for AI agents

This is a local search tool over 62 official U.S. AI documents, used in a
workshop. The user may not program. Do the work yourself, keep explanations
short, and show command output unchanged.

## Answering questions

For AI rules, policies, or guidance, call `search_documents` first. Read the
results, use `get_document` for more text, and answer only from those records,
citing record IDs. Do not answer from memory or the web. If the documents do
not answer the question, say so. Use the `sessions` search tools the same way
for questions about the user's own AI sessions. If the tools are unavailable,
say so and tell the user to start a new session from this folder.

## Working in this project

- Follow [README.md](README.md) for [setup](README.md#setup),
  [workshop prompts](README.md#workshop), commands, and file locations.
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
