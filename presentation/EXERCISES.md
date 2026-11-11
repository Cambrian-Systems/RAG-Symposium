# Participant exercises

Use the committed snapshot reviewed at `70695d5`. Work in pairs if setup is
incomplete. These are source-research exercises; no farming background is needed.
The aim is to inspect evidence, not make current crop-management recommendations.

## Before class

Obtain the repo and open it in a prepared local coding agent. Install/sign in to
that agent, make Python/uv available, and prepare your intended chatbot connection
using [the client guide](CLIENT_SETUP.md). The setup agent needs local file and
command access. You may use a different chatbot for the source questions.

No prepared local agent? Use the one-command fallback in
[AGENT_SETUP.md](AGENT_SETUP.md), or join a prepared pair. Account permissions
and cloud connection provisioning should be resolved during prework.

## 1. Ask your agent to prepare the project — minutes 20–35

Paste this once into your **local setup agent**, with the repo open:

> Read presentation/AGENT_SETUP.md and set up this repo on my computer. Run the
> prepared setup script, help connect my selected MCP client, and report evidence
> for three checkpoints: data loaded, tools connected, and answer supported.

Read the agent's report. Which steps did it actually verify? The fixed script
runs the existing checks and builds the page export. On the reviewed snapshot,
**data loaded** means 3,274 source-linked records from 273 publications. The
script's temporary test servers stop afterward; the chosen client still needs
its actual connection.

Let the agent explain any failure and ask a presenter if it remains unresolved.
At minute 35, join a working pair so you can continue the evidence exercises.
Do not ask the agent to build a replacement project to get past setup.

## 2. Confirm tools connected and inspect evidence — minutes 35–65

Have the setup agent help configure your prepared connection route. Complete
any sign-in/permission choices yourself. In the **question-answering client**,
confirm `data_status`, `search_documents` and `get_document` are available. Ask
it to call `data_status`, then search/read a record. Seeing those actual calls
establishes **tools connected**. A successful local test alone does not.

The setup agent can show one export record and explain its source/page metadata.
Ingestion prepares records locally; it does not train the model. The next check
is whether the question-answering chatbot uses that evidence correctly.

Use this explicit first prompt so we can inspect one known path:

> Use only our RAG-Symposium connection. Call data_status, then
> search_documents with query "frost free season western central eastern climate
> 1895 2015" and limit 3. Read MF3334-p2 with get_document. What historical
> average frost-free season lengths does the supplied publication report for
> western, central and eastern Kansas? Cite the record, page and original source.
> Describe the figures as historical averages, not a forecast.

Find the matching passage in [MF3334](../corpus/docs/MF3334.md), under page 2.
Open the original source linked in the result if needed; the local text is
available without the source website. Record:

| What to record | Your observation |
| --- | --- |
| Ingested mode / record count | |
| Search query actually sent | |
| Returned record and publication ID | |
| PDF page metadata | |
| Claim supported by the source | |
| A limitation of that claim | |

**Answer-supported checkpoint — self-check after inspecting:** page 2 reports 170, 182 and 189 days for western,
central and eastern Kansas. The publication is from April 2017. These are historical
regional averages; they do not predict the next frost on a particular farm.
The chatbot can word its answer differently, but each number and qualification
must agree with the source. A plausible citation alone does not earn credit.

## 3. Compare chunking — minutes 70–90

First predict which mode will put the clearest evidence in the top three results.
Use exactly this shorter tool query for every comparison:

```json
{"query":"frost free season western central eastern","limit":3}
```

1. Begin in page mode. Ask the question-answering chatbot to call
   `search_documents` with exactly that input. Save the top three IDs, source
   pages and a short description of the excerpts.
2. Ask the **local setup agent**:

   > Use the existing ingestion command to switch this workshop export to default
   > window mode. Keep the implementation and dependencies unchanged. Report the
   > actual record count when it finishes.

3. In a fresh conversation (or with explicitly requested new status/search
   calls), have the question-answering chatbot send the **same tool query** and
   limit. Record the new IDs/pages. Window defaults are 1,500 characters with
   approximately 200 shared; these are characters, not model tokens.
4. If time permits, ask the setup agent to switch the export to whole-document
   mode, then repeat that same search. This comparison is optional.
5. Finish by asking the local setup agent:

   > Restore the workshop export to page mode using the existing ingestion command.
   > Report the result so I can confirm the shared baseline is back.

The setup agent runs ingestion; the question-answering chatbot reads the results
through MCP. They may be different applications. Exact command references are
in [the agent guide](AGENT_SETUP.md#changing-chunking-later).

| Mode | Top three record IDs | Relevant evidence visible? | One benefit / one cost |
| --- | --- | --- | --- |
| Page | | | |
| Window | | | |
| Whole document (optional) | | | |

The server rereads the export. IDs and offsets change across modes: use the
new search results, not a cached record ID. Do not refresh tools merely because
data changed; tool refresh is needed when descriptions/schemas change.

**Observed on the reviewed revision:** page: `L514-p2`, `MF3334-p2`, `MF3018-p6`;
window: `MF3334-w2`, `MF3334-w3`, `MF3066-w3`; document: `C449`, `C529`, `C560`.
Several whole documents contain all query words and tie; ID breaks ties. A higher
record count or a different first result is not automatically better retrieval.
These are deterministic retrieval observations, not scores for generated answers.

## 4. Pair challenge — minutes 102–112

**Paraphrase:** search for `days crops can grow west middle east Kansas`.
Compare with the source-language query above. Did the actual tool input preserve
your wording, or did the chatbot rewrite it? Inspect the results before judging.
Then refine to `climate frost season western central eastern` and compare.

**Unsupported request:** ask, “Using only these publications, what exact date
will the first frost occur on my field next autumn?” A supported response explains
that historical regional averages do not establish that date and identifies the
missing current/local evidence. Relevant retrieved text may still be insufficient.

Score one answer together, one point per check:

- It used the requested connection and an observed tool result.
- It found and read the relevant source text.
- Its substantive claims match the source and include a record/page reference.
- It states the boundary of the evidence without inventing a field-specific forecast.

If the client/model correctly refuses immediately, that is a successful result.
No exercise depends on making a model hallucinate on cue.

## Take it home

Choose a personal document source. Identify the extraction step, stable IDs,
source/page metadata and connection route you would need. Keep the same MCP tool
interface while changing the ingestion/retrieval behind it. Use the annotated
source and tests to explore implementation after the workshop.
