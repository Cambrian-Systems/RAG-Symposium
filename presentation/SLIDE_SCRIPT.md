# Rehearsal slide script

16 main slides plus 2 optional appendix slides. Main slides show agent prompts and evidence checkpoints. Terminal commands are agent/presenter references in the notes and setup guide. The same notes are embedded in the live deck.

## 1. Build a retrieval tool your chatbot can use

**Time:** 0–2 · **Lead:** Grady

**On screen**

- Local ingestion · MCP · evidence you can inspect
- Grady Burns and Hayden Thatcher
- Two-hour hands-on workshop

**Speaker notes**

Time: 0–2. Lead: Grady.

Say: “Today a local coding agent will prepare the project for us. We will check what it accomplished, connect our chatbot to the evidence, and inspect an answer.” The baseline code already exists. Participants paste one prepared setup prompt and make one controlled retrieval change with the agent. The local agent must be installed/signed in during prework. A separate chatbot can ask the document questions. ChatGPT is the presenter client and its account/tunnel route must be rehearsed. Move into the prepared evidence demo promptly; no installation in the opening.

Sources: https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/README.md ; local guide: presentation/AGENT_SETUP.md

## 2. An answer with visible evidence

**Time:** 2–8 · **Lead:** Grady + Hayden

**On screen**

- Watch the tool call
- Open the supporting source
- Check one claim yourself

**Speaker notes**

Time: 2–8. Lead: Grady + Hayden.

Do: use the prepared ChatGPT connection and the exact first prompt in EXERCISES.md. Show data_status, the search result, and get_document for MF3334-p2. Expand the tool details. Ask: “Which part of this claim can you verify on the page?” A baseline answer without retrieval may correctly say it does not know; no hallucination is required. Capture a successful actual ChatGPT run during rehearsal. Allow two minutes for projected recovery, then use the labeled backup. Transition: “Now let’s identify which part did each job.”

Sources: https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/corpus/docs/MF3334.md ; https://developers.openai.com/api/docs/guides/custom-mcp-server

## 3. The evidence path

**Time:** 8–13 · **Lead:** Grady

**On screen**

- Documents → ingestion → local records
- Chatbot ⇄ MCP tools ⇄ retrieval
- Retrieved text → chatbot → cited answer

**Speaker notes**

Time: 8–13. Lead: Grady.

Say: “Ingestion prepares the records. Retrieval selects evidence at question time. MCP exposes functions the chatbot can call. The model writes the answer.” These are roles, not four separate servers. The same local process contains the tool wrappers and record adapter. The current retrieval is keyword-based. RAG does not require that retrieval use embeddings; semantic retrieval is a later extension. Ask a participant to trace where the source text enters the answer.

Sources: https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/src/rag_symposium/ingest.py ; https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/src/rag_symposium/server.py ; https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/src/rag_symposium/store.py

## 4. The shared publication snapshot

**Time:** 13–16 · **Lead:** Hayden

**On screen**

- 273 K-State crop publications
- Original source, page and date metadata
- Historical documents for source research

**Speaker notes**

Time: 13–16. Lead: Hayden.

Show corpus/docs/MF3334.md: the small JSON-valued header and PDF page markers. This committed snapshot was captured November 2; ingestion uses local text, so the room does not scrape or download PDFs. Explain that PDF extraction can lose table layout. We focus on an easily inspected prose passage rather than a complex table or current farming recommendation. Keep attribution with reused excerpts. Do not claim the snapshot is complete or current guidance.

Sources: https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/corpus/README.md ; https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/corpus/docs/MF3334.md

## 5. Your setup agent and your chatbot

**Time:** 16–20 · **Lead:** Grady

**On screen**

- Local setup agent → prepares the project on your laptop
- Question-answering chatbot → calls the retrieval tools
- They can be different applications

**Speaker notes**

Time: 16–20. Lead: Grady.

Explain the two roles explicitly. The local coding agent can read the repo, run the prepared setup script, diagnose an environment failure and help configure a client. The question-answering chatbot uses MCP to search/read evidence and generate an answer. They may be different applications. Browser-only chat does not automatically provide local command access. ChatGPT’s presenter connection still uses its rehearsed private route; the setup prompt cannot create account permissions. Claude Desktop local configuration and Gemini CLI remain alternative routes to test. Use the same tool names; keep cloud authentication/prework out of the live setup window.

Sources: https://developers.openai.com/api/docs/guides/secure-mcp-tunnels ; https://developers.openai.com/api/docs/guides/custom-mcp-server ; https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp ; https://geminicli.com/docs/tools/mcp-server/ ; local guide: presentation/AGENT_SETUP.md

## 6. One prompt for your setup agent

**Time:** 20–35 · **Lead:** Hayden

**On screen**

- Read presentation/AGENT_SETUP.md and set up this repo on my computer.
- Use the prepared setup script
- Report: data loaded · tools connected · answer supported

**Speaker notes**

Time: 20–35. Lead: Hayden.

Participants copy the complete single prompt from EXERCISES.md into their prepared local agent: “Read presentation/AGENT_SETUP.md and set up this repo on my computer. Run the prepared setup script, help connect my selected MCP client, and report evidence for three checkpoints: data loaded, tools connected, and answer supported.” The agent runs setup-workshop.py, uses existing diagnostics and explains failures. Keep the slide on the prompt and the agent’s short report; show terminal output only for recovery. The fixed script installs locked dependencies, runs existing unit/protocol checks, ingests page records and verifies a source-linked read. It does not start a persistent client connection. A local test pass must not be reported as a verified chatbot connection. The one-command fallback is “uv run python setup-workshop.py” after Python/uv prework. If the local agent is not ready, use that fallback or a prepared pair. At minute 35, move unresolved setups into pairs.

Sources: https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/tests/mcp_smoke.py ; https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/tests/http_smoke.py ; local guide: presentation/AGENT_SETUP.md

## 7. Three visible checkpoints

**Time:** 35–50 · **Lead:** Hayden

**On screen**

- Data loaded: source-linked records on your laptop
- Tools connected: actual calls in your chosen client
- Answer supported: a claim checked against its source

**Speaker notes**

Time: 35–50. Lead: Hayden.

Read the setup report together. Data loaded means the export was read successfully; the reviewed page snapshot has 3,274 records from 273 publications. Tools connected means the selected actual client discovers data_status, search_documents and get_document and calls them successfully. The setup agent helps merge the existing client configuration; the attendee completes sign-ins and permission choices. Keep the answer-supported checkpoint pending until the next source-question exercise. Show one source/page record and, for up to three minutes, ask the setup agent to locate records_for() and explain how a source page becomes a record. Do not walk through parsing internals. The fixed script rebuilds only the generated default export, not the server implementation.

Sources: https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/src/rag_symposium/ingest.py ; local guide: presentation/AGENT_SETUP.md

## 8. The first source question

**Time:** 50–58 · **Lead:** Grady + Hayden

**On screen**

- Historical frost-free season lengths
- Western, central and eastern Kansas
- Search, read, then cite the source

**Speaker notes**

Time: 50–58. Lead: Grady + Hayden.

Use only the RAG-Symposium connection. Request data_status, then search_documents with query “frost free season western central eastern climate 1895 2015” and limit 3. Read MF3334-p2 with get_document. Ask which historical averages the supplied publication reports. The specific query is a provided recovery path, not evidence of general retrieval accuracy. Inspect the actual query the model sent: it may otherwise rewrite it. Require the record ID, page and original source. Keep the answer grounded in the historical publication.

Sources: https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/corpus/docs/MF3334.md ; https://bookstore.ksre.ksu.edu/item/temperature-trends-and-changes-in-frost-dates-from-1895-to-2015-kansas-climate-basics_MF3334

## 9. Check the source

**Time:** 58–65 · **Lead:** Grady

**On screen**

| Region | Historical average |
| --- | --- |
| Western Kansas | 170 days |
| Central Kansas | 182 days |
| Eastern Kansas | 189 days |

**Speaker notes**

Time: 58–65. Lead: Grady.

These figures are read from the source, not a fabricated ChatGPT transcript. Show MF3334 page 2 and ask the room to verify each value. Then ask what cannot be inferred: the exact next frost at a particular field. The text reports historical regional averages and notes changing conditions. Record publication April 2017 and the source reference. A citation’s existence is not enough; it must support the attached claim. Have pairs complete the evidence worksheet.

Sources: https://bookstore.ksre.ksu.edu/item/temperature-trends-and-changes-in-frost-dates-from-1895-to-2015-kansas-climate-basics_MF3334 ; https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/corpus/docs/MF3334.md

## 10. Five-minute pause

**Time:** 65–70 · **Lead:** Both

**On screen**

- Return at minute 70
- Stretch, compare notes, ask a helper
- Next: compare the same query across chunks

**Speaker notes**

Time: 65–70. Lead: Both.

Keep this pause. Use it for a short stretch and private setup help. Before resuming, confirm pairs have page ingestion and at least one working way to inspect tool results. Do not spend the pause adding new infrastructure.

Sources: https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/README.md

## 11. Ask the agent to change the chunks

**Time:** 70–83 · **Lead:** Hayden

**On screen**

- Ask the setup agent to switch to window mode
- Repeat the same search; inspect what changed
- Ask the setup agent to restore page mode

**Speaker notes**

Time: 70–83. Lead: Hayden.

First predict the result, then save page-mode outputs for exactly “frost free season western central eastern”, limit 3. Ask the local setup agent to use the existing ingestion command to switch to default windows, keeping the implementation/dependencies unchanged. In the question-answering client request fresh status/search calls with exactly the same query/limit. These may be two applications: the local agent changes the export; the chatbot reads it through MCP. Compare IDs, page spans, excerpts and context. Whole-document mode is optional. Always ask the local agent to restore page mode and report completion. IDs/offsets change with mode, so use fresh results. Command references for agent/presenter only: “uv run rag-ingest --mode window”; optional “uv run rag-ingest --mode document”; restore “uv run rag-ingest --mode page”.

Sources: https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/src/rag_symposium/ingest.py ; https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/src/rag_symposium/store.py ; local guide: presentation/AGENT_SETUP.md

## 12. Observed fixed-query results

**Time:** 83–90 · **Lead:** Hayden + Grady

**On screen**

| Mode | Records | First result |
| --- | --- | --- |
| Page | 3,274 | L514-p2 |
| Window | 7,128 | MF3334-w2 |
| Document | 273 | C449 |

**Speaker notes**

Time: 83–90. Lead: Hayden + Grady.

These results were actually observed at revision 70695d5 on November 6, 2026, for the fixed shorter query and limit 3. Source file: presentation/retrieval-snapshot.json. In whole-document mode, several large documents contain all terms and tie; ID ordering breaks the tie. Windows surface the climate publication first in this case, but can duplicate evidence and cross page boundaries. Do not call any mode universally best or interpret counts as quality scores. Ask one pair to explain a benefit and a cost using its results. Confirm page mode is restored.

Sources: https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/src/rag_symposium/store.py ; local rehearsal snapshot: presentation/retrieval-snapshot.json

## 13. A retrieval function becomes a tool

**Time:** 90–96 · **Lead:** Hayden

**On screen**

```python
@server.tool(annotations=read_only)
def search_documents(query: str, limit: int = 5) -> dict:
    return store.search(query, limit)
```

Name + input types + description → discoverable tool

**Speaker notes**

Time: 90–96. Lead: Hayden.

Ask the setup agent to open the existing search_documents wrapper and explain what goes in and what comes out. The on-screen excerpt omits the docstring to fit; show its purpose in the full function. Explain only the decorator, input types and returned evidence. The wrapper delegates retrieval to RecordStore; the language model is outside this server. Ask participants whether changing the store requires changing the tool name. Keep the interface stable if its contract is unchanged. Do not ask the agent to rewrite the wrapper as a setup exercise. Spend six minutes here and keep low-level configuration in the self-guided material.

Sources: https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/src/rag_symposium/server.py ; local guide: presentation/AGENT_SETUP.md

## 14. What decides the search order

**Time:** 96–102 · **Lead:** Hayden + Grady

**On screen**

```python
matched = terms & words
ranked.sort(key=lambda pair:
    (-len(pair[1]), pair[0]["id"]))
```

Distinct word matches first; record ID breaks ties

**Speaker notes**

Time: 96–102. Lead: Hayden + Grady.

Have the local agent locate the existing ranking lines and explain one rule in plain language, then ask a participant to restate it. These excerpts are not a complete standalone function. Set intersection finds words present in both question and record. More distinct matches rank first; ID breaks ties. This explains synonym misses and long-document ties observed in the chunking exercise. The matched_terms field explains ranking, not confidence in an answer. Embeddings remain a possible later extension. The agent helps navigate code; the participant still inspects the evidence and explains the result. End the code tour at minute 102.

Sources: https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/src/rag_symposium/store.py ; local guide: presentation/AGENT_SETUP.md

## 15. Challenge: language and missing evidence

**Time:** 102–112 · **Lead:** Grady

**On screen**

- Paraphrase: “days crops can grow west middle east Kansas”
- Ask: “What exact date will my field frost next autumn?”
- Inspect the source, claims and uncertainty

**Speaker notes**

Time: 102–112. Lead: Grady.

In pairs, run the paraphrase as an exact tool query and compare with “climate frost season western central eastern.” Inspect whether the model changed the query. Then ask the unsupported field-specific forecast using only the corpus. A good answer distinguishes historical averages from that prediction and identifies missing evidence. A correct immediate refusal is successful; do not rely on a hallucination. Score tool use, source read, supported claims/citation, and appropriate uncertainty: one point each. This is a teaching rubric, not a measured accuracy statistic.

Sources: https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/corpus/docs/MF3334.md ; https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/src/rag_symposium/store.py

## 16. Your next data source

**Time:** 112–120 · **Lead:** Both

**On screen**

- Identify extraction and source metadata
- Keep the same tools; improve retrieval behind them
- Explore the annotated repo and tests
- Questions

**Speaker notes**

Time: 112–120. Lead: Both.

Ask participants to name one dataset of their own and the extraction, IDs and source metadata it would need. Bring the conversation back to the evidence path. Remind them the chatbot/client and model remain outside this server. The supplied code and guide are take-home resources; the core outcome is a runnable connection plus the ability to inspect and improve evidence. Leave the final minutes for questions. Do not use this segment to start another provider integration.

Sources: https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/README.md

## 17. Appendix: ChatGPT connection preflight

**Time:** Appendix only · **Lead:** Hayden

**On screen**

- Have the local agent prepare the existing server
- Complete your account’s private connection prework
- Observe actual ChatGPT tool calls and check one claim

**Speaker notes**

Time: Appendix only. Lead: Hayden.

Use AGENT_SETUP.md and CLIENT_SETUP.md before rehearsal. The local agent runs the fixed setup script, starts the existing HTTP launcher and helps with the documented connection route. The attendee completes account sign-ins, permissions and credential entry. A Platform tunnel and ChatGPT custom-MCP access are separate prerequisites. Local protocol checks cannot establish either. After connection, observe discovery and actual status/search/read calls, then inspect one generated claim. Keep an honest pending/blocked report when a required UI or permission is unavailable. Command references remain in the agent/client guides. The loopback server should not be exposed publicly as-is.

Sources: https://developers.openai.com/api/docs/guides/secure-mcp-tunnels ; https://developers.openai.com/api/docs/guides/custom-mcp-server ; local guide: presentation/AGENT_SETUP.md

## 18. Appendix: recovery checkpoints

**Time:** Appendix only · **Lead:** Both

**On screen**

- Data not loaded → ask the agent to inspect its report
- Tools not connected → inspect the chosen client route
- No local agent ready → one-command fallback or a pair
- Two-minute projected-debugging limit

**Speaker notes**

Time: Appendix only. Lead: Both.

The recovery path is to inspect the failed checkpoint, not regenerate the project. For data, use the setup report and ask the agent to check export path/mode. For the client, inspect actual discovery/calls and the prepared route; CORS does not make localhost reachable from a provider’s cloud. With no prepared local agent, the one-command fallback is “uv run python setup-workshop.py”, followed by prepared client setup or pairing. A saved retrieval snapshot is recorded tool output, not a live ChatGPT answer. Ask the setup agent to restore page mode before new exercises. Skip the optional whole-document comparison if behind, keep the pause and questions, and limit projected debugging to two minutes.

Sources: https://github.com/Cambrian-Systems/RAG-Symposium/blob/70695d5b05e841d0f19a7cf10298260e0fe1a42d/README.md ; local rehearsal snapshot: presentation/retrieval-snapshot.json ; local guide: presentation/AGENT_SETUP.md

