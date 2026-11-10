"""Check that this laptop is ready for the workshop, one PASS/FAIL line per step.

    uv run rag-check

1. The ingestion export exists and has records (run `uv run rag-ingest` if not).
2. The embedding model loads with no network, so hybrid search works offline.
3. A keyword search returns results.
4. A hybrid search returns results.

The searches use the first record's title as the query, so the check works
with any export. It exits with status 0 only if every step passes.
"""
import argparse
import os
import sys
from pathlib import Path

from .embeddings import DEFAULT_MODEL, Embedder
from .store import RecordStore


def run_checks(data: Path, embedder, query: str | None = None) -> list[tuple[bool, str]]:
    """Run every check and return (passed, message) pairs, in order.

    embedder is an embeddings.Embedder; main() makes one that cannot download.

    A later check that depends on a failed one fails too, with the reason,
    rather than being skipped, so the output always has the same four lines.
    """
    results = []

    def check(name, step):
        """Run one step; a step returns its PASS message or raises with the reason."""
        try:
            results.append((True, f"{name}: {step()}"))
        except Exception as exc:  # Any failure becomes a FAIL line, never a traceback.
            results.append((False, f"{name}: {exc}"))
        return results[-1][0]

    records = []

    def export():
        records.extend(RecordStore(data).records())
        if not records:
            missing = "is missing" if not data.expanduser().is_file() else "has no records"
            raise RuntimeError(f"{data} {missing}. Run `uv run rag-ingest` first.")
        return f"{data} has {len(records)} records"

    def model():
        try:
            vectors = embedder.encode(["setup check"])
        except Exception as exc:
            raise RuntimeError(f"{embedder.name} did not load offline ({type(exc).__name__}). "
                               "While online, run `uv run rag-search test --mode hybrid` once to "
                               "download it, or set RAG_EMBED_MODEL to a local model folder.") from exc
        return f"{embedder.name} loads offline ({vectors.shape[1]} dimensions)"

    def search(mode):
        def step():
            if not records:
                raise RuntimeError("no records to search (see the export check)")
            store = RecordStore(data, mode, embedder if mode == "hybrid" else None)
            text = query or records[0]["title"]
            matches = store.search(text[:2000], 5)["matches"]
            if not matches:
                raise RuntimeError(f"no results for {text!r}")
            return f"{len(matches)} results for {text[:50]!r}, first {matches[0]['id']}"
        return step

    check("export", export)
    model_loaded = check("embedding model", model)
    check("keyword search", search("keyword"))
    if model_loaded:
        check("hybrid search", search("hybrid"))
    else:
        results.append((False, "hybrid search: needs the embedding model (see above)"))
    return results


def main():
    """Parse options, print one line per check, and exit 1 if any failed."""
    parser = argparse.ArgumentParser(description="Check the export, embedding model and search")
    parser.add_argument("--data", type=Path,
                        default=Path(os.environ.get("RAG_DATA_PATH", "data/documents.jsonl")),
                        help="Ingestion export to check (default: data/documents.jsonl)")
    parser.add_argument("--embed-model", default=os.environ.get("RAG_EMBED_MODEL", DEFAULT_MODEL),
                        help="Hybrid mode's embedding model: a Hugging Face name or a local folder")
    parser.add_argument("--query", help="Query for the two searches (default: the first record's title)")
    args = parser.parse_args()
    # The Hugging Face libraries read this when first imported (inside
    # Embedder.encode), so the model must already be cached or be a local
    # folder: exactly the situation on a workshop network that is down.
    os.environ["HF_HUB_OFFLINE"] = "1"
    results = run_checks(args.data, Embedder(args.embed_model), args.query)
    for passed, message in results:
        print(f"{'PASS' if passed else 'FAIL'}  {message}")
    sys.exit(0 if all(passed for passed, _ in results) else 1)


if __name__ == "__main__":
    main()
