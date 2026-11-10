"""Test rag-check's PASS/FAIL lines with a temporary export and a stand-in model."""
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from rag_symposium.check import run_checks


class FakeEmbedder:
    """Stands in for the real model so the test needs no download."""
    name = "fake-model"

    def encode(self, texts):
        return np.ones((len(texts), 4), dtype=np.float32) / 2


class BrokenEmbedder(FakeEmbedder):
    def encode(self, texts):
        raise OSError("not cached")


class CheckTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / "records.jsonl"

    def publish(self):
        records = [{"id": "DOC-p1", "title": "Guidance on record keeping", "text": "record keeping rules",
                    "source": "s"}]
        self.path.write_text("\n".join(json.dumps(r) for r in records), encoding="utf-8")

    def test_all_pass_with_an_export_and_a_model(self):
        self.publish()
        results = run_checks(self.path, FakeEmbedder())
        self.assertEqual([passed for passed, _ in results], [True] * 4)
        self.assertIn("1 records", results[0][1])
        self.assertIn("first DOC-p1", results[3][1])

    def test_missing_export_and_model_fail_every_dependent_check(self):
        results = run_checks(self.path, BrokenEmbedder())
        self.assertEqual([passed for passed, _ in results], [False] * 4)
        self.assertIn("rag-ingest", results[0][1])
        self.assertIn("did not load offline", results[1][1])

    def test_a_query_with_no_results_fails(self):
        self.publish()
        results = run_checks(self.path, FakeEmbedder(), query="zebra")
        self.assertEqual([passed for passed, _ in results], [True, True, False, True])


if __name__ == "__main__":
    unittest.main()
