# Setup, for an AI agent

You are an AI agent setting this project up for someone who may not program.
Run the commands yourself, in order. Keep what you tell them short. Stop and
show the exact error if a step fails.

The person only needs to send you one prompt:

```text
Set up https://github.com/Cambrian-Systems/RAG-Symposium on this computer by following the SETUP.md file in it. Tell me when it's done and what to do next.
```

## 1. Get the folder

Skip this if you are already inside a folder that contains this file and
`pyproject.toml`.

```bash
git clone https://github.com/Cambrian-Systems/RAG-Symposium
```

If git is not installed, download
<https://github.com/Cambrian-Systems/RAG-Symposium/archive/refs/heads/main.zip>,
unzip it and rename the folder to `RAG-Symposium`. Put it somewhere the person
can find again, such as their Documents folder. Work inside that folder from
here on, and note its full path.

## 2. Make sure uv is installed

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

## 3. Install the project and load the documents

```bash
uv sync --locked
uv run rag-ingest
uv run rag-check
```

`rag-ingest` should publish 1,847 records from 62 documents. `rag-check` should
print four lines that start with `PASS`. Nothing here needs a download beyond
the Python packages: the embedding model is in the `models/` folder.

## 4. Connect the search server to the agent the person will use

The server is a local MCP server that the agent launches itself. Do not start
it in the background and do not run it as an HTTP service.

**OpenCode:** nothing to add. `opencode.jsonc` in this folder connects it when
the folder is opened. If OpenCode cannot find `uv`, replace `"uv"` in
`opencode.jsonc` with the full path from step 2.

**Any other agent (Codex, Claude Code, Cursor, VS Code, Gemini CLI and so
on):** add a local stdio MCP server named `rag` to your own MCP settings, in
whatever way your app documents. [mcp.example.json](mcp.example.json) shows the
shape. Use full paths, not relative ones:

- command: the full path of `uv`
- arguments: `run`, `--directory`, the full path of this folder, `--locked`,
  `rag-symposium`, `--search`, `bm25`, `--data`, the full path of
  `data/documents.jsonl` in this folder

Each argument is a separate item. Do not join them into one string.

## 5. Say whether web search is on

In the workshop, answers should come from the documents in this folder.
`opencode.jsonc` switches OpenCode's web tools off. In any other agent, tell
the person whether you have web search or web browsing available, and how to
switch it off for this project if that is possible. Do not change their global
settings without asking.

## 6. Tell the person what to do next

Finish with a short message that says:

1. Whether every `rag-check` line said PASS, and the record count.
2. Where the folder is.
3. To open the `RAG-Symposium` folder in their agent and start a **new
   session**, so the search tools load.
4. To ask in that new session: `What tools do you have, and is the data loaded?`
   The answer should name three tools, `data_status`, `search_documents` and
   `get_document`, and report 1,847 records in bm25 mode.
5. That `WORKSHOP.md` in the folder has every prompt for the rest of the
   session.

Do not edit anything under `src/` or `corpus/` during setup.
