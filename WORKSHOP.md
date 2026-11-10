# Workshop guide

Everything you type in the workshop, in order. Copy each prompt from this page
and paste it into OpenCode. The slides show the same prompts.

You never have to write code. If OpenCode gets stuck, each step has a fallback
you can run by hand.

## Set up (start as soon as you sit down)

**1. Install OpenCode.** Download the desktop app from
<https://opencode.ai/desktop> and install it. The installers are also on the
USB sticks on the tables.

**2. Get this folder.** On the GitHub page for this project, choose
**Code › Download ZIP** and unzip it, or copy the folder from a USB stick. Then
open the folder in OpenCode. Open the `RAG-Symposium` folder itself, not the
folder above it.

**3. Connect a model.** Type `/connect` in OpenCode and pick one of these:

| You have | Choose | Then |
|---|---|---|
| Nothing (most people) | **OpenCode** | Paste the workshop key from the sheet on your table. Type `/models` and pick **GLM-5.3-Flash**. |
| ChatGPT Plus or Pro | **OpenAI** | Choose **Sign in with ChatGPT**. Type `/models` and pick a model. |
| GitHub Copilot, including Copilot Free | **GitHub Copilot** | Sign in with GitHub. Type `/models` and pick a model. |
| Your own API key | Your provider | Paste the key. Type `/models` and pick a model. |

The free ChatGPT plan and Claude Pro/Max subscriptions cannot sign in to
OpenCode. Use the workshop key instead.

Whichever model you connect, the tools are the same: they come from OpenCode
and from this folder, not from the model. What changes is how well the model
uses them, and we will compare.

The workshop key is switched off when the session ends.

**4. Let the agent install the project.** Paste:

```text
If uv is not installed on this computer, install it for this user only, following https://docs.astral.sh/uv/ . Then run uv sync --locked, then uv run rag-ingest, then uv run rag-check, and tell me whether every line says PASS.
```

OpenCode asks before it runs a command. Say yes.

Fallback, in a terminal opened in this folder (needs
[uv](https://docs.astral.sh/uv/)):

```bash
uv sync --locked
uv run rag-ingest
uv run rag-check
```

## Checkpoint 1: is your data loaded?

```text
Run rag-check and tell me whether the documents are loaded and how many records there are.
```

You should see 1,847 records. Fallback: `uv run rag-check`.

## Checkpoint 2: can OpenCode see the tools?

Start a **new session**, then ask:

```text
What tools do you have, and is the data loaded?
```

It should call `rag_data_status` and report 1,847 records in bm25 mode. Look
for the three tools whose names start with `rag_`.

If there are no `rag_` tools, OpenCode could not start the search server,
usually because it cannot find uv. Paste this, then start a new session:

```text
Find the full path of the uv program on this computer and put that full path in place of "uv" in opencode.jsonc.
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
In opencode.jsonc, change "bm25" to "hybrid".
```

Start a new session, then ask:

```text
Call data_status and tell me the search mode.
```

Fallback: open `opencode.jsonc` in a text editor, change `"bm25"` to
`"hybrid"`, save, and start a new session.

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

- **Start a new session** after any change to `opencode.jsonc` or `server.py`.
  The search server only restarts with a new session. Don't ask the agent to
  reconnect.
- **Stuck?** Pair with a neighbour and keep following along. We will finish
  your laptop with you during the open floor.
