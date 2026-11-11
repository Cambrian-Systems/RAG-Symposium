"""Tests for rag-add: each supported file type becomes a corpus document that ingests.

The files are built here, in a temporary folder: a two-page PDF written by hand,
a Word file assembled from its XML, a web page and a text file.
"""
import tempfile
import unittest
import zipfile
from pathlib import Path

from rag_symposium import convert
from rag_symposium.ingest import ingest, read_document


def pdf_bytes(pages: list[str]) -> bytes:
    """A minimal valid PDF with one line of Helvetica text per page ('' = a blank page)."""
    objects = ["<< /Type /Catalog /Pages 2 0 R >>", None,
               "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    kids = []
    for text in pages:
        stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET" if text else ""
        objects.append(f"<< /Length {len(stream)} >>\nstream\n{stream}\nendstream")
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                       f"/Resources << /Font << /F1 3 0 R >> >> /Contents {len(objects)} 0 R >>")
        kids.append(f"{len(objects)} 0 R")
    objects[1] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(kids)} >>"
    out, offsets = b"%PDF-1.4\n", []
    for number, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n{body}\nendobj\n".encode("latin-1")
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    out += "".join(f"{offset:010d} 00000 n \n" for offset in offsets).encode()
    out += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return out


DOCX_BODY = """<?xml version="1.0" encoding="UTF-8"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>
<w:p><w:r><w:t>Lab AI policy</w:t></w:r></w:p>
<w:p><w:r><w:t xml:space="preserve">Students may use AI tools </w:t></w:r><w:r><w:t>with disclosure.</w:t></w:r></w:p>
<w:tbl><w:tr><w:tc><w:p><w:r><w:t>Tool</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Allowed</w:t></w:r></w:p></w:tc></w:tr>
<w:tr><w:tc><w:p><w:r><w:t>Chatbot</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Yes</w:t></w:r></w:p></w:tc></w:tr></w:tbl>
</w:body></w:document>"""

HTML_PAGE = """<html><head><title>Data &amp; AI guidance</title><style>p { color: red }</style></head>
<body><nav>Home | About</nav><main><h1>Guidance</h1><p>Do not paste participant data into a chatbot.</p>
<script>track()</script></main><footer>Contact us</footer></body></html>"""


class ConvertTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="rag-add-test-")
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name)
        self.out = self.folder / "docs"

    def write(self, name: str, data) -> Path:
        path = self.folder / name
        path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
        return path

    def test_pdf_keeps_its_pages(self):
        """Each PDF page becomes one page marker, and a blank page keeps its number."""
        source = self.write("Grant Rules (2026).pdf", pdf_bytes(["Six applications per year.", "", "Appeals go to the dean."]))
        done = convert.convert(source, self.out, issuer="Research office", status="in force")
        self.assertEqual((done["id"], done["pages"], done["empty_pages"]), ("GRANT-RULES-2026", 3, 1))
        header, pages = read_document(self.out / "GRANT-RULES-2026.md")
        self.assertEqual(pages, [(1, "Six applications per year."), (2, ""), (3, "Appeals go to the dean.")])
        self.assertEqual((header["title"], header["issuer"], header["status"], header["source_url"]),
                         ("Grant Rules (2026)", "Research office", "in force", "Grant Rules (2026).pdf"))

    def test_a_pdf_with_no_text_is_refused(self):
        """A scanned PDF has pages but no text layer; say so instead of writing an empty document."""
        source = self.write("scan.pdf", pdf_bytes(["", ""]))
        with self.assertRaisesRegex(ValueError, "OCR"):
            convert.convert(source, self.out)
        self.assertFalse((self.out / "SCAN.md").exists())

    def test_word_file_paragraphs_and_tables(self):
        """Runs join into paragraphs, and a table row becomes one line."""
        source = self.folder / "policy.docx"
        with zipfile.ZipFile(source, "w") as archive:
            archive.writestr("word/document.xml", DOCX_BODY)
        done = convert.convert(source, self.out)
        self.assertEqual(done["title"], "Lab AI policy")  # No title in the file, so its first line.
        _, pages = read_document(self.out / "POLICY.md")
        self.assertEqual(pages[0][1], "Lab AI policy\nStudents may use AI tools with disclosure.\n"
                                      "Tool | Allowed\nChatbot | Yes")

    def test_web_page_keeps_only_the_visible_main_text(self):
        """Navigation, scripts, styles and the footer are left out; the <title> becomes the title."""
        done = convert.convert(self.write("guidance.html", HTML_PAGE), self.out, source_url="https://example.edu/guidance")
        self.assertEqual(done["title"], "Data & AI guidance")
        header, pages = read_document(self.out / "GUIDANCE.md")
        self.assertEqual(pages[0][1], "Guidance\nDo not paste participant data into a chatbot.")
        self.assertEqual(header["source_url"], "https://example.edu/guidance")

    def test_long_text_is_cut_into_sections_at_line_ends(self):
        """Text has no page breaks, so sections of about 3,000 characters stand in for pages."""
        lines = [f"Line {n}: " + "word " * 20 for n in range(100)]
        done = convert.convert(self.write("notes.txt", "# Meeting notes\n" + "\n".join(lines)), self.out)
        self.assertEqual(done["title"], "Meeting notes")
        _, pages = read_document(self.out / "NOTES.md")
        self.assertGreater(len(pages), 2)
        self.assertTrue(all(len(text) <= convert.SECTION_SIZE + 200 for _, text in pages))
        # No line is split or lost between sections.
        self.assertEqual([line for _, text in pages for line in text.splitlines()][1:], [line.strip() for line in lines])

    def test_existing_document_is_not_overwritten(self):
        """A second file with the same ID is refused unless --replace or another --id is given."""
        convert.convert(self.write("memo.txt", "First memo"), self.out)
        with self.assertRaisesRegex(ValueError, "already exists"):
            convert.convert(self.write("memo.md", "Second memo"), self.out)
        convert.convert(self.folder / "memo.md", self.out, id="MEMO-2")
        convert.convert(self.folder / "memo.md", self.out, replace=True)
        self.assertEqual(read_document(self.out / "MEMO.md")[1], [(1, "Second memo")])
        self.assertEqual(read_document(self.out / "MEMO-2.md")[0]["id"], "MEMO-2")

    def test_unsupported_and_bad_ids(self):
        with self.assertRaisesRegex(ValueError, "unsupported file type"):
            convert.convert(self.write("slides.pptx", b"x"), self.out)
        with self.assertRaisesRegex(ValueError, "may only contain"):
            convert.convert(self.write("a.txt", "text"), self.out, id="bad id/")
        self.assertEqual(convert.document_id("Résumé – final (v2)"), "RESUME-FINAL-V2")
        self.assertEqual(convert.document_id("政策"), "DOCUMENT")

    def test_converted_documents_ingest(self):
        """The whole path: files in, corpus documents out, records published with page numbers."""
        convert.convert(self.write("rules.pdf", pdf_bytes(["Page one text.", "Page two text."])), self.out)
        convert.convert(self.write("guidance.html", HTML_PAGE), self.out)
        summary = ingest(self.out, self.folder / "export.jsonl")
        self.assertEqual((summary["documents"], summary["records"]), (2, 3))
        export = (self.folder / "export.jsonl").read_text(encoding="utf-8")
        self.assertIn('"id": "RULES-p2"', export)
        self.assertIn('"pages": [2]', export)


if __name__ == "__main__":
    unittest.main()
