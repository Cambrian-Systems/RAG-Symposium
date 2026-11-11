# Build a retrieval tool your chatbot can use

Two-hour hands-on symposium workshop · rehearsal draft · November 6, 2026

## The promise

Participants ask a local coding agent to prepare the existing project, then
confirm data loaded, tools connected and an answer supported by source text.
They use the agent to make one measured retrieval change and inspect its effect. They leave with a runnable project and a map of
where to replace the data or improve retrieval.

The presentation demonstrates ChatGPT. The server remains reusable across
compatible clients; account permissions, connection transport and setup differ.
A working ChatGPT connection is a rehearsal prerequisite, not an installation
exercise to improvise during class. Mixed technical audience and pairs are the
working assumptions.

## What the pulled repository actually does

Reviewed revision: `70695d5` — Hayden's corpus ingestion and search-excerpt work,
after the initial MCP foundation. This plan supersedes the earlier 90-minute plan.

| Component | Current behavior | Teaching point |
| --- | --- | --- |
| `corpus/docs/` | 273 committed KSRE crop publications as extracted text | Everyone starts from the same snapshot; no live scraping in class |
| `rag-ingest` | Page, overlapping character-window, or whole-document records | Chunking decides the units search can return |
| `data/documents.jsonl` | Local generated export with source/page/date metadata | Ingestion prepares evidence before a question is asked |
| `RecordStore` | Whole-word keyword matching, distinct-term ranking, 600-character excerpts | Relevant-looking results require inspection; no semantic embeddings yet |
| MCP server | `data_status`, `search_documents`, `get_document` over stdio or loopback HTTP | One implementation exposes tools to different clients |
| Chatbot | Calls tools and generates its answer outside this repo | Retrieval and generation are separate steps |

Verified locally on November 6: 16 unit tests, both MCP transport smoke checks,
and ingestion in all three modes. Corpus outputs were 3,274 page records, 7,128
default window records, and 273 document records. These are snapshot counts, not
a quality score. Actual ChatGPT connection, generated answers, other client
connections, Windows setup and classroom timing remain to be rehearsed.

The project can demonstrate retrieval-augmented generation with keyword retrieval.
Do not describe it as vector search, embedding search, model training, automatic
fact verification, or a complete/current agricultural advisory service.

## Outcomes participants can demonstrate

1. Point to ingestion, retrieval, MCP and answer generation in one architecture.
2. Ask the setup agent to run ingestion and explain one record's source/page metadata.
3. Observe a real MCP tool call and verify a claim against returned/source text.
4. Compare one fixed query across chunking modes and explain the difference.
5. Recognize an unsupported request and name the evidence still needed.

## Run of show — exactly 120 minutes

Roles below are proposed: Grady leads the story, framing and discussion; Hayden
drives the technical demonstrations. The other presenter assists participants.

| Minutes | Length | Lead | Screen / slides | Participant action | Checkpoint |
| --- | ---: | --- | --- | --- | --- |
| 0–8 | 8 | Grady + Hayden | 1–2; prepared ChatGPT demo | Inspect one cited answer and the actual tool result | Name where the evidence came from |
| 8–20 | 12 | Grady | 3–5; architecture, corpus, client routes | Trace a question through the system | Distinguish retrieval from generation |
| 20–35 | 15 | Hayden | 6; one setup prompt and the agent report | Ask the local agent to run the prepared script; join a pair if needed | Data loaded; local checks pass |
| 35–50 | 15 | Hayden | 7; setup report, client and one record | Let the agent help connect the client; inspect actual tool calls and metadata | Tools connected in the actual client |
| 50–65 | 15 | Grady + Hayden | 8–9; ChatGPT and original source | Ask the climate question, inspect search/read calls, verify the answer | Answer supported by the cited source |
| 65–70 | 5 | Both | 10 | Short pause; helpers recover stalled pairs | Ready to compare retrieval |
| 70–90 | 20 | Hayden | 11–12; fixed-query chunking lab | Predict, ask the setup agent to change mode, repeat the same query and compare | One observation with evidence; restore page mode |
| 90–102 | 12 | Both | 13–14; three small code excerpts | Identify what turns retrieval into a callable tool | Explain one wrapper and one ranking rule |
| 102–112 | 10 | Grady | 15; pair challenge | Try a paraphrase and an unsupported forecast; review claims | Correct uncertainty and source support |
| 112–120 | 8 | Both | 16; adaptation and questions | Name a personal data source and the required changes | Runnable takeaway and next step |

The code budget is 15 minutes total: up to 3 minutes during ingestion and 12
minutes in the code tour. Slides anchor the explanation; most exercise time is
spent with the setup agent, question-answering client and source material. A prepared baseline runs from
the beginning. Attendees do not implement the complete server during the session.

## The explanation boundary

Show `records_for()` only to connect one source page to one record. Show the
small `@server.tool` search wrapper and two ranking lines in `RecordStore.search()`.
The questions to answer are: what goes in, what comes out, and what decides the
result? Keep regex parsing, CORS internals, packaging, locks, atomic writes,
window-scanning internals and authentication implementation in the annotated repo
for independent exploration. Explain their purpose only if needed for recovery.

Do not spend the extra 30 minutes on more infrastructure. The additional time
supports a measured chunking experiment, a pause, participant discussion and
setup recovery.

## Preparation and recovery

Before class, distribute the repo and a tested local-agent/client route. Install
and sign in to the local agent, make Python/uv available, and resolve private-repo
access and chatbot/cloud-to-local permissions during prework. The local agent
must be able to read the repo and run commands. A browser-only chat without local
tools is not that setup environment.

The attendee pastes the single prompt in [AGENT_SETUP.md](AGENT_SETUP.md). The
agent runs the fixed `setup-workshop.py`, diagnoses environment failures, and
helps connect the selected client. It uses our existing implementation rather
than generating a replacement. Attendees complete sign-ins and permission choices.
Use the same script as a one-command fallback; do not require an unprepared
attendee to install/authenticate another agent during the room's setup window.

Three visible checkpoints define success:

1. **Data loaded:** actual export path/count and one source-linked record.
2. **Tools connected:** the actual selected client discovers and calls the tools.
3. **Answer supported:** a generated claim is checked against the source text.

The script can verify local data and protocol behavior. It must leave the last
two checkpoints pending until the actual client and answer are observed. The
fixed-query comparison and page-mode restore are the later exercise checkpoint.

At minute 35, move unresolved setups into pairs. Allow at most two minutes of
projected debugging at any one failure. Use the saved retrieval snapshot if
network/model access fails; label it as recorded tool output. It is not a saved
ChatGPT answer. A separate successful ChatGPT recording should be captured during
rehearsal. Keep the 5-minute pause and final questions; shorten the optional
whole-document comparison or skip a code excerpt if behind.

## Presenter materials

- [Agent setup prompt and procedure](AGENT_SETUP.md)
- [Slide script and speaker notes](SLIDE_SCRIPT.md)
- [Participant exercises](EXERCISES.md)
- [Client connection and ChatGPT preflight](CLIENT_SETUP.md)
- [Weekend rehearsal checklist](REHEARSAL.md)
- [Verified retrieval snapshot](retrieval-snapshot.json)

## Open rehearsal decisions

ChatGPT is the presenter client; record the actual selected model during
rehearsal. Verify custom-MCP/tunnel permissions on the target workspace. Pick one
local setup-agent route and one local-client fallback; test both before advertising support.
Confirm audience size, laptop restrictions, distribution access and projector
readability. No universal/free-account compatibility promise is made.

The weekend is Saturday November 7 and Sunday November 8, 2026. See the rehearsal
checklist for a technical pass, a handoff pass and a full two-hour practice run.
