# /// script
# requires-python = ">=3.10"
# dependencies = ["pypdf>=5"]
# ///
"""Snapshot official U.S. AI rules and guidance into the workshop corpus.

Facilitator-only. Attendees use the committed snapshot in corpus/docs/ and never
download anything during the workshop.

    uv run corpus/fetch_sources.py                # every source in sources.jsonl
    uv run corpus/fetch_sources.py --only EO-14110 OMB-M-24-10
    uv run corpus/fetch_sources.py --check        # report what would change, write nothing

sources.jsonl is the curated list: one JSON object per line, one official
document per object. This script downloads each file once (cached in
corpus/.cache/), turns it into plain text with page markers, and writes
corpus/docs/<id>.md plus corpus/manifest.jsonl.

Status ("in force", "revoked", "rescinded", ...) is never guessed. For executive
orders it is read from the Federal Register's own disposition notes at snapshot
time. For everything else it comes from sources.jsonl, where each status carries
a quoted sentence from an official document as evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import io
import json
import logging
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = HERE / "sources.jsonl"
DOCS = HERE / "docs"
CACHE = HERE / ".cache"
MANIFEST = HERE / "manifest.jsonl"
# Some agency sites refuse requests that do not look like a browser.
UA = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
FR_API = "https://www.federalregister.gov/api/v1/documents/{number}.json"
# Header fields, in the order they are written to each document.
FIELDS = ["id", "aliases", "title", "issuer", "published", "revised", "status", "status_note",
          "status_evidence", "replaces", "replaced_by", "topics", "source_url", "credit", "license_note"]
# pypdf warns about fonts it cannot fully decode; the text still extracts.
logging.getLogger("pypdf").setLevel(logging.ERROR)
PUBLIC_DOMAIN = "U.S. government work; not subject to copyright in the United States (17 U.S.C. 105)."


def get(url: str, tries: int = 3) -> bytes:
    """Download a URL, retrying briefly; raise the last error if every try fails."""
    last = None
    for attempt in range(tries):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError) as error:
            last = error
            time.sleep(2 * (attempt + 1))
    raise last


def cached(source: dict) -> bytes:
    """Return the source file's bytes, downloading it only the first time."""
    CACHE.mkdir(exist_ok=True)
    suffix = ".pdf" if source.get("format", "pdf") == "pdf" else ".html"
    path = CACHE / (source["id"] + suffix)
    if not path.exists():
        path.write_bytes(get(source["url"]))
    return path.read_bytes()


def clean(text: str) -> str:
    """Normalise extracted text so search sees ordinary words.

    NFKC folds typographic ligatures (the single character "ﬁ" becomes "fi"),
    which otherwise hide words like "defined" from a word search.
    """
    text = unicodedata.normalize("NFKC", text).replace("\u00ad", "")
    text = re.sub(r"[ \t]+\n", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def pdf_pages(data: bytes) -> list[str]:
    """Extract one string per PDF page, in reading order."""
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(data))
    return [clean(page.extract_text() or "") for page in reader.pages]


class _Text(HTMLParser):
    """Collect visible text from an HTML page, skipping scripts, styles and navigation."""

    SKIP = {"script", "style", "nav", "header", "footer", "noscript", "form", "svg"}
    BREAK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "table", "section"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.depth += 1
        elif tag in self.BREAK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.depth:
            self.depth -= 1
        elif tag in self.BREAK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.depth:
            self.parts.append(data)


def html_pages(data: bytes, selector: str | None = None) -> list[str]:
    """Return an HTML document as a single 'page' of visible text."""
    page = data.decode("utf-8", errors="replace")
    if selector:
        # Keep only the part of the page after a marker string, when one is given.
        _, found, rest = page.partition(selector)
        page = rest if found else page
    parser = _Text()
    parser.feed(page)
    return [clean(html.unescape("".join(parser.parts)))]


def executive_order_status(source: dict) -> dict:
    """Read an executive order's status from the Federal Register disposition notes."""
    record = json.loads(get(FR_API.format(number=source["fr_document_number"])))
    notes = (record.get("disposition_notes") or "").strip()
    today = date.today().isoformat()
    revoked = re.search(r"Revoked by:\s*(.+?)(?:\n|$)", notes)
    update = {"published": record.get("signing_date") or source.get("published", ""),
              "status_evidence": f"Federal Register disposition notes, read {today}: "
                                 f"{notes or '(none)'} | {record.get('html_url', '')}"}
    if revoked:
        update["status"] = "revoked"
        update["status_note"] = f"Revoked by {revoked.group(1).strip()}."
        update["replaced_by"] = ["EO-" + n for n in re.findall(r"EO (\d+)", revoked.group(1))]
    else:
        update["status"] = "in force"
        amended = re.search(r"Amended by:\s*(.+?)(?:\n|$)", notes)
        update["status_note"] = (f"Amended by {amended.group(1).strip()}; not revoked as of {today}." if amended
                                 else f"No revocation recorded in the Federal Register as of {today}.")
    revokes = re.search(r"Revokes:\s*(.+?)(?:\n|$)", notes)
    if revokes:
        update["replaces"] = ["EO-" + n for n in re.findall(r"EO (\d+)", revokes.group(1))]
    return update


def build(source: dict) -> tuple[dict, list[str]]:
    """Return a document's header and its page texts."""
    data = cached(source)
    pages = pdf_pages(data) if source.get("format", "pdf") == "pdf" else html_pages(data, source.get("html_after"))
    header = {"aliases": [], "revised": "", "status": "unknown", "status_note": "", "status_evidence": "",
              "replaces": [], "replaced_by": [], "topics": [], "license_note": PUBLIC_DOMAIN}
    header.update({key: value for key, value in source.items() if key in FIELDS})
    header["source_url"] = source.get("landing_url") or source["url"]
    if source.get("fr_document_number"):
        header.update(executive_order_status(source))
    when = header.get("revised") or header.get("published", "")
    header.setdefault("credit", f"{header['issuer']}, {header['title']}, {when}.".replace(", .", "."))
    header["_sha256"] = hashlib.sha256(data).hexdigest()
    return header, pages


def write(header: dict, pages: list[str]) -> None:
    """Write one corpus document: the header block, then each page behind its marker."""
    lines = ["---"] + [f"{key}: {json.dumps(header.get(key, ''), ensure_ascii=False)}" for key in FIELDS] + ["---", ""]
    for number, text in enumerate(pages, 1):
        lines += [f"<!-- page {number} -->", text, ""]
    (DOCS / f"{header['id']}.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Snapshot official AI rules and guidance into corpus/docs/")
    parser.add_argument("--only", nargs="+", metavar="ID", help="fetch only these document IDs")
    parser.add_argument("--check", action="store_true", help="download and extract, but write nothing")
    args = parser.parse_args()
    sources = [json.loads(line) for line in SOURCES.read_text(encoding="utf-8").splitlines() if line.strip()]
    seen = set()
    for source in sources:
        if source["id"] in seen:
            sys.exit(f"sources.jsonl lists {source['id']} twice")
        seen.add(source["id"])
    if args.only:
        sources = [s for s in sources if s["id"] in set(args.only)]
    DOCS.mkdir(exist_ok=True)
    rows, failed = [], []
    for source in sources:
        try:
            header, pages = build(source)
        except Exception as error:  # Keep going: one bad source must not lose the rest.
            failed.append((source["id"], repr(error)))
            print(f"FAIL  {source['id']}: {error}", file=sys.stderr)
            continue
        characters = sum(len(page) for page in pages)
        # A scanned PDF extracts to almost nothing; flag it rather than ship an empty document.
        thin = characters < 400 * len(pages)
        print(f"{'THIN' if thin else 'ok  '}  {header['id']:<34} {len(pages):>4} pages {characters:>8} chars  {header['status']}")
        if not args.check:
            write(header, pages)
        rows.append({"id": header["id"], "title": header["title"], "issuer": header["issuer"],
                     "published": header.get("published", ""), "status": header["status"], "pages": len(pages),
                     "characters": characters, "url": source["url"], "sha256": header["_sha256"],
                     "fetched": date.today().isoformat()})
    if not args.check and not args.only:
        MANIFEST.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
        # A full run makes docs/ match sources.jsonl exactly.
        for stale in set(p.stem for p in DOCS.glob("*.md")) - {row["id"] for row in rows} - {f[0] for f in failed}:
            (DOCS / f"{stale}.md").unlink()
            print(f"removed {stale}.md (no longer in sources.jsonl)")
    print(f"{len(rows)} documents, {sum(r['pages'] for r in rows)} pages, {len(failed)} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
