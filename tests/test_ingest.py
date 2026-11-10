"""Test corpus ingestion: header parsing, chunking modes and safe publishing.

Small artificial documents keep chunk boundaries predictable. The final test
ingests the committed corpus into a temporary export and loads it through the
server's own RecordStore, so a corpus change that breaks the contract fails here.
"""
import json
import tempfile
import unittest
from pathlib import Path

from rag_symposium.ingest import ingest, read_document, windows
from rag_symposium.store import RecordStore

CORPUS = Path(__file__).resolve().parent.parent / "corpus" / "docs"


def document(doc_id="DOC1", pages=("first page text", "second page text"), **fields):
    """Build corpus-format Markdown: a JSON-valued header, then marked pages.

    fields adds or replaces header fields; a value of None leaves the field out.
    """
    header = {"id": doc_id, "title": f"Title {doc_id}", "published": "Aug 2025",
              "revised": "", "topics": ["testing"], "source_url": f"https://example.test/{doc_id}",
              "credit": f"Credit {doc_id}", **fields}
    header = {k: v for k, v in header.items() if v is not None}
    body = "\n\n".join(f"<!-- page {n} -->\n{text}" for n, text in enumerate(pages, 1))
    return "---\n" + "\n".join(f"{k}: {json.dumps(v)}" for k, v in header.items()) + "\n---\n\n" + body + "\n"


class IngestTests(unittest.TestCase):
    def setUp(self):
        """Give each test its own corpus folder and export path."""
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.corpus = Path(folder.name) / "docs"
        self.corpus.mkdir()
        self.output = Path(folder.name) / "data" / "documents.jsonl"

    def write(self, name, content):
        (self.corpus / name).write_text(content, encoding="utf-8")

    def exported(self):
        return [json.loads(line) for line in self.output.read_text(encoding="utf-8").splitlines()]

    def test_header_and_pages_are_parsed(self):
        """Header values are JSON; page markers become numbered page texts."""
        self.write("DOC1.md", document())
        header, pages = read_document(self.corpus / "DOC1.md")
        self.assertEqual(header["published"], "Aug 2025")
        self.assertEqual(pages, [(1, "first page text"), (2, "second page text")])

    def test_page_mode_keeps_provenance_and_skips_blank_pages(self):
        """One record per nonblank page; IDs and metadata identify the page."""
        self.write("DOC1.md", document(pages=("alpha", "   ", "gamma")))
        summary = ingest(self.corpus, self.output, mode="page")
        records = self.exported()
        self.assertEqual(summary["records"], 2)
        self.assertEqual([r["id"] for r in records], ["DOC1-p1", "DOC1-p3"])
        self.assertEqual(records[1]["metadata"]["pages"], [3])
        self.assertEqual(records[1]["metadata"]["document_id"], "DOC1")
        self.assertEqual(records[1]["source"], "https://example.test/DOC1")

    def test_status_and_aliases_reach_every_record(self):
        """Status, issuer, aliases and replacement links ride along in metadata."""
        self.write("DOC1.md", document(
            aliases=["Doc 1", "D-1"], issuer="Test Office", status="superseded",
            status_note="Replaced by DOC2 in 2025.", replaces=["DOC0"], replaced_by=["DOC2"]))
        ingest(self.corpus, self.output)
        for record in self.exported():
            metadata = record["metadata"]
            self.assertEqual(metadata["aliases"], ["Doc 1", "D-1"])
            self.assertEqual(metadata["issuer"], "Test Office")
            self.assertEqual(metadata["status"], "superseded")
            self.assertEqual(metadata["status_note"], "Replaced by DOC2 in 2025.")
            self.assertEqual((metadata["replaces"], metadata["replaced_by"]), (["DOC0"], ["DOC2"]))

    def test_missing_optional_fields_get_empty_defaults(self):
        """A header with only id, title and source_url still ingests."""
        self.write("DOC1.md", document(published=None, revised=None, topics=None, credit=None))
        ingest(self.corpus, self.output)
        metadata = self.exported()[0]["metadata"]
        self.assertEqual((metadata["status"], metadata["issuer"], metadata["aliases"],
                          metadata["replaced_by"], metadata["published"]), ("", "", [], [], ""))

    def test_document_mode_is_one_record_per_file(self):
        self.write("DOC1.md", document())
        self.write("DOC2.md", document("DOC2"))
        ingest(self.corpus, self.output, mode="document")
        records = self.exported()
        self.assertEqual([r["id"] for r in records], ["DOC1", "DOC2"])
        self.assertEqual(records[0]["metadata"]["pages"], [1, 2])

    def test_windows_overlap_cover_text_and_report_pages(self):
        """Windows stay within size, overlap their neighbours and lose no words."""
        words = [f"w{i}" for i in range(400)]
        pages = [(1, " ".join(words[:200])), (2, " ".join(words[200:]))]
        chunks = windows(pages, size=300, overlap=50)
        self.assertTrue(all(len(text) <= 300 for text, _ in chunks))
        seen = set(" ".join(text for text, _ in chunks).split())
        self.assertEqual(seen, set(words))
        self.assertEqual(chunks[0][1], [1])
        self.assertEqual(chunks[-1][1], [2])
        self.assertTrue(any(spanned == [1, 2] for _, spanned in chunks))
        # Overlap: the start of each window repeats the end of the previous one.
        for (previous, _), (current, _) in zip(chunks, chunks[1:]):
            self.assertIn(current.split()[0], previous.split())

    def test_publish_replaces_and_failures_keep_old_export(self):
        """A bad corpus raises before publishing, leaving the last export intact."""
        self.write("DOC1.md", document())
        ingest(self.corpus, self.output)
        before = self.output.read_bytes()
        self.write("DOC2.md", document("DOC1"))  # Second file reuses DOC1's ID.
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            ingest(self.corpus, self.output)
        self.assertEqual(self.output.read_bytes(), before)
        self.assertEqual(list(self.output.parent.glob(".ingest-*")), [])

    def test_missing_header_or_empty_corpus_fail(self):
        with self.assertRaisesRegex(ValueError, "No .md"):
            ingest(self.corpus, self.output)
        self.write("BAD.md", "no header here")
        with self.assertRaisesRegex(ValueError, "header"):
            ingest(self.corpus, self.output)

    @unittest.skipUnless(CORPUS.is_dir(), "workshop corpus not present")
    def test_committed_corpus_loads_in_every_mode(self):
        """The real corpus ingests cleanly and the server accepts the export."""
        for mode in ("page", "window", "document"):
            with self.subTest(mode=mode):
                summary = ingest(CORPUS, self.output, mode=mode)
                store = RecordStore(self.output)
                self.assertEqual(store.status()["record_count"], summary["records"])
                self.assertGreaterEqual(summary["records"], summary["documents"])


if __name__ == "__main__":
    unittest.main()
