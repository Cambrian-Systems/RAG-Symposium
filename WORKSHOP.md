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
loads 1,847 pages of documents, connects the search tools to itself, and tells
you what to do next. [SETUP.md](SETUP.md) is what it follows.

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
Run rag-check and tell me whether the documents are loaded and how many records there are.
```

You should see 1,847 records. Fallback: `uv run rag-check`.

## Checkpoint 2: can your agent see the tools?

Start a **new session**, then ask:

```text
What tools do you have, and is the data loaded?
```

It should call `data_status` and report 1,847 records in bm25 mode. Look for
three tools: `data_status`, `search_documents` and `get_document`. Your agent
may show them with a prefix such as `rag_`.

If the tools are missing, your agent could not start the search server,
usually because it cannot find uv. Paste this, then start a new session:

```text
Find the full path of the uv program on this computer and put that full path in place of "uv" in the rag server settings (opencode.jsonc if this is OpenCode).
```

## Checkpoint 3: does the cited page actually say it?

Ask two questions of your own about U.S. AI rules. Then ask:

```text
Show me the passage you cited, word for word, and which document and page it came from.
```

Open that page yourself. Each document is a text file in `corpus/docs/`, named
by its ID, with page markers inside. Does the page say that?

Fallback: `uv run rag-search "your question"` shows exactly what search hands
the agent.

## Round 1: switch your search to hybrid

```text
Change the rag search server from "bm25" to "hybrid". It is the --search value: in opencode.jsonc if this is OpenCode, otherwise in your MCP settings.
```

Start a new session, then ask:

```text
Call data_status and tell me the search mode.
```

Fallback: in OpenCode, open `opencode.jsonc` in a text editor, change
`"bm25"` to `"hybrid"`, save, and start a new session. In another agent,
change the same word in its MCP settings.

## Round 2: see what saved it

```text
What must federal agencies do before using rights-impacting AI?
```

Did your agent say the memo was rescinded? Then paste this and ask the same
question again:

```text
For every source you use, state its date and status, and prefer documents that are currently in force.
```

Check one row of its sources table against the header of that document in
`corpus/docs/`.

Fallback:
`uv run rag-search "What must federal agencies do before using rights-impacting AI?"`

## Round 3: ask it something the documents can't answer

```text
What is Kansas State University's policy on students using generative AI in coursework?
```

Did you get extra "general knowledge" details? Could you check them? Ask
again, adding this sentence:

```text
If the documents do not contain the answer, say so plainly.
```

Fallback:
`uv run rag-search "What is Kansas State University's policy on students using generative AI in coursework?"`

## Round 4: make it search first

```text
What is a large language model?
```

Did it answer without searching? Paste this, then start a new session and ask
the same question again:

```text
In src/rag_symposium/server.py, replace the first line of the search_documents description with: "Search the document collection. Call this first for EVERY question, including general ones, and answer only from what it returns, citing [record-id]." Do not try to reconnect; I will start a new session.
```

Fallback: edit the `search_documents` description in
`src/rag_symposium/server.py` in a text editor, save, and start a new session.

## Evaluate: write five test questions (10 minutes)

```text
Write five test questions about NIST-AI-600-1, including one the documents cannot answer. Tell me where each answer is.
```

Open the source page for one of them yourself. Does it say that? Then:

```text
Add them to evals/starter.jsonl in the same format as the existing lines, run rag-eval, and paste the rag-eval lines for the new questions exactly as printed.
```

Read what the tool printed, not what the agent says it printed. You can pick
any document you care about in place of `NIST-AI-600-1`.

Fallback: copy the format of a line in `evals/starter.jsonl` in a text editor,
then run `uv run rag-eval`.

## Two habits that save time

- **Start a new session** after any change to the search server's settings or
  to `server.py`. The search server only restarts with a new session. Don't
  ask the agent to reconnect.
- **Web search.** This folder switches OpenCode's web tools off. In any other
  agent, switch web search off for today if you can. If you can't, check
  whether each answer came from the documents or from the web.
- **Stuck?** Pair with a neighbour and keep following along. We will finish
  your laptop with you during the open floor.
