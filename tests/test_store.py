"""Test the data adapter directly, without MCP or a language model.

Each test gets a temporary export and deletes it afterward. Tiny artificial
strings keep the tests predictable; they are not an attendee dataset. Test names
describe the behavior that future adapters should continue to provide.
"""
import json
import tempfile
import unittest
from pathlib import Path

from rag_symposium.store import RecordStore


class StoreTests(unittest.TestCase):
    def setUp(self):
        """Give each test isolated data so test order cannot change the result."""
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / "records.jsonl"
        self.store = RecordStore(self.path)

    def publish(self, records):
        """Act as a minimal ingestion writer: serialize one object per line."""
        self.path.write_text("\n".join(json.dumps(r) for r in records), encoding="utf-8")

    @staticmethod
    def record(id="record-1", text="alpha beta", **fields):
        """Build a valid neutral record; tests override only the relevant fields."""
        return dict(id=id, title="Test record", text=text, source="test-source", **fields)

    def test_empty_start_does_not_create_data(self):
        """An attendee can connect before ingestion; reads never seed a dataset."""
        self.assertFalse(self.store.status()["data_available"])
        self.assertEqual(self.store.search("anything")["matches"], [])
        self.assertFalse(self.path.exists())

    def test_keyword_ranking_provenance_and_no_matches(self):
        """Rank distinct whole-word matches and retain the citation/source link."""
        self.publish([self.record("a", "alpha"), self.record("b", "alpha beta")])
        matches = self.store.search("ALPHA beta")["matches"]
        self.assertEqual([r["id"] for r in matches], ["b", "a"])
        self.assertEqual(matches[0]["citation"], "[b]")
        self.assertEqual(matches[0]["source"], "test-source")
        self.assertEqual(self.store.search("alphabet")["matches"], [])
        self.assertEqual(len(self.store.search("alpha", limit=1)["matches"]), 1)

    def test_bounded_read_and_metadata(self):
        """Excerpts stay small; repeated reads reconstruct the exact original text."""
        text = "x" * 700 + " needle " + "y" * 700
        self.publish([self.record(text=text, metadata={"page": 2})])
        match = self.store.search("needle")["matches"][0]
        self.assertLessEqual(len(match["text"]), 600)
        self.assertIn("needle", match["text"])
        parts, offset = [], 0
        while offset is not None:
            result = self.store.get("record-1", offset=offset, max_chars=100)
            parts.append(result["text"])
            self.assertEqual(result["metadata"], {"page": 2})
            offset = result["next_offset"]
        self.assertEqual("".join(parts), text)

    def test_excerpt_centres_on_most_matched_words(self):
        """A common word near the top should not pull the excerpt away from the answer."""
        text = "the cover page " + "filler " * 300 + "the seeding rate for wheat is listed here"
        self.publish([self.record(text=text, metadata={"published": "2025"})])
        match = self.store.search("the seeding rate for wheat")["matches"][0]
        self.assertIn("seeding rate for wheat", match["text"])
        self.assertNotIn("cover", match["text"])
        self.assertEqual(match["metadata"], {"published": "2025"})

    def test_replacement_and_deletion_visible_without_restart(self):
        """Republishing an export changes the next call without recreating the store."""
        self.publish([self.record()])
        self.assertEqual(self.store.status()["record_count"], 1)
        replacement = self.path.with_suffix(".tmp")
        replacement.write_text(json.dumps(self.record(text="gamma")), encoding="utf-8")
        replacement.replace(self.path)
        self.assertEqual(self.store.search("alpha")["matches"], [])
        self.assertEqual(self.store.get("record-1")["text"], "gamma")
        self.path.unlink()
        self.assertEqual(self.store.status()["record_count"], 0)

    def test_invalid_exports_fail_explicitly(self):
        """Broken or ambiguous input must report an error rather than disappear."""
        for records in ([self.record(), self.record()], [{"id": "missing"}],
                        [self.record(metadata=[])], [self.record(id="../escape")], [None]):
            with self.subTest(records=records):
                self.publish(records)
                with self.assertRaisesRegex(ValueError, "line"):
                    self.store.status()
        self.path.write_text("not JSON", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "line 1"):
            self.store.search("alpha")

    def test_invalid_queries_and_reads(self):
        """Bound requests and treat IDs as record keys, never arbitrary file paths."""
        self.publish([self.record()])
        for query in ("", "   ", "!!!", "a" * 2001):
            with self.assertRaises(ValueError):
                self.store.search(query)
        for limit in (0, 11, True):
            with self.assertRaises(ValueError):
                self.store.search("alpha", limit)
        for args in ({"offset": -1}, {"offset": 100}, {"max_chars": 0}, {"max_chars": 10001}):
            with self.assertRaises(ValueError):
                self.store.get("record-1", **args)
        with self.assertRaisesRegex(ValueError, "not found"):
            self.store.get("/etc/passwd")


if __name__ == "__main__":
    unittest.main()
