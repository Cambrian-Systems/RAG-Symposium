# Agent-assisted workshop setup

Use a **local coding agent that can read files and run commands on your laptop**.
It prepares this existing project and helps with the client connection. The
chatbot you later ask source questions can be a different application.

## Prework

Install/sign in to the local agent and obtain this repo through the presenters'
access route. Python and uv should be available before class; an agent can help
with installation during prework. Test the intended chatbot account and
connection route in advance using [CLIENT_SETUP.md](CLIENT_SETUP.md).

No specific agent product is required by this project. Presenters must rehearse
one supported local-agent route and its permissions before recommending it.
A browser-only chat without local tools cannot run this setup just from a prompt.

## The one setup prompt

Paste this into the local agent with the repo open:

> Read presentation/AGENT_SETUP.md and set up this repo on my computer. Run the
> prepared setup script, help connect my selected MCP client, and report evidence
> for three checkpoints: data loaded, tools connected, and answer supported.

## Instructions for the setup agent

1. Read the repo README, this guide and `presentation/CLIENT_SETUP.md`. Inspect
   the current folder, available Python/uv and existing client settings. Ask
   which MCP client the attendee wants only if it is not already clear.
2. Run the existing `setup-workshop.py` from the repo. With uv available:

   ```sh
   uv run python setup-workshop.py
   ```

   It installs locked dependencies, runs the tests and both MCP protocol checks,
   rebuilds `data/documents.jsonl` in page mode, and verifies a source-linked read.
   Re-running it restores the generated export to the shared page baseline.
   It creates no embeddings and does not configure a chatbot or tunnel.
3. If a step fails, read the reported error and explain the next action in plain
   language. Use existing diagnostics. Handle routine environment/path repairs;
   ask a presenter if the fix would require changing implementation or dependencies.
   Use the existing server, tests and ingestion. Setup is not an instruction to
   generate a new server or rewrite the project. Preserve unrelated files and
   client connections; do not commit, push or alter global Git identity.
4. Help configure the attendee's chosen connection route using the existing
   `mcp.example.json` and [client guide](CLIENT_SETUP.md). Inspect and merge with
   existing client settings rather than replacing them. Use absolute paths.
   A local-process client starts the server itself. An HTTP route needs the
   existing HTTP launcher running; cloud clients also need their prepared route
   to the laptop. Avoid starting duplicate listeners and explain how to stop any
   foreground process you start.
5. Let the attendee complete sign-ins, permission choices and credential entry
   through the appropriate application. Do not put literal credentials into the
   repo, chat response, recording or client example. If the connection requires
   unavailable workspace permissions or UI actions you cannot perform, say so
   and give the precise next step; a prepared pair is an acceptable class fallback.
6. Verify the **actual client**, not only the test client: discover all three
   tools, call `data_status`, then search/read an available record. If you cannot
   observe these calls in that client, mark that checkpoint pending.
7. Have the attendee use the first source question in
   [EXERCISES.md](EXERCISES.md). Inspect the actual tool result and compare one
   generated claim with the source. Do not claim the answer checkpoint passed
   based solely on direct Python calls, a recording or the agent's own summary.
8. Finish with this short report, using `verified`, `pending` or `blocked` and
   the evidence or next step for each:

   | Checkpoint | Evidence to report |
   | --- | --- |
   | Data loaded | Actual export path, record count and one source-linked ID |
   | Tools connected | Chosen client and observed discovery/status/search/read calls |
   | Answer supported | One generated claim checked against the returned/source text |

The reviewed snapshot has 3,274 page records. Report what actually loaded; check
revision and mode if the count differs. Report an incomplete client setup
honestly even if all local checks pass.

## Fallback without a local agent

With Python and uv already installed, run the same single command from the repo:

```sh
uv run python setup-workshop.py
```

Then use the prepared client instructions or ask a presenter to help connect.
This automates the local checks/ingestion; it does not automate account access or
prove a chatbot can reach the server. Attendees can join a prepared pair at the
setup checkpoint and continue the evidence exercises.

## Changing chunking later

The attendee asks the local setup agent to run the existing ingestion mode; the
question-answering chatbot then makes a fresh search call. These jobs may be in
two applications. Command references for the agent/presenter:

```sh
uv run rag-ingest --mode window
uv run rag-ingest --mode document
uv run rag-ingest --mode page
```

Keep query/limit fixed while comparing modes. Restore page mode afterward and
search again before reusing an ID or offset. Changing the data requires a fresh
tool call, not a new tool implementation.
