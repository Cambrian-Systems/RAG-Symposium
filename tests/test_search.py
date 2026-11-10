"""Test that rag-search prints each result's date and status on its line."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from rag_symposium import search


class SearchCommandTests(unittest.TestCase):
    def run_search(self, records, query):
        """Publish records to a temporary export and capture rag-search's output."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "records.jsonl"
            path.write_text("\n".join(json.dumps(r) for r in records), encoding="utf-8")
            output = io.StringIO()
            argv = ["rag-search", query, "--data", str(path), "--mode", "bm25"]
            with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
                search.main()
        return output.getvalue()

    def test_status_appears_next_to_the_date(self):
        output = self.run_search([
            {"id": "OLD-p1", "title": "Old guidance", "text": "guidance text", "source": "s",
             "metadata": {"published": "Oct 2023", "status": "rescinded"}},
            {"id": "NEW-p1", "title": "New guidance", "text": "guidance text", "source": "s",
             "metadata": {"published": "Apr 2025", "status": "in force"}}], "guidance")
        self.assertRegex(output, r"OLD-p1 +Oct 2023 +rescinded +Old guidance")
        self.assertRegex(output, r"NEW-p1 +Apr 2025 +in force +New guidance")

    def test_no_status_column_without_statuses(self):
        output = self.run_search([{"id": "A", "title": "Plain", "text": "guidance", "source": "s",
                                   "metadata": {"published": "2025"}}], "guidance")
        self.assertIn("1. A            2025      Plain", output)


if __name__ == "__main__":
    unittest.main()
