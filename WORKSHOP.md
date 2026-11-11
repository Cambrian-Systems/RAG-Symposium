# Workshop guide

Everything you type in the workshop, in order. Copy each prompt from this page
and paste it into your agent. The slides show the same prompts.

You never have to write code. If your agent gets stuck, each step has a
fallback you can run by hand.

## Set up: one prompt (start as soon as you sit down)

Use any AI agent that can run commands on your laptop: Codex, Claude Code,
Cursor, Copilot in VS Code, Gemini CLI, OpenCode or another. A chatbot that
only runs in a browser tab cannot do this.

Send it this:

```text
Set up https://github.com/Cambrian-Systems/RAG-Symposium on this computer by following the SETUP.md file in it. Tell me when it's done and what to do next.
```

Say yes when it asks to run commands. It downloads this folder, installs it,
loads 1,847 pages of documents, adds the search tools to its settings, and
tells you to start a new session so they load. [SETUP.md](SETUP.md) is what it follows.

If you already have this folder (from a USB stick, say), open it in your agent
and send `Follow SETUP.md in this folder.` instead.

**No agent yet?** Install [OpenCode](https://opencode.ai/desktop), which is
free and open source (installers are on the USB sticks). Type `/connect`,
choose **OpenCode** and paste the workshop key from the sheet on your table,
then type `/models` and pick **GLM-5.3-Flash**. If you pay for ChatGPT Plus or
Pro, or have GitHub Copilot, you can choose **OpenAI** or **GitHub Copilot** in
`/connect` instead. Then send the prompt above.

Fallback, in a terminal opened in this folder (needs
[uv](https://docs.astral.sh/uv/)):

```bash
uv sync --locked
uv run rag-ingest
uv run rag-check
```

Whichever agent and model you use, the search tools are the same: they come
from this folder. What changes is how well each model uses them, and we will
compare.

## Checkpoint 1: is your data loaded?

```text
Did setup finish? How many records are loaded?
```

You should see 1,847 records.

Fallback: `uv run rag-check`

## Checkpoint 2: can your agent see the tools?

Start a new session, then ask:

```text
What tools do you have, and is the data loaded?
```

It should call `data_status` and report 1,847 records in bm25 mode. Look for
three tools: `data_status`, `search_documents` and `get_document`. Your agent
may show them with a prefix such as `rag_`. You may also see the same three for
`sessions`, with 0 records: those are for part two.

If the tools are missing, your agent could not start the search server,
usually because it cannot find uv. Paste this, then start a new session:

```text
Find the full path of the uv program on this computer and put that full path in place of "uv" in the rag server settings (opencode.jsonc if this is OpenCode).
```

## Checkpoint 3: does the cited page actually say it?

Ask a question about U.S. AI rules: your own, or one of these, which the
documents can answer.

```text
Can NIH reviewers use ChatGPT to help write their critiques?
```

```text
Do I have to tell NSF if I used AI to write my grant proposal?
```

```text
Can federal education grant money pay for a chatbot that advises students?
```

```text
Should there be a law against making an AI clone of my voice without permission?
```

```text
How much did generative AI use grow at federal agencies between 2023 and 2024?
```

```text
How many grant applications can one researcher submit to NIH in a year?
```

Then ask:

```text
Show me the exact passage you cited, and which document and page it's from.
```

Open that page yourself. Each document is a text file in `corpus/docs/`, named
by its ID, with page markers inside. Does the page say that?

Fallback: `uv run rag-search "your question"` shows exactly what search hands
the agent.

## Search your own AI sessions (15 minutes)

```text
Turn my AI sessions on this laptop into a searchable collection.
```

Your agent runs `uv run rag-sessions`. It finds the sessions your AI agents
saved on this laptop (Claude Code, Codex, OpenCode, Gemini CLI), replaces
anything that looks like a password or key with `[REDACTED]`, writes one
document per session and loads them into the `sessions` search tools. Nothing
leaves your laptop. If you use one of those agents, you have at least today's
setup session. If it finds none (Cursor and Copilot keep their history
somewhere else), pair with a neighbour or load a chatbot export (below).
Then start a new session, so the `sessions` tools see the new data, and ask:

```text
What went wrong during setup today, and how did we fix it?
```

Then ask your own: a decision you made, a prompt you wish you'd kept,
something from last month.

Then try the summary layer and ask the same question again:

```text
Rebuild my sessions in summary mode, then ask the same question again.
```

Web chatbots (ChatGPT, Claude, Gemini) keep your history on their servers.
Request an export (ChatGPT: Settings › Data controls › Export data; Claude:
Settings › Privacy › Export data; Gemini: Google Takeout); it arrives by email.
Then: `Load my chatbot export from <path to the zip>.`

Redaction catches the obvious patterns, not everything. Read a few documents
in `sessions/docs/` before you share anything.

Fallback: `uv run rag-sessions`, then
`uv run rag-search "what went wrong during setup?" --data data/sessions.jsonl --mode bm25`.
`uv run rag-sessions --mode summary` writes one short page per session, and
`uv run rag-sessions --export path/to/export.zip` loads a chatbot export.

## Your own documents (if there is time)

```text
Add this document to the collection.
```

Give it a file, or paste the text. Then ask a question only that document can
answer.

Before you load anything sensitive: the documents and the search stay on your
laptop, but your question and every passage search returns are sent to whoever
runs your model.

Fallback: put one text file per document in `corpus/docs/` with a short header
(see "Using your own documents" in [README.md](README.md)), then run
`uv run rag-ingest`.

## Three habits that save time

- **Start a new session** after any change to the search server's settings or
  to `server.py`. The search server only restarts with a new session. Don't
  ask the agent to reconnect.
- **Web search.** This folder switches OpenCode's web tools off. Other agents
  probably have web search on, so check whether each answer came from the
  documents or from the web.
- **Stuck?** Pair with a neighbour and keep following along. We will finish
  your laptop with you during the hands-on time.
