"""Reproduce the workshop's retrieval observations without a chatbot or API key.

All ingestion exports are temporary. This does not replace the attendee's data
or evaluate a generated answer. Run from the repo with:
    uv run python presentation/check_demo.py
Use --save PATH only when intentionally recording a new retrieval snapshot.
"""
import argparse
import json
import subprocess
import tempfile
from datetime import date
from pathlib import Path

from rag_symposium.ingest import ingest
from rag_symposium.store import RecordStore

BROAD_QUERY = "frost free season western central eastern"
SPECIFIC_QUERY = "frost free season western central eastern climate 1895 2015"
PARAPHRASE = "days crops can grow west middle east Kansas"


def capture(repo: Path) -> dict:
    """Compare fixed inputs across ingestion modes and retain source provenance."""
    revision = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    report = {"checked_on": date.today().isoformat(), "revision": revision,
              "kind": "retrieval-only; no generated answers", "modes": {}}
    with tempfile.TemporaryDirectory(prefix="symposium-presentation-check-") as folder:
        for mode in ("page", "window", "document"):
            export = Path(folder) / f"{mode}.jsonl"
            summary = ingest(repo / "corpus/docs", export, mode=mode)
            store = RecordStore(export)
            queries = {}
            for query in (BROAD_QUERY, SPECIFIC_QUERY, PARAPHRASE):
                queries[query] = store.search(query, limit=3)["matches"]
            report["modes"][mode] = {"documents": summary["documents"], "records": summary["records"],
                                      "queries": queries}
            if mode == "page":
                record = store.get("MF3334-p2")
                if not all(str(number) in record["text"] for number in (170, 182, 189)):
                    raise ValueError("The anchor source changed; review the exercise before presenting")
                report["anchor_source"] = {"id": record["id"], "source": record["source"],
                    "pages": record["metadata"]["pages"], "published": record["metadata"]["published"],
                    "excerpt": record["text"][:310]}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--save", type=Path, help="Optionally write the observed retrieval report as JSON")
    args = parser.parse_args()
    report = capture(args.repo.resolve())
    print(f"Revision: {report['revision'][:7]} | retrieval only; no language model called")
    for mode, result in report["modes"].items():
        ids = [record["id"] for record in result["queries"][BROAD_QUERY]]
        print(f"{mode}: {result['documents']} documents -> {result['records']} records; top three: {', '.join(ids)}")
    if args.save:
        args.save.parent.mkdir(parents=True, exist_ok=True)
        args.save.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Saved labeled retrieval snapshot to {args.save}")


if __name__ == "__main__":
    main()
