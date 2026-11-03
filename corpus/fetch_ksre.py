# /// script
# requires-python = ">=3.10"
# dependencies = ["pypdf>=5"]
# ///
"""Snapshot K-State Research and Extension crop publications into a RAG corpus.

Facilitator-only. Attendees use the committed snapshot in corpus/docs/ and never
hit the KSRE site live.

    uv run corpus/fetch_ksre.py                    # default crop topics
    uv run corpus/fetch_ksre.py --topics wheat     # one topic
    uv run corpus/fetch_ksre.py --list-only        # print listings as JSONL, change nothing

KSRE publications state: "Contents of this publication may be freely reproduced
for educational purposes. All other rights reserved." Every document keeps its
credit line in its header and in manifest.jsonl.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path

BASE = "https://bookstore.ksre.ksu.edu"
UA = "heartland-rag-workshop corpus snapshot (educational use)"
DEFAULT_TOPICS = [
    "wheat", "sorghum", "corn", "soybeans", "canola", "sunflower",
    "alfalfa", "forages", "pests", "various", "other", "cotton",
]
HERE = Path(__file__).resolve().parent
ITEM_RE = re.compile(r'href="https://bookstore\.ksre\.ksu\.edu/item/([a-z0-9-]+_([A-Z]+[0-9]+[A-Z]?))"')
PAGE_RE = re.compile(r'\?page=(\d+)"')


@dataclass
class Pub:
    id: str
    slug: str
    title: str = ""
    authors: list[str] = field(default_factory=list)
    published: str = ""
    revised: str = ""
    description: str = ""
    topics: list[str] = field(default_factory=list)
    url: str = ""
    download_url: str = ""
    pages: int = 0
    sha256: str = ""
    status: str = "listed"

    @property
    def credit(self) -> str:
        date = self.revised or self.published
        who = ", ".join(self.authors) or "K-State Research and Extension"
        return f"{who}, {self.title}, Kansas State University, {date}."


def get(url: str, delay: float, attempts: int = 6) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(attempts):
        time.sleep(delay)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 502, 503) or attempt == attempts - 1:
                raise
            wait = e.headers.get("Retry-After")
            wait = float(wait) if wait and wait.isdigit() else 15 * (attempt + 1)
            print(f"  {e.code} on {url}; waiting {wait:.0f}s", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError("unreachable")


def text_of(fragment: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def list_topic(topic: str, delay: float) -> list[tuple[str, str]]:
    found: dict[str, str] = {}
    page, last = 1, 1
    while page <= last:
        url = f"{BASE}/topic/crops/{topic}" + (f"?page={page}" if page > 1 else "")
        s = get(url, delay).decode("utf-8", "replace")
        for slug, pid in ITEM_RE.findall(s):
            found.setdefault(pid, slug)
        last = max([last, *map(int, PAGE_RE.findall(s))])
        page += 1
    return [(pid, slug) for pid, slug in found.items()]


def read_item(pub: Pub, delay: float) -> None:
    pub.url = f"{BASE}/item/{pub.slug}"
    s = get(pub.url, delay).decode("utf-8", "replace")
    m = re.search(r'<h2><small class="lead text-muted">[^<]*</small>(.*?)</h2>', s, re.S)
    pub.title = text_of(m.group(1)) if m else pub.slug.rsplit("_", 1)[0].replace("-", " ")
    pub.authors = [text_of(a) for a in re.findall(r'href="https://bookstore\.ksre\.ksu\.edu/author/[^"]+">(.*?)</a>', s)]
    if m := re.search(r"Published Date:\s*([^<]+)<", s):
        pub.published = m.group(1).strip()
    if m := re.search(r"Revision Date:\s*([^<]+)<", s):
        pub.revised = m.group(1).strip()
    if m := re.search(r'<div class="flex-fill">(.*?)</div>', s, re.S):
        pub.description = text_of(m.group(1))
    if m := re.search(r'href="(https://bookstore\.ksre\.ksu\.edu/download/[^"]+)"', s):
        pub.download_url = m.group(1)


def pdf_to_text(data: bytes) -> tuple[str, int]:
    import io
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(data))
    pages = []
    for i, page in enumerate(reader.pages, 1):
        body = (page.extract_text() or "").rstrip()
        body = "\n".join(line.rstrip() for line in body.splitlines())
        pages.append(f"<!-- page {i} -->\n{body}")
    return "\n\n".join(pages), len(reader.pages)


def write_doc(pub: Pub, body: str, out: Path) -> None:
    header = {
        "id": pub.id,
        "title": pub.title,
        "authors": pub.authors,
        "published": pub.published,
        "revised": pub.revised,
        "topics": pub.topics,
        "source_url": pub.url,
        "credit": pub.credit,
        "license_note": "Contents may be freely reproduced for educational purposes. All other rights reserved.",
    }
    lines = ["---", *(f"{k}: {json.dumps(v)}" for k, v in header.items()), "---", "", body, ""]
    (out / f"{pub.id}.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topics", default=",".join(DEFAULT_TOPICS))
    ap.add_argument("--delay", type=float, default=2.0, help="seconds between requests")
    ap.add_argument("--list-only", action="store_true",
                    help="print listings as JSONL to stdout; write no files")
    ap.add_argument("--out", type=Path, default=HERE)
    args = ap.parse_args()

    docs, pdfs = args.out / "docs", args.out / ".pdf-cache"
    if not args.list_only:
        docs.mkdir(parents=True, exist_ok=True)
        pdfs.mkdir(parents=True, exist_ok=True)

    pubs: dict[str, Pub] = {}
    for topic in args.topics.split(","):
        items = list_topic(topic, args.delay)
        print(f"{topic}: {len(items)} publications", file=sys.stderr)
        for pid, slug in items:
            pubs.setdefault(pid, Pub(id=pid, slug=slug)).topics.append(topic)

    for n, pub in enumerate(sorted(pubs.values(), key=lambda p: p.id), 1):
        try:
            read_item(pub, args.delay)
            if args.list_only or not pub.download_url:
                pub.status = "no-download" if not pub.download_url else "listed"
                continue
            cached = pdfs / f"{pub.id}.pdf"
            data = cached.read_bytes() if cached.exists() else get(pub.download_url, args.delay)
            if not data.startswith(b"%PDF"):
                pub.status = "not-pdf"
                continue
            cached.write_bytes(data)
            pub.sha256 = hashlib.sha256(data).hexdigest()
            body, pub.pages = pdf_to_text(data)
            if len(re.sub(r"<!-- page \d+ -->", "", body).strip()) < 400:
                pub.status = "stub"
                continue
            write_doc(pub, body, docs)
            pub.status = "ok"
        except Exception as e:  # keep the crawl going; the manifest records the failure
            pub.status = f"error: {type(e).__name__}: {e}"
        print(f"[{n}/{len(pubs)}] {pub.id} {pub.status} {pub.title[:60]}", file=sys.stderr)

    lines = [json.dumps({**asdict(pub), "credit": pub.credit}) + "\n"
             for pub in sorted(pubs.values(), key=lambda p: p.id)]
    if args.list_only:
        sys.stdout.writelines(lines)
        return 0
    with (args.out / "manifest.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        f.writelines(lines)
    ok = sum(p.status == "ok" for p in pubs.values())
    if set(args.topics.split(",")) == set(DEFAULT_TOPICS):
        # A full run defines the snapshot: drop documents that are no longer
        # listed or no longer extract, so docs/ always matches the manifest.
        keep = {p.id for p in pubs.values() if p.status == "ok"}
        for stale in docs.glob("*.md"):
            if stale.stem not in keep:
                stale.unlink()
                print(f"removed {stale.name}", file=sys.stderr)
    print(f"done: {ok}/{len(pubs)} documents in {docs}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
