"""Test the data adapter directly, without MCP or a language model.

Each test gets a temporary export and deletes it afterward. Tiny artificial
strings keep the tests predictable; they are not an attendee dataset. Test names
describe the behavior that future adapters should continue to provide.
"""
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

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


class Bm25Tests(unittest.TestCase):
    """The bm25 mode: same records and citations, better ranking, coverage warnings."""

    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / "records.jsonl"
        self.store = RecordStore(self.path, "bm25")

    def publish(self, records):
        self.path.write_text("\n".join(json.dumps(r) for r in records), encoding="utf-8")

    @staticmethod
    def record(id, text, title="Test record", **metadata):
        return dict(id=id, title=title, text=text, source="test-source", metadata=metadata)

    def test_rare_words_outrank_common_ones(self):
        """Keyword mode ties these on word count; bm25 lets the rare word decide."""
        filler = [self.record(f"f{i}", "how do i control the weeds in wheat") for i in range(5)]
        self.publish([*filler, self.record("target", "cheatgrass is a weed in wheat")])
        query = "how do i control cheatgrass in wheat"
        self.assertEqual(self.store.search(query)["matches"][0]["id"], "target")
        self.assertNotEqual(RecordStore(self.path).search(query)["matches"][0]["id"], "target")

    def test_pronouns_do_not_decide_the_ranking(self):
        """Rare-but-meaningless words like "my" must not outweigh the subject."""
        self.publish([*(self.record(f"f{i}", "downy brome is a weed in wheat") for i in range(3)),
                       self.record("chat", "my farm, I plant my wheat early")])
        top = self.store.search("how do I get rid of downy brome in my wheat")["matches"][0]
        self.assertTrue(top["id"].startswith("f"))

    def test_publication_id_ranks_its_own_pages_first(self):
        """Pages that cite an ID should not outrank the publication itself."""
        self.publish([self.record("EP1-p1", "see MF9 and MF9 again for MF9 details", document_id="EP1"),
                      self.record("MF9-p1", "variety guide text", document_id="MF9")])
        match = self.store.search("MF9")["matches"][0]
        self.assertEqual(match["id"], "MF9-p1")
        self.assertTrue(match["id_match"])

    def test_plurals_match_and_excerpt_uses_the_word_as_written(self):
        self.publish([self.record("a", "x " * 400 + "these fungicides protect wheat")])
        match = self.store.search("fungicide")["matches"][0]
        self.assertEqual(match["matched_terms"], ["fungicides"])
        self.assertIn("fungicides protect", match["text"])

    def test_reports_words_no_result_contains(self):
        self.publish([self.record("a", "pistachio trees"), self.record("b", "wheat in kansas")])
        result = self.store.search("can I grow quinoa in kansas")
        self.assertEqual(result["missing_terms"], ["grow", "quinoa"])
        self.assertEqual(result["unknown_terms"], ["grow", "quinoa"])
        self.assertIn("No result contains: grow, quinoa", result["notice"])
        self.assertEqual(result["matches"][0]["missing_terms"], ["grow", "quinoa"])
        self.assertEqual(self.store.search("wheat kansas")["missing_terms"], [])

    def test_republished_export_rebuilds_the_index(self):
        self.publish([self.record("a", "alpha")])
        self.assertEqual(self.store.search("alpha")["matches"][0]["id"], "a")
        replacement = self.path.with_suffix(".tmp")
        replacement.write_text(json.dumps(self.record("b", "beta gamma delta")), encoding="utf-8")
        replacement.replace(self.path)
        self.assertEqual([m["id"] for m in self.store.search("beta")["matches"]], ["b"])
        self.assertEqual(self.store.status()["search_mode"], "bm25")

    def test_hybrid_finds_different_words_for_the_same_thing(self):
        """A fake embedder that knows two synonyms stands in for the real model."""
        class Synonyms:
            def encode(self, texts):
                rows = [[float("cheat" in t or "cheatgrass" in t), float("hay" in t), 1.0] for t in texts]
                vectors = np.array(rows, dtype=np.float32)
                return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
        self.publish([self.record("brome", "cheat is a weedy brome in winter wheat"),
                      self.record("bales", "store hay bales dry"),
                      self.record("MF9-p1", "unrelated text", document_id="MF9")])
        bm25 = self.store.search("cheatgrass")["matches"]
        self.assertEqual(bm25, [])
        hybrid = RecordStore(self.path, "hybrid", embedder=Synonyms())
        match = hybrid.search("cheatgrass")["matches"][0]
        self.assertEqual(match["id"], "brome")
        self.assertEqual(match["ranks"], {"bm25": None, "semantic": 1})
        self.assertEqual(hybrid.search("MF9 hay")["matches"][0]["id"], "MF9-p1")
        self.assertEqual(hybrid.status()["search_mode"], "hybrid")

    def test_unknown_mode_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "search mode"):
            RecordStore(self.path, "semantic")


class DocumentIdTests(unittest.TestCase):
    """IDs and aliases written the way people write them still find their document."""

    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / "records.jsonl"
        # A document that cites the others many times, so only ID matching
        # (not word counts) can put the named document first.
        citing = "see M-24-10, EO 14110 and NIST AI 600-1. " * 5
        records = [self.page("MEMO-p1", "MEMO", [], citing)]
        for doc_id, aliases, texts in (
                ("M-24-10", ["OMB M-24-10"], ["agency use of automated tools"]),
                ("EO-14110", ["EO 14110", "Executive Order 14110"], ["an order on automated tools"]),
                ("NIST-AI-600-1", ["NIST AI 600-1"],
                 ["a profile for automated tools", "content provenance and labeling"])):
            records += [self.page(f"{doc_id}-p{n}", doc_id, aliases, text)
                        for n, text in enumerate(texts, 1)]
        self.path.write_text("\n".join(json.dumps(r) for r in records), encoding="utf-8")
        self.store = RecordStore(self.path, "bm25")

    @staticmethod
    def page(id, document_id, aliases, text):
        return dict(id=id, title="Test record", text=text, source="test-source",
                    metadata={"document_id": document_id, "aliases": aliases})

    def top(self, query, store=None):
        match = (store or self.store).search(query)["matches"][0]
        return match["metadata"]["document_id"], match["id_match"]

    def test_ids_and_aliases_match_however_they_are_written(self):
        for query, document in (("M-24-10", "M-24-10"), ("omb m-24-10", "M-24-10"),
                                ("m 24 10", "M-24-10"), ("M2410", "M-24-10"),
                                ("EO 14110", "EO-14110"), ("eo-14110", "EO-14110"),
                                ("Executive Order 14110", "EO-14110"),
                                ("NIST AI 600-1", "NIST-AI-600-1")):
            with self.subTest(query=query):
                self.assertEqual(self.top(query), (document, True))

    def test_id_in_a_question_picks_the_page_about_the_rest(self):
        result = self.store.search("what does NIST AI 600-1 say about provenance")
        self.assertEqual(result["matches"][0]["id"], "NIST-AI-600-1-p2")
        self.assertEqual([m["id_match"] for m in result["matches"][:2]], [True, True])
        # The ID's own numbers are not reported as words the results lack.
        self.assertEqual(result["missing_terms"], [])
        self.assertNotIn("600", result["matches"][1]["missing_terms"])

    def test_ids_match_only_on_whole_words(self):
        """14110 inside a longer number, or a prefix of an ID, is not the ID."""
        for query in ("EO 141105", "EO 214110", "M-24-1", "NIST AI 600"):
            with self.subTest(query=query):
                matches = self.store.search(query)["matches"]
                self.assertTrue(matches)
                self.assertFalse(any(m["id_match"] for m in matches))

    def test_hybrid_puts_aliases_first_too(self):
        class Flat:
            def encode(self, texts):
                return np.ones((len(texts), 2), dtype=np.float32) / np.sqrt(2)
        hybrid = RecordStore(self.path, "hybrid", embedder=Flat())
        self.assertEqual(self.top("omb m-24-10 automated tools", hybrid), ("M-24-10", True))


class DocumentStatusTests(unittest.TestCase):
    """A rescinded or superseded document says so next to its title."""

    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / "records.jsonl"
        records = [
            dict(id="OLD-p1", title="Old guidance", text="guidance on automated tools", source="s",
                 metadata={"document_id": "OLD", "published": "Oct 2023", "revised": "",
                           "status": "rescinded", "replaced_by": ["NEW"]}),
            dict(id="NEW-p1", title="New guidance", text="guidance on automated tools", source="s",
                 metadata={"document_id": "NEW", "published": "Apr 2025", "revised": "May 2025",
                           "status": "in force", "replaced_by": []}),
            dict(id="PLAIN", title="No status", text="guidance on automated tools", source="s")]
        self.path.write_text("\n".join(json.dumps(r) for r in records), encoding="utf-8")

    def test_search_and_read_show_document_status(self):
        expected = {"OLD-p1": "rescinded; published Oct 2023; replaced by NEW",
                    "NEW-p1": "in force; revised May 2025"}
        for mode in ("keyword", "bm25"):
            store = RecordStore(self.path, mode)
            with self.subTest(mode=mode):
                matches = {m["id"]: m for m in store.search("guidance")["matches"]}
                self.assertEqual({k: m.get("document_status") for k, m in matches.items()},
                                 {**expected, "PLAIN": None})
        store = RecordStore(self.path)
        self.assertEqual(store.get("OLD-p1")["document_status"], expected["OLD-p1"])
        self.assertNotIn("document_status", store.get("PLAIN"))

if __name__ == "__main__":
    unittest.main()
