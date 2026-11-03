# Workshop corpus: K-State Research and Extension crop publications

A fixed snapshot of 273 public crop publications from the
[K-State Research and Extension (KSRE) Bookstore](https://bookstore.ksre.ksu.edu/),
converted from PDF to plain text. Everyone in the workshop searches the same
files, so results are reproducible and nobody needs to reach the KSRE site.

This folder is source material, not an ingestion export. An ingestion step reads
`docs/` and publishes records for the server to `data/documents.jsonl`
(see the [data contract](../README.md#data-contract)).

## What is here

| Path | What it holds |
| --- | --- |
| `docs/<ID>.md` | One publication per file, named by its KSRE publication number |
| `manifest.jsonl` | One line per publication found, including the 12 excluded as stubs |
| `fetch_ksre.py` | The facilitator script that produced this snapshot |

Each document starts with a header between `---` lines. Every value is JSON:

| Field | Meaning |
| --- | --- |
| `id` | KSRE publication number, such as `MF991` or `SRP1193` |
| `title` | Publication title as listed in the bookstore |
| `authors` | Listed authors; may be empty |
| `published` / `revised` | Dates from the bookstore listing, such as `Aug 2025`; `revised` may be empty |
| `topics` | Bookstore crop topics that list this publication |
| `source_url` | The publication's bookstore page |
| `credit` | Attribution to keep with any reuse |
| `license_note` | KSRE's reproduction statement |

The body follows the header. `<!-- page N -->` marks where each PDF page starts,
so an answer can cite a page as well as a publication.

## Snapshot

- Captured 2026-11-02 from 12 bookstore crop topics: wheat, sorghum, corn,
  soybeans, canola, sunflower, alfalfa, forages, pests, various, other, cotton.
- 285 publications listed; 273 kept. The 12 excluded (`status: "stub"` in the
  manifest) had no usable text: eleven annual weed-control reports whose download
  is a cover page only, and one product listing.
- About 3,300 PDF pages and 9.5 MB of text. A few publications are Spanish or
  French translations of English ones.

Text comes from `pypdf` in reading order. Tables keep their numbers but lose
their visual layout and column alignment. That is how the PDFs extract, not a
cleanup step that was skipped.

## Use and credit

KSRE publications state: "Contents of this publication may be freely reproduced
for educational purposes. All other rights reserved." Keep each document's
`credit` line with any excerpt. Crop performance reports add their own condition
for tables: reproduce a table in its entirety, reference the source, and do not
manipulate or reinterpret the data.

This snapshot is for the workshop's educational use. It is not KSRE's current
guidance; check the bookstore for the latest version of any publication.

## Regenerate

Facilitators only. The script makes about 600 requests, pausing between them
because the site rate-limits, so a full run takes 40–60 minutes.

```sh
uv run corpus/fetch_ksre.py                  # all default topics
uv run corpus/fetch_ksre.py --topics wheat   # one topic
uv run corpus/fetch_ksre.py --list-only      # manifest only, no PDFs
```

The script declares its own dependency (`pypdf`) inline, so it does not change
the project's requirements. Downloaded PDFs are cached in `corpus/.pdf-cache/`,
which Git ignores. A new run produces a different snapshot if KSRE has published
or revised anything.
