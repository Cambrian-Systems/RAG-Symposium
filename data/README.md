# Search exports

This folder starts empty. `uv run rag-ingest` writes the workshop documents
here as `documents.jsonl`, and `uv run rag-sessions` writes your own AI sessions
here as `sessions.jsonl`. The search server only reads these files; Git ignores
them, so nothing in here is ever committed.
