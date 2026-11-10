"""Turn the workshop corpus into the JSONL export the server reads.

Each corpus document is one Markdown file: a header of `key: JSON value` lines
between `---` markers, then the extracted text with `<!-- page N -->` markers.
Ingestion splits that text into records, keeps provenance in metadata, and
publishes the whole export at once. It loads no model and creates no embeddings;
chunking choices made here decide what any later search can return.
"""
import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

from .store import RecordStore

PAGE_MARKER = re.compile(r"<!-- page (\d+) -->\n?")
WHITESPACE = re.compile(r"\s+")


def read_document(path: Path) -> tuple[dict, list[tuple[int, str]]]:
    """Return a document's header fields and its (page number, text) pairs."""
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n") or "\n---\n" not in content[4:]:
        raise ValueError(f"{path.name}: missing the --- header block")
    header_text, body = content[4:].split("\n---\n", 1)
    header = {}
    for line in header_text.splitlines():
        key, _, value = line.partition(": ")
        header[key] = json.loads(value)
    # re.split with a capture group alternates text and page numbers:
    # [before-first-marker, "1", page-1 text, "2", page-2 text, ...].
    parts = PAGE_MARKER.split(body)
    pages = [(int(number), text.strip()) for number, text in zip(parts[1::2], parts[2::2])]
    if not pages:
        # A document without markers is treated as a single page.
        pages = [(1, body.strip())]
    return header, pages


def windows(pages: list[tuple[int, str]], size: int, overlap: int) -> list[tuple[str, list[int]]]:
    """Split a document into ~size-character windows that share `overlap` characters.

    Windows end at the last newline or space before the limit when there is one,
    so words are not cut in half. Each window reports the pages it spans.
    """
    # Join pages into one string and remember where each page starts in it.
    text, starts = "", []
    for number, page_text in pages:
        starts.append((len(text), number))
        text += page_text + "\n\n"
    text = text.rstrip()
    chunks, start = [], 0
    while start < len(text):
        end = min(len(text), start + size)
        if end < len(text):
            cut = max(text.rfind("\n", start + size // 2, end), text.rfind(" ", start + size // 2, end))
            end = cut if cut > start else end
        spanned = [n for i, (offset, n) in enumerate(starts)
                   if offset < end and (i + 1 == len(starts) or starts[i + 1][0] > start)]
        if text[start:end].strip():
            chunks.append((text[start:end].strip(), spanned))
        if end >= len(text):
            break
        # Step back by the overlap so a sentence cut at a boundary appears whole
        # in at least one window, then skip ahead to the next word boundary so
        # the window does not open mid-word. Always move forward.
        next_start = end - overlap
        if overlap and not text[next_start - 1].isspace():
            boundary = WHITESPACE.search(text, next_start, end)
            next_start = boundary.end() if boundary else end
        start = max(next_start, start + 1)
    return chunks


def records_for(header: dict, pages: list[tuple[int, str]], mode: str,
                size: int, overlap: int) -> list[dict]:
    """Build export records for one document under the chosen chunking mode."""
    doc_id = header["id"]
    if mode == "document":
        pieces = [("\n\n".join(text for _, text in pages), [n for n, _ in pages])]
        ids = [doc_id]
    elif mode == "page":
        pieces = [(text, [n]) for n, text in pages if text]
        ids = [f"{doc_id}-p{spanned[0]}" for _, spanned in pieces]
    else:
        pieces = windows(pages, size, overlap)
        ids = [f"{doc_id}-w{i}" for i in range(len(pieces))]
    # Every record carries its document's status, so a search result can say
    # "rescinded" or "superseded" without reading the header separately.
    # Optional header fields default to empty, so older documents still ingest.
    shared = {
        "document_id": doc_id,
        "aliases": header.get("aliases", []),
        "issuer": header.get("issuer", ""),
        "published": header.get("published", ""),
        "revised": header.get("revised", ""),
        "status": header.get("status", ""),
        "status_note": header.get("status_note", ""),
        "replaces": header.get("replaces", []),
        "replaced_by": header.get("replaced_by", []),
        "topics": header.get("topics", []),
        "credit": header.get("credit", ""),
    }
    records = []
    for index, (record_id, (text, spanned)) in enumerate(zip(ids, pieces)):
        if not text.strip():
            continue  # The server rejects empty text; blank scanned pages carry nothing.
        records.append({
            "id": record_id,
            "title": header["title"],
            "text": text,
            "source": header["source_url"],
            "metadata": {**shared, "pages": spanned, "chunk_index": index},
        })
    return records


def publish(records: list[dict], output: Path) -> None:
    """Write the complete export to a temporary file, then rename it into place.

    The server rereads the export on every call; a rename means a reader sees
    either the old file or the new one, never a half-written mix.
    """
    output.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=output.parent, prefix=".ingest-", suffix=".jsonl")
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            for record in records:
                stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        os.replace(temporary, output)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def ingest(corpus: Path, output: Path, mode: str = "page", size: int = 1500,
           overlap: int = 200) -> dict:
    """Read every corpus document, chunk it, validate the records and publish them."""
    files = sorted(corpus.glob("*.md"))
    if not files:
        raise ValueError(f"No .md documents found in {corpus}")
    records = []
    for path in files:
        header, pages = read_document(path)
        records.extend(records_for(header, pages, mode, size, overlap))
    # Check against the server's own rules before publishing, so a bad export
    # fails here instead of on an attendee's first tool call.
    seen = set()
    for record in records:
        RecordStore.validate(record)
        if record["id"] in seen:
            raise ValueError(f"Duplicate record ID {record['id']}")
        seen.add(record["id"])
    publish(records, output)
    return {"documents": len(files), "records": len(records), "mode": mode, "output": str(output)}


def main():
    """Parse options, ingest the corpus, and report what was published."""
    parser = argparse.ArgumentParser(description="Chunk the workshop corpus into a JSONL export")
    parser.add_argument("--corpus", type=Path, default=Path("corpus/docs"),
                        help="Folder of corpus .md documents (default: corpus/docs)")
    parser.add_argument("--output", type=Path,
                        default=Path(os.environ.get("RAG_DATA_PATH", "data/documents.jsonl")),
                        help="Export path the server reads (default: data/documents.jsonl)")
    parser.add_argument("--mode", choices=("page", "window", "document"), default="page",
                        help="One record per PDF page, per fixed-size window, or per document")
    parser.add_argument("--size", type=int, default=1500, help="Window size in characters (window mode)")
    parser.add_argument("--overlap", type=int, default=200, help="Characters shared by adjacent windows")
    args = parser.parse_args()
    if args.size < 100 or not 0 <= args.overlap < args.size // 2:
        parser.error("--size must be at least 100 and --overlap between 0 and half of --size")
    summary = ingest(args.corpus, args.output, args.mode, args.size, args.overlap)
    print(f"Published {summary['records']} records from {summary['documents']} documents "
          f"({summary['mode']} mode) to {summary['output']}", file=sys.stderr)


if __name__ == "__main__":
    main()
