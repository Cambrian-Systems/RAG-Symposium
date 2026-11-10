"""Score search against a set of questions with known answers, with no model involved.

A question file is JSONL. Each line names the documents (and optionally the
pages) that hold the answer. rag-eval runs every question through the same
search the server uses and reports how often the right record came back:

- hit@1: the first result comes from a right document.
- hit@k: a right one is somewhere in the top k (default 5).
- MRR: mean reciprocal rank. 1 for first place, 1/2 for second, 0 for a miss.
- page hit@1 / hit@k: the same, for questions that name pages, but a result
  must also cover one of those pages. Finding the right document but the wrong
  page counts as a document hit and a page miss.

Questions with an empty `expect` list have no answer in the data. For those,
the score is whether search warned that its results don't cover the question.
Warnings on questions the data does answer are counted too, as false alarms.
This measures retrieval only: whether the evidence reached the agent, not
whether the agent's answer was right.
"""
import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

from .embeddings import DEFAULT_MODEL, Embedder
from .store import SEARCH_MODES, RecordStore


def load_questions(path: Path) -> list[dict]:
    """Read and check a question file, naming the line of any problem."""
    questions, ids = [], set()
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                question = json.loads(line)
                if not isinstance(question, dict):
                    raise ValueError("each line must be a JSON object")
                for field in ("id", "question"):
                    if not isinstance(question.get(field), str) or not question[field].strip():
                        raise ValueError(f"{field} must be nonempty text")
                if question["id"] in ids:
                    raise ValueError("duplicate question id")
                expect = question.get("expect")
                if not isinstance(expect, list) or not all(isinstance(e, str) for e in expect):
                    raise ValueError("expect must be a list of document IDs ([] if unanswerable)")
                pages = question.get("pages", [])
                if not isinstance(pages, list) or not all(type(p) is int for p in pages):
                    raise ValueError("pages must be a list of page numbers")
            except (ValueError, TypeError) as exc:
                raise ValueError(f"{path}, line {line_number}: {exc}") from exc
            ids.add(question["id"])
            questions.append(question)
    if not questions:
        raise ValueError(f"{path} has no questions")
    return questions


def is_right(match: dict, question: dict, by_page: bool = False) -> bool:
    """A result counts if it comes from an expected document. With by_page,
    and when the question names pages, it must also cover one of them."""
    metadata = match.get("metadata", {})
    document = metadata.get("document_id", match["id"])
    if document not in question["expect"]:
        return False
    pages = question.get("pages") if by_page else None
    return not pages or bool(set(pages) & set(metadata.get("pages", [])))


def rank_of(matches: list[dict], question: dict, by_page: bool = False) -> int | None:
    """1-based position of the first right result, or None if none came back.

    With "all": true, every expected document must appear, and the rank is
    the position where the last one showed up. by_page is passed to is_right.
    """
    if question.get("all"):
        needed, found = set(question["expect"]), set()
        for position, match in enumerate(matches, 1):
            if is_right(match, question, by_page):
                found.add(match.get("metadata", {}).get("document_id", match["id"]))
                if found == needed:
                    return position
        return None
    for position, match in enumerate(matches, 1):
        if is_right(match, question, by_page):
            return position
    return None


def evaluate(store: RecordStore, questions: list[dict], k: int = 5) -> dict:
    """Run every question once and collect per-question results and totals."""
    rows = []
    for question in questions:
        result = store.search(question["question"], k)
        matches = result["matches"]
        row = {"id": question["id"], "question": question["question"],
               "category": question.get("category", "general"), "expect": question["expect"],
               "top": [m["id"] for m in matches]}
        warned = not matches or bool(result.get("missing_terms"))
        if question["expect"]:
            row["rank"] = rank_of(matches, question)
            if question.get("pages"):
                row["pages"] = question["pages"]
                row["page_rank"] = rank_of(matches, question, by_page=True)
            # A warning on a question the data does answer is a false alarm.
            row["false_warning"] = warned
        else:
            # Without an answer to find, the useful behavior is a warning.
            row["flagged"] = warned
        row["missing_terms"] = result.get("missing_terms", [])
        rows.append(row)
    return {"mode": store.mode, "k": k, "summary": summarize(rows), "questions": rows}


def summarize(rows: list[dict]) -> dict:
    """Totals overall and per category. Rates are fractions from 0 to 1."""
    def scores(group):
        answerable = [r for r in group if "rank" in r]
        unanswerable = [r for r in group if "flagged" in r]
        ranks = [r["rank"] for r in answerable]
        n = len(answerable)
        # Page-level scores count only the questions that name pages.
        page_ranks = [r["page_rank"] for r in answerable if "page_rank" in r]
        p = len(page_ranks)
        return {"answerable": n,
                "hit@1": sum(r == 1 for r in ranks) / n if n else None,
                "hit@k": sum(r is not None for r in ranks) / n if n else None,
                "mrr": sum(1 / r for r in ranks if r) / n if n else None,
                "with_pages": p,
                "page_hit@1": sum(r == 1 for r in page_ranks) / p if p else None,
                "page_hit@k": sum(r is not None for r in page_ranks) / p if p else None,
                "unanswerable": len(unanswerable),
                "flagged": sum(r["flagged"] for r in unanswerable),
                "false_warnings": sum(r["false_warning"] for r in answerable)}
    categories = defaultdict(list)
    for row in rows:
        categories[row["category"]].append(row)
    return {"all": scores(rows), "categories": {c: scores(g) for c, g in sorted(categories.items())}}


def percent(value) -> str:
    return "  -  " if value is None else f"{value * 100:4.0f}%"


def report(results: list[dict], show: str) -> str:
    """Plain-text tables: one line per mode, then per category, then misses."""
    k = results[0]["k"]
    lines = [f"{'':<10} {'document':^19} {'page':^13}",
             f"{'mode':<10} {'hit@1':>6} {f'hit@{k}':>6} {'MRR':>5} {'hit@1':>6} {f'hit@{k}':>6}"
             "   warned: no answer / has answer"]
    for result in results:
        s = result["summary"]["all"]
        mrr = "  -  " if s["mrr"] is None else f"{s['mrr']:.2f}"
        lines.append(f"{result['mode']:<10} {percent(s['hit@1']):>6} {percent(s['hit@k']):>6} "
                     f"{mrr:>5} {percent(s['page_hit@1']):>6} {percent(s['page_hit@k']):>6}   "
                     f"{s['flagged']}/{s['unanswerable']:<9} {s['false_warnings']}/{s['answerable']}")
    totals = results[0]["summary"]["all"]
    lines.append(f"\n({totals['answerable']} answerable questions, {totals['with_pages']} of them "
                 f"naming pages; {totals['unanswerable']} with no answer in the data)")
    lines.append(f"\nhit@{k} by category")
    categories = results[0]["summary"]["categories"]
    lines.append(f"{'category':<16}" + "".join(f"{r['mode']:>12}" for r in results))
    for category in categories:
        cells = []
        for result in results:
            s = result["summary"]["categories"][category]
            cells.append(f"{s['flagged']}/{s['unanswerable']} warned" if not s["answerable"]
                         else percent(s["hit@k"]).strip())
        lines.append(f"{category:<16}" + "".join(f"{c:>12}" for c in cells))
    for result in results:
        rows = [r for r in result["questions"]
                if show == "all" or (show == "misses" and not r.get("flagged")
                                     and (r.get("rank") != 1 or r.get("page_rank", 1) != 1))]
        if not rows:
            continue
        lines.append(f"\n{result['mode']}: {'every question' if show == 'all' else 'not ranked first'}")
        for row in rows:
            if "rank" in row:
                outcome = f"rank {row['rank']}" if row["rank"] else "MISS"
                if "page_rank" in row:
                    outcome += f", page {row['page_rank'] or 'MISS'}"
            else:
                outcome = "warned" if row["flagged"] else "no warning"
            lines.append(f"  {row['id']:<5} {outcome:<16} {row['question']}")
            pages = f" (pages {', '.join(map(str, row['pages']))})" if row.get("pages") else ""
            lines.append(f"        expected {', '.join(row['expect']) or '(no answer)'}{pages}; "
                         f"got {', '.join(row['top'][:3]) or 'nothing'}")
    return "\n".join(lines)


def main():
    """Parse options, score each requested search mode, and print the comparison."""
    parser = argparse.ArgumentParser(description="Score search results against known answers")
    parser.add_argument("--questions", type=Path, default=Path("evals/starter.jsonl"),
                        help="Question file (default: evals/starter.jsonl)")
    parser.add_argument("--data", type=Path,
                        default=Path(os.environ.get("RAG_DATA_PATH", "data/documents.jsonl")),
                        help="Ingestion export to search (default: data/documents.jsonl)")
    parser.add_argument("--mode", choices=SEARCH_MODES, action="append",
                        help="Search mode to score; repeat to compare (default: all)")
    parser.add_argument("--embed-model", default=os.environ.get("RAG_EMBED_MODEL", DEFAULT_MODEL),
                        help="Hybrid mode's embedding model: a Hugging Face name or a local folder")
    parser.add_argument("-k", type=int, default=5, help="How many results count (1-10, default 5)")
    parser.add_argument("--show", choices=("none", "misses", "all"), default="misses",
                        help="Which questions to list under the scores (default: misses)")
    parser.add_argument("--json", action="store_true", help="Print full results as JSON")
    args = parser.parse_args()
    if not 1 <= args.k <= 10:
        parser.error("-k must be between 1 and 10")
    questions = load_questions(args.questions)
    stores = [RecordStore(args.data, mode, Embedder(args.embed_model) if mode == "hybrid" else None)
              for mode in (args.mode or SEARCH_MODES)]
    if not stores[0].status()["record_count"]:
        parser.error(f"{args.data} has no records. Run `uv run rag-ingest` first.")
    results = [evaluate(store, questions, args.k) for store in stores]
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(report(results, args.show))


if __name__ == "__main__":
    main()
