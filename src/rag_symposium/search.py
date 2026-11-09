"""Run one search from the command line and print what the agent would receive.

No model or chat client is involved, so the result depends only on the query,
the export and the search mode. Useful for comparing modes side by side:

    uv run rag-search "How do I control cheatgrass in wheat?" --mode keyword --mode bm25
"""
import argparse
import os
from pathlib import Path

from .embeddings import DEFAULT_MODEL, Embedder
from .store import SEARCH_MODES, RecordStore


def main():
    parser = argparse.ArgumentParser(description="Print search results for one query")
    parser.add_argument("query")
    parser.add_argument("--mode", choices=SEARCH_MODES, action="append",
                        help="Search mode; repeat to compare (default: all)")
    parser.add_argument("--data", type=Path,
                        default=Path(os.environ.get("RAG_DATA_PATH", "data/documents.jsonl")))
    parser.add_argument("--embed-model", default=os.environ.get("RAG_EMBED_MODEL", DEFAULT_MODEL))
    parser.add_argument("-k", type=int, default=5, help="Results per mode (1-10, default 5)")
    args = parser.parse_args()
    if not 1 <= args.k <= 10:
        parser.error("-k must be between 1 and 10")
    for mode in args.mode or SEARCH_MODES:
        store = RecordStore(args.data, mode, Embedder(args.embed_model) if mode == "hybrid" else None)
        result = store.search(args.query, args.k)
        print(f"\n{mode}")
        for position, match in enumerate(result["matches"], 1):
            metadata = match["metadata"]
            date = metadata.get("revised") or metadata.get("published") or ""
            ranks = match.get("ranks")
            found = f"  (bm25 #{ranks['bm25'] or '-'}, embeddings #{ranks['semantic'] or '-'})" if ranks else ""
            print(f"  {position}. {match['id']:<12} {date:<9} {match['title'][:56]}{found}")
        if result.get("missing_terms"):
            print(f"  No result contains: {', '.join(result['missing_terms'])}")


if __name__ == "__main__":
    main()
