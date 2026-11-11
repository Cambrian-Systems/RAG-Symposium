"""Convert your own files into corpus documents that rag-ingest can read.

    uv run rag-add report.pdf
    uv run rag-add notes.docx policy.html memo.txt --issuer "My department"
    uv run rag-add ~/my-papers            # every supported file in a folder

Each file becomes one `<ID>.md` in corpus/docs/: a header, then the extracted
text behind `<!-- page N -->` markers. That is the same format as the workshop
documents, so `uv run rag-ingest` picks the new ones up with the rest.

Supported: PDF, Word (.docx), web pages (.html, .htm) and plain text (.txt,
.md). A PDF keeps its own pages. The other formats have no page breaks, so
their text is cut into numbered sections of about 3,000 characters at line
ends; those sections play the role of pages in citations.

This only extracts text that is already in the file. A scanned PDF with no
text layer needs OCR first, and tables keep their words but lose their layout.
"""
import argparse
import html
import io
import json
import logging
import re
import sys
import unicodedata
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

from .ingest import read_document

SUPPORTED = {".pdf", ".docx", ".html", ".htm", ".txt", ".md"}
SECTION_SIZE = 3000
# Header fields, in the order the workshop documents use.
FIELDS = ["id", "aliases", "title", "issuer", "published", "revised", "status", "status_note",
          "status_evidence", "replaces", "replaced_by", "topics", "source_url", "credit", "license_note"]
WORD = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
# pypdf warns about fonts it cannot fully decode; the text still extracts.
logging.getLogger("pypdf").setLevel(logging.ERROR)


def clean(text: str) -> str:
    """Normalise extracted text so search sees ordinary words.

    NFKC folds typographic ligatures (the single character "ﬁ" becomes "fi"),
    which otherwise hide words like "defined" from a word search.
    """
    text = unicodedata.normalize("NFKC", text).replace("\u00ad", "")
    # Drop form feeds and other control characters some files carry.
    text = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", " ", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def sections(text: str, size: int = SECTION_SIZE) -> list[str]:
    """Cut text without page breaks into sections of about `size` characters, at line ends."""
    pages, current = [], ""
    for line in clean(text).splitlines():
        if current.strip() and len(current) + len(line) > size:
            pages.append(current)
            current = ""
        current += line + "\n"
    return [page.strip() for page in pages + [current] if page.strip()]


def from_pdf(path: Path) -> tuple[str, list[str]]:
    """One string per PDF page, in reading order, and the PDF's own title if it has one."""
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(path.read_bytes()))
    if reader.is_encrypted and not reader.decrypt(""):
        raise ValueError("the PDF is password-protected")
    pages = [clean(page.extract_text() or "") for page in reader.pages]
    if not any(pages):
        raise ValueError("no text found; a scanned PDF needs OCR before it can be searched")
    title = (reader.metadata.title if reader.metadata else "") or ""
    return title, pages


def from_docx(path: Path) -> tuple[str, list[str]]:
    """Paragraphs and table rows from a Word file, read straight from its XML."""
    with zipfile.ZipFile(path) as archive:
        body = ElementTree.fromstring(archive.read("word/document.xml")).find(f"{WORD}body")
        title = ""
        if "docProps/core.xml" in archive.namelist():
            found = ElementTree.fromstring(archive.read("docProps/core.xml")).find(
                "{http://purl.org/dc/elements/1.1/}title")
            title = (found.text or "") if found is not None else ""

    def paragraph(node) -> str:
        parts = []
        for item in node.iter():
            if item.tag == f"{WORD}t":
                parts.append(item.text or "")
            elif item.tag == f"{WORD}tab":
                parts.append("\t")
            elif item.tag in (f"{WORD}br", f"{WORD}cr"):
                parts.append("\n")
        return "".join(parts)

    lines = []
    for block in body if body is not None else []:
        if block.tag == f"{WORD}p":
            lines.append(paragraph(block))
        elif block.tag == f"{WORD}tbl":
            # A table row becomes one line, cells separated by " | ".
            for row in block.iter(f"{WORD}tr"):
                cells = [" ".join(paragraph(p) for p in cell.iter(f"{WORD}p")).strip()
                         for cell in row.iter(f"{WORD}tc")]
                lines.append(" | ".join(cells))
    return title, sections("\n".join(lines))


class _VisibleText(HTMLParser):
    """Collect a web page's visible text, skipping scripts, styles and navigation."""

    SKIP = {"script", "style", "nav", "header", "footer", "noscript", "form", "svg"}
    BREAK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "table", "section"}

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


def from_html(path: Path) -> tuple[str, list[str]]:
    """A saved web page's visible text, preferring its <main> or <article> part."""
    page = path.read_bytes().decode("utf-8", errors="replace")
    found = re.search(r"<title[^>]*>(.*?)</title>", page, flags=re.S | re.I)
    title = html.unescape(re.sub(r"\s+", " ", found.group(1)).strip()) if found else ""
    for tag in ("main", "article"):
        inner = re.search(rf"<{tag}\b.*?</{tag}>", page, flags=re.S | re.I)
        if inner:
            page = inner.group(0)
            break
    parser = _VisibleText()
    parser.feed(page)
    lines = (re.sub(r"\s+", " ", line).strip() for line in "".join(parser.parts).splitlines())
    return title, sections("\n".join(line for line in lines if line))


def from_text(path: Path) -> tuple[str, list[str]]:
    """A plain text or Markdown file, read as UTF-8."""
    return "", sections(path.read_bytes().decode("utf-8-sig", errors="replace"))


READERS = {".pdf": from_pdf, ".docx": from_docx, ".html": from_html, ".htm": from_html,
           ".txt": from_text, ".md": from_text}


def document_id(name: str) -> str:
    """A stable ID from a file name: REPORT-2026 from 'Report (2026).pdf'."""
    plain = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "-", plain).strip("-").upper()[:80] or "DOCUMENT"


def convert(path: Path, out: Path, replace: bool = False, **fields) -> dict:
    """Write one file as a corpus document and return a summary of it.

    `fields` are header values given on the command line; `id`, `title` and
    `source_url` fall back to the file's name and its own title.
    """
    reader = READERS.get(path.suffix.lower())
    if reader is None:
        raise ValueError(f"unsupported file type {path.suffix or '(none)'}; use {', '.join(sorted(SUPPORTED))}")
    found_title, pages = reader(path)
    if not any(pages):
        raise ValueError("no text found in the file")
    doc_id = fields.get("id") or document_id(path.stem)
    if not re.fullmatch(r"[\w.-]{1,190}", doc_id):
        raise ValueError(f"ID {doc_id!r} may only contain letters, numbers, underscores, dots and dashes")
    target = out / f"{doc_id}.md"
    if target.exists() and not replace:
        raise ValueError(f"{target} already exists; pass --replace to overwrite it, or --id to choose another ID")
    header = {"aliases": [], "replaces": [], "replaced_by": [], "topics": []}
    header.update({key: value for key, value in fields.items() if value})
    header["id"] = doc_id
    # A PDF's first line is usually a letterhead, so only the other formats
    # fall back to their first line when the file carries no title of its own.
    first_line = "" if path.suffix.lower() == ".pdf" else next(iter(pages[0].splitlines()), "").lstrip("# ").strip()
    header["title"] = (fields.get("title") or clean(found_title)
                       or (first_line if 0 < len(first_line) <= 120 else "") or path.stem)
    header["source_url"] = fields.get("source_url") or path.name
    lines = ["---"] + [f"{key}: {json.dumps(header.get(key, ''), ensure_ascii=False)}" for key in FIELDS] + ["---", ""]
    for number, text in enumerate(pages, 1):
        lines += [f"<!-- page {number} -->", text, ""]
    out.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    # Read it back the way ingestion will, so a bad document fails here.
    read_document(target)
    return {"id": doc_id, "title": header["title"], "path": str(target),
            "pages": len(pages), "empty_pages": sum(not page for page in pages),
            "characters": sum(len(page) for page in pages)}


def main():
    """Convert each file (or each supported file in a folder) and report what was written."""
    parser = argparse.ArgumentParser(
        description="Convert PDF, Word, HTML and text files into corpus documents for rag-ingest")
    parser.add_argument("paths", nargs="+", type=Path, help="Files, or folders of files, to add")
    parser.add_argument("--out", type=Path, default=Path("corpus/docs"),
                        help="Folder the documents are written to (default: corpus/docs)")
    parser.add_argument("--replace", action="store_true", help="Overwrite a document that already exists")
    parser.add_argument("--id", help="Document ID (one file only; default: from the file name)")
    parser.add_argument("--title", help="Title (one file only; default: the file's own title, or its name)")
    parser.add_argument("--source", dest="source_url",
                        help="Where the original lives, such as a URL (one file only; default: the file name)")
    parser.add_argument("--issuer", help="Who wrote or published the documents")
    parser.add_argument("--published", help="Date as YYYY-MM-DD or YYYY-MM")
    parser.add_argument("--status", help='Standing, such as "in force", "draft" or "superseded"')
    args = parser.parse_args()

    files = []
    for path in args.paths:
        if path.is_dir():
            files += sorted(p for p in path.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED)
        else:
            files.append(path)
    if not files:
        parser.error("no supported files found")
    if len(files) > 1 and (args.id or args.title or args.source_url):
        parser.error("--id, --title and --source describe one document; add files one at a time to use them")

    fields = {key: getattr(args, key) for key in ("id", "title", "source_url", "issuer", "published", "status")}
    failed = 0
    for path in files:
        try:
            if not path.is_file():
                raise ValueError("file not found")
            done = convert(path, args.out, args.replace, **fields)
        except (ValueError, OSError, zipfile.BadZipFile, KeyError, ElementTree.ParseError) as error:
            failed += 1
            print(f"SKIPPED {path.name}: {error}", file=sys.stderr)
            continue
        except Exception as error:  # A damaged PDF can fail in many ways inside pypdf.
            failed += 1
            print(f"SKIPPED {path.name}: could not be read ({type(error).__name__}: {error})", file=sys.stderr)
            continue
        note = f", {done['empty_pages']} with no text" if done["empty_pages"] else ""
        print(f"Added {done['id']}: \"{done['title']}\", {done['pages']} pages{note}, "
              f"{done['characters']:,} characters -> {done['path']}")
    added = len(files) - failed
    if added:
        # A separate folder gets its own export, so it does not replace the workshop one.
        where = "" if args.out == Path("corpus/docs") else f" --corpus {args.out} --output my-docs.jsonl"
        print(f"\nAdded {added} document{'s' if added != 1 else ''}. "
              f"Read one to check the text, then run: uv run rag-ingest{where}")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
