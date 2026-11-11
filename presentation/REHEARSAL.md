# Weekend rehearsal checklist

Practice weekend: Saturday November 7 and Sunday November 8, 2026.
Roles are proposed: Grady leads framing/discussion, Hayden drives ingestion and
MCP demonstrations; swap if a handoff works better. Use a visible stopwatch.

## Saturday — technical pass (45 minutes suggested)

- [ ] Both presenters pull the same revision and open the repo in a local agent.
- [ ] Rehearse the exact [setup prompt](AGENT_SETUP.md) from a fresh environment.
      Confirm the fixed script completes and the agent explains its report.
- [ ] Confirm the workshop distribution route. The GitHub repo is currently private;
      attendees need access or an approved copy before class.
- [ ] Confirm the setup script runs the tests, both protocol checks and page ingestion.
      Local success must not be labeled an actual chatbot connection.
- [ ] Run `uv run python presentation/check_demo.py` and compare the summary with
      `retrieval-snapshot.json`; record the checked revision.
- [ ] Ask the agent to show a source-linked record; inspect `MF3334-p2` against the source.
- [ ] Complete [ChatGPT preflight](CLIENT_SETUP.md) on the actual presenter account.
      Record model name, workspace, connection route, tool discovery and first answer.
- [ ] Test one local alternative (Claude Desktop or Gemini CLI, whichever the
      presenters can support) with the same source question.
- [ ] Test projector readability and switching between slides, the local setup
      agent, ChatGPT tool details and local source text. Keep a terminal available
      for presenter recovery, rather than making it the attendee workflow.
- [ ] Capture a successful ChatGPT interaction. Keep a labeled retrieval-only
      snapshot too; neither should be presented as a current live result.

Any unfinished account/connection item is a real readiness gap. Resolve it
before inviting attendees to follow that route. No tunnel setup was performed
by the materials-authoring pass.

## Saturday — handoff pass (45–60 minutes suggested)

Walk through the setup prompt, agent reports, slide transitions and exercises once without waiting
for a real audience. Practice these spoken handoffs:

- Grady: “We have the evidence path. Hayden will show how one source becomes a record.”
- Hayden: “The export is ready. Grady will ask the same question through ChatGPT.”
- Grady: “We can see the source. Now predict what changing the chunk will do.”
- Hayden: “The result changed for an inspectable reason. Let's find those few lines.”

Prepare windows in order: deck, local setup agent, ChatGPT, `MF3334.md`. Keep
the terminal/commands as presenter recovery references. Practice asking the
setup agent to change the chunking mode, then inspect new calls in ChatGPT. Start with page mode and restore
it after every rehearsal. Practice a no-network fallback and a missing-data case.

## Sunday — full 120-minute practice plus 20-minute debrief

Run the timeline in [RUN_OF_SHOW.md](RUN_OF_SHOW.md) at full duration. Simulate
questions and working time; do not skip those periods and conclude it fits.
Have one presenter act as a stalled attendee during setup, then switch roles.

| Checkpoint | Planned minute | Actual minute | Change for next run |
| --- | ---: | --- | --- |
| Opening demo ends | 8 | | |
| Architecture/client explanation ends | 20 | | |
| Data-loaded checkpoint; move to pairs if needed | 35 | | |
| Actual tools-connected checkpoint | 50 | | |
| Answer-supported checkpoint | 65 | | |
| Return from pause | 70 | | |
| Chunking comparison done; page mode restored | 90 | | |
| Code tour ends | 102 | | |
| Pair challenge ends | 112 | | |
| Session ends | 120 | | |

Debrief three questions: Where did an attendee need an unexplained term? Which
step took longer than its budget? Which claim lacked visible evidence? Revise
wording or shorten content before adding another feature.

## Recovery rules to practice

- A projected failure gets at most two minutes. The assisting presenter helps
  privately; the room continues on a prepared pair or recorded trace.
- If tool discovery works but search fails, inspect export path and ingestion
  status before investigating the language model.
- If a cloud client cannot connect, use the prepared fallback. A CORS change
  does not make localhost reachable from the provider's cloud.
- If behind by minute 80, skip whole-document mode and compare page/window only.
- If behind at minute 90, show the tool wrapper and ranking rule; omit the rest
  of the code. Keep final source checking and questions.
- Ask the setup agent to restore page mode; the presenter command reference is
  `uv run rag-ingest --mode page`. IDs/offsets from other modes must be searched again.
- If an attendee has no local agent ready, use the one-command fallback or a
  prepared pair. Do not spend class installing another agent/account.
- A setup agent should use the existing script and explain a blocked step,
  rather than rewriting the server, changing requirements or claiming success.

## Before calling the session ready

- [ ] Actual ChatGPT connection and answer inspected; recording saved.
- [ ] One alternative client verified, or its support claim explicitly deferred.
- [ ] Fresh-laptop run completed, including Windows if advertised.
- [ ] A person who did not build the repo can follow the single setup prompt
      and identify evidence for all three checkpoints.
- [ ] One-command fallback verified without relying on a coding agent.
- [ ] A person who did not build the repo can follow the participant exercises.
- [ ] Private repo access/distribution and attendee prework are resolved.
- [ ] Two-hour rehearsal fits with the pause and questions intact.
- [ ] No slide implies embeddings, universal client access, or current crop advice.

## Verification already completed November 6

At revision `70695d5`, all 16 automated tests and both stdio/HTTP smoke checks
passed. Direct retrieval was exercised in all three chunking modes and the
snapshot was saved. Those checks do not validate ChatGPT, Claude or Gemini UI
connections, classroom timing or generated-answer support.
