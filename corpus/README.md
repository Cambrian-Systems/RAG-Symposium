# Workshop corpus: official U.S. AI rules and guidance

A fixed snapshot of 62 official U.S. government documents about artificial
intelligence (1,847 pages, about 5.4 million characters of text), taken
2026-11-10. Everyone in the workshop searches the same files, so results are
reproducible and nobody needs to reach an agency website.

This is a teaching snapshot. It is not legal advice, and it is not a complete
or current statement of the law: documents published, revoked or changed after
2026-11-10 are not reflected, and many relevant documents are not included.

This folder is source material, not an ingestion export. `uv run rag-ingest`
reads `docs/` and publishes records for the server to `data/documents.jsonl`
(see [Ingestion](../README.md#ingestion)). Each document is one file,
`docs/<ID>.md`.

## What is in it

| Kind of document | Issuers | How many |
| --- | --- | --- |
| Executive orders | Executive Office of the President | 15 |
| Memos to federal agencies | Office of Management and Budget (OMB) | 6 |
| Standards, frameworks and drafts | National Institute of Standards and Technology (NIST) | 9 |
| Copyright reports and registration guidance | U.S. Copyright Office | 4 |
| Education rules, letters and guides | U.S. Department of Education and its offices | 9 |
| Research-funding notices | National Science Foundation, National Institutes of Health | 3 |
| Hiring and workplace guidance | EEOC, Department of Labor, Office of Personnel Management, and a joint EEOC/DOJ/FTC/CFPB statement | 5 |
| Reports to Congress and audits | Congressional Research Service (CRS), Government Accountability Office (GAO) | 6 |
| Statutes | U.S. Congress: Public Law 119-12 and 15 U.S.C. Chapter 119 | 2 |
| Plans and policy statements | The White House, White House OSTP, Federal Trade Commission | 3 |

Two things make this corpus a good retrieval test. First, the words changed:
Executive Order 14434 (September 29, 2026) tells agencies to write "Super
Intelligence" or "SI" instead of "Artificial Intelligence" or "AI", so the
newest documents, such as `ED-FR-2026-22615`, use different words than older
ones. Second, many documents are no longer in force. A revoked order or a
rescinded memo reads just as confidently as a current one; only its `status`
says otherwise.

## Document header

Each document starts with a header between `---` lines, one field per line.
Every value is JSON:

| Field | Meaning |
| --- | --- |
| `id` | Stable document ID, such as `EO-14110`, `OMB-M-24-10` or `NIST-AI-600-1` |
| `aliases` | Other ways people write the ID, such as `EO 14110` or `Executive Order 14110`; `bm25` and `hybrid` search match these |
| `title` | The document's official title |
| `issuer` | The agency or office that issued it |
| `published` / `revised` | Dates as `YYYY-MM-DD` or `YYYY-MM`; empty when the document does not give one |
| `status` | The document's standing on 2026-11-10; see [Status](#status) |
| `status_note` | One or two plain sentences explaining the status |
| `status_evidence` | Where the status comes from: a quoted sentence and its URL, or the Federal Register disposition notes |
| `replaces` / `replaced_by` | IDs of documents this one replaced, or that replaced it, when they are in the corpus or named by the evidence |
| `topics` | Broad subjects, such as `executive-order`, `federal-use`, `education`, `copyright`, `hiring` |
| `source_url` | The official page for the document (not the archive copy) |
| `credit` | Citation to keep with any excerpt |
| `license_note` | Copyright status of the text |

The body follows the header. `<!-- page N -->` marks where each page starts, so
an answer can cite a page as well as a document. Text comes from `pypdf` in
reading order. Tables keep their numbers but lose their layout and column
alignment; that is how the PDFs extract, not a cleanup step that was skipped.

Six documents are web pages rather than PDFs. A web page has no page breaks, so
its text is split at line ends into numbered sections of about 3,000 characters.
Those sections play the role of pages: `EEOC-ADA-AI-2022-p3` is the third
section of that page, not page 3 of a printed document.

## Status

Status is never guessed.

- **Executive orders:** read from the Federal Register's own disposition notes
  (for EO 14110, "Revoked by: EO 14148, January 20, 2025") when the snapshot
  was taken, 2026-11-10. The notes are copied into `status_evidence`.
- **Everything else:** set from a sentence in an official document, quoted in
  `status_evidence` with its URL. For example, OMB M-25-21
  says "This memorandum rescinds and replaces ... M-24-10", so M-24-10 is
  `rescinded` and `replaced_by` lists `OMB-M-25-21`.
- **`unknown`:** no official sentence establishing the status was found.
  `status_note` says what we could and could not confirm.

| Status | Meaning |
| --- | --- |
| `in force` | An order, memo, rule, notice or statute that had not been revoked or rescinded |
| `current` | Guidance or a standard the issuer still presents as its latest version |
| `report` | An analysis (Congressional Research Service, Government Accountability Office); not a rule, and it describes the law as of its own date |
| `draft` | A proposal or public draft; not final |
| `pre-publication` | Released by the issuer ahead of a final version |
| `superseded` | A proposal replaced by a later final version |
| `earlier edition` | A later edition of the same report is also in the corpus |
| `revoked` | An executive order revoked by a later order |
| `rescinded` | A memo or guidance withdrawn by a later document |
| `removed from agency site` | The official URL now returns "Page not found"; see below |
| `unknown` | Not established from an official source |

**Removed from agency site** means the document's official address now returns
"Page not found", which `status_evidence` quotes. That is all the corpus
records: not why it was removed, and not whether the agency still holds that
view. These texts come from Internet Archive (web.archive.org) copies of the
official files, captured while they were still published; `status_note` says
which copy was used. A few other documents also come from Internet Archive
copies because the agency site refused automated downloads; their `status_note`
says so. In every case `source_url` points at the official address.

## Use and credit

All 62 documents are works of the U.S. government and are not subject to
copyright in the United States (17 U.S.C. 105). Every header carries the same
`license_note`; no document in this snapshot has a different one. Keep each
document's `credit` line with any excerpt anyway, so readers can find the
original. Some documents quote or reproduce third-party material, which may
have its own rights.

## All documents

Grouped by issuer as each header names it, then by date.

| Issuer | ID | Title | Date | Status |\n| --- | --- | --- | --- | --- |')
for i, r in enumerate(rows):
    issuer = r['issuer'] if i == 0 or rows[i - 1]['issuer'] != r['issuer'] else ''
    print(f\"| {issuer} | \`{r['id']}\` | {r['title'].replace('|', '/')} | {r['published'] or '—'} | {r['status']} |\")
"
-->

| Issuer | ID | Title | Date | Status |
| --- | --- | --- | --- | --- |
| Congressional Research Service | `CRS-R47644` | Artificial Intelligence: Overview, Recent Advances, and Considerations for the 118th Congress | 2023-08-04 | report |
|  | `CRS-IF12426` | Generative Artificial Intelligence: Overview, Issues, and Considerations for Congress | 2025-04-02 | report |
|  | `CRS-R48555` | Regulating Artificial Intelligence: U.S. and International Approaches and Considerations for Congress | 2025-06-04 | report |
|  | `CRS-LSB10922` | Generative Artificial Intelligence and Copyright Law | 2025-07-18 | report |
| EEOC, DOJ Civil Rights Division, FTC, CFPB | `JOINT-STATEMENT-AI-ENFORCEMENT-2023` | Joint Statement on Enforcement Efforts Against Discrimination and Bias in Automated Systems | 2023-04 | unknown |
| Executive Office of the President | `EO-13859` | Maintaining American Leadership in Artificial Intelligence | 2019-02-11 | in force |
|  | `EO-13960` | Promoting the Use of Trustworthy Artificial Intelligence in the Federal Government | 2020-12-03 | in force |
|  | `EO-14110` | Safe, Secure, and Trustworthy Development and Use of Artificial Intelligence | 2023-10-30 | revoked |
|  | `EO-14141` | Advancing United States Leadership in Artificial Intelligence Infrastructure | 2025-01-14 | revoked |
|  | `EO-14148` | Initial Rescissions of Harmful Executive Orders and Actions | 2025-01-20 | in force |
|  | `EO-14179` | Removing Barriers to American Leadership in Artificial Intelligence | 2025-01-23 | in force |
|  | `EO-14277` | Advancing Artificial Intelligence Education for American Youth | 2025-04-23 | in force |
|  | `EO-14318` | Accelerating Federal Permitting of Data Center Infrastructure | 2025-07-23 | in force |
|  | `EO-14319` | Preventing Woke AI in the Federal Government | 2025-07-23 | in force |
|  | `EO-14320` | Promoting the Export of the American AI Technology Stack | 2025-07-23 | in force |
|  | `EO-14355` | Unlocking Cures for Pediatric Cancer With Artificial Intelligence | 2025-09-30 | in force |
|  | `EO-14363` | Launching the Genesis Mission | 2025-11-24 | in force |
|  | `EO-14365` | Ensuring a National Policy Framework for Artificial Intelligence | 2025-12-11 | in force |
|  | `EO-14409` | Promoting Advanced Artificial Intelligence Innovation and Security | 2026-06-02 | in force |
|  | `EO-14434` | Inaugurating the Era of Super Intelligence | 2026-09-29 | in force |
| Federal Trade Commission | `FTC-AI-POLICY-STATEMENT-2026-PROPOSED` | Policy Statement Concerning the Suppression of Accuracy in Artificial Intelligence Systems (proposed) | 2026-07-07 | draft |
| National Institute of Standards and Technology | `NIST-AI-100-1` | Artificial Intelligence Risk Management Framework (AI RMF 1.0) | 2023-01 | current |
|  | `NIST-AI-100-2E2023` | Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations (2023 edition) | 2024-01 | earlier edition |
|  | `NIST-AI-100-5` | A Plan for Global Engagement on AI Standards | 2024-07 | unknown |
|  | `NIST-AI-600-1` | Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile | 2024-07 | current |
|  | `NIST-SP-800-218A` | Secure Software Development Practices for Generative AI and Dual-Use Foundation Models: An SSDF Community Profile | 2024-07-26 | current |
|  | `NIST-AI-100-4` | Reducing Risks Posed by Synthetic Content | 2024-11 | unknown |
|  | `NIST-AI-100-2E2025` | Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations (2025 edition) | 2025-03 | unknown |
|  | `NIST-IR-8596-DRAFT` | Cybersecurity Framework Profile for Artificial Intelligence (Cyber AI Profile), Preliminary Draft | 2025-12-16 | draft |
| National Institute of Standards and Technology (U.S. AI Safety Institute) | `NIST-AI-800-1-DRAFT` | Managing Misuse Risk for Dual-Use Foundation Models (Second Public Draft) | 2025-01 | draft |
| National Institutes of Health | `NIH-NOT-OD-23-149` | The Use of Generative Artificial Intelligence Technologies is Prohibited for the NIH Peer Review Process | 2023-06-23 | in force |
|  | `NIH-NOT-OD-25-132` | Supporting Fairness and Originality in NIH Research Applications | 2025-07-17 | in force |
| Office of Management and Budget | `OMB-M-21-06` | Guidance for Regulation of Artificial Intelligence Applications | 2020-11-17 | in force |
|  | `OMB-M-24-10` | Advancing Governance, Innovation, and Risk Management for Agency Use of Artificial Intelligence | 2024-03-28 | rescinded |
|  | `OMB-M-24-18` | Advancing the Responsible Acquisition of Artificial Intelligence in Government | 2024-09-24 | rescinded |
|  | `OMB-M-25-21` | Accelerating Federal Use of AI through Innovation, Governance, and Public Trust | 2025-04-03 | in force |
|  | `OMB-M-25-22` | Driving Efficient Acquisition of Artificial Intelligence in Government | 2025-04-03 | in force |
|  | `OMB-M-26-04` | Increasing Public Trust in Artificial Intelligence Through Unbiased AI Principles | 2025-12-11 | in force |
| The White House | `WH-AI-ACTION-PLAN-2025` | Winning the Race: America's AI Action Plan | 2025-07 | current |
| U.S. Congress | `PL-119-12` | Tools to Address Known Exploitation by Immobilizing Technological Deepfakes on Websites and Networks Act (TAKE IT DOWN Act) | 2025-05-19 | in force |
| U.S. Congress (codified by Office of the Law Revision Counsel; published by GPO) | `USC-15-CH119` | 15 U.S.C. Chapter 119 — National Artificial Intelligence Initiative (codified National AI Initiative Act of 2020, Div. E of Pub. L. 116-283) | 2023 | in force |
| U.S. Copyright Office | `USCO-AI-REGISTRATION-2023` | Copyright Registration Guidance: Works Containing Material Generated by Artificial Intelligence | 2023-03-16 | unknown |
|  | `USCO-AI-PART-1` | Copyright and Artificial Intelligence, Part 1: Digital Replicas | 2024-07 | current |
|  | `USCO-AI-PART-2` | Copyright and Artificial Intelligence, Part 2: Copyrightability | 2025-01 | current |
|  | `USCO-AI-PART-3` | Copyright and Artificial Intelligence, Part 3: Generative AI Training (pre-publication version) | 2025-05 | pre-publication |
| U.S. Department of Education | `ED-FR-2025-13650` | Proposed Priority and Definitions-Secretary's Supplemental Priority and Definitions on Advancing Artificial Intelligence in Education | 2025-07-21 | superseded |
|  | `ED-FR-2026-07087` | Final Priority and Definitions-Secretary's Supplemental Priority and Definitions on Advancing Artificial Intelligence in Education | 2026-04-13 | in force |
|  | `ED-FR-2026-22615` | Proposed Priorities and Definitions-Secretary's Supplemental Priorities and Definitions | 2026-11-05 | draft |
| U.S. Department of Education, Office for Civil Rights | `ED-OCR-AI-2024` | Avoiding the Discriminatory Use of Artificial Intelligence | 2024-11 | unknown |
| U.S. Department of Education, Office of Educational Technology | `ED-OET-AI-REPORT-2023` | Artificial Intelligence and the Future of Teaching and Learning: Insights and Recommendations | 2023-05 | unknown |
|  | `ED-OET-DEVELOPERS-GUIDE-2024` | Designing for Education with Artificial Intelligence: An Essential Guide for Developers | 2024-07 | unknown |
|  | `ED-OET-LEADERS-TOOLKIT-2024` | Empowering Education Leaders: A Toolkit for Safe, Ethical, and Equitable AI Integration | 2024-10 | unknown |
|  | `ED-OET-POSTSECONDARY-2025` | Navigating Artificial Intelligence in Postsecondary Education: Building Capacity for the Road Ahead | 2025-01 | unknown |
| U.S. Department of Education, Office of the Secretary | `ED-DCL-AI-2025-07-22` | Dear Colleague Letter: Guidance on the Use of Federal Grant Funds to Improve Education Outcomes Using Artificial Intelligence (AI) | 2025-07-22 | current |
| U.S. Department of Labor | `DOL-AI-WORKER-PRINCIPLES-2024` | Artificial Intelligence and Worker Well-being: Principles and Best Practices for Developers and Employers | 2024-10 | removed from agency site |
| U.S. Equal Employment Opportunity Commission | `EEOC-ADA-AI-2022` | The Americans with Disabilities Act and the Use of Software, Algorithms, and Artificial Intelligence to Assess Job Applicants and Employees | 2022-05 | removed from agency site |
|  | `EEOC-TITLE-VII-AI-2023` | Select Issues: Assessing Adverse Impact in Software, Algorithms, and Artificial Intelligence Used in Employment Selection Procedures Under Title VII of the Civil Rights Act of 1964 | 2023-05-18 | removed from agency site |
| U.S. Government Accountability Office | `GAO-21-519SP` | Artificial Intelligence: An Accountability Framework for Federal Agencies and Other Entities | 2021-06 | report |
|  | `GAO-25-107653` | Artificial Intelligence: Generative AI Use and Management at Federal Agencies | 2025-07 | report |
| U.S. National Science Foundation | `NSF-GAI-MERIT-REVIEW-2023` | Notice to Research Community: Use of Generative Artificial Intelligence Technology in the NSF Merit Review Process | 2023-12-14 | in force |
| U.S. Office of Personnel Management | `OPM-GENAI-FEDERAL-WORKFORCE-2024` | Responsible Use of Generative Artificial Intelligence for the Federal Workforce | 2024-04 | removed from agency site |
| White House Office of Science and Technology Policy | `OSTP-AI-BILL-OF-RIGHTS-2022` | Blueprint for an AI Bill of Rights: Making Automated Systems Work for the American People | 2022-10 | removed from agency site |

