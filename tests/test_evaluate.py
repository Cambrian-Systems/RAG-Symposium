"""Test rag-eval's scoring on tiny artificial records and questions."""
import json
import tempfile
import unittest
from pathlib import Path

from rag_symposium.evaluate import evaluate, load_questions, rank_of
from rag_symposium.store import RecordStore


def match(document_id, pages=(1,)):
    """A search result as rank_of sees it: only the ID and metadata matter."""
    return {"id": f"{document_id}-p{pages[0]}", "metadata": {"document_id": document_id, "pages": list(pages)}}


class EvaluateTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.folder = Path(folder.name)

    def write(self, name, rows):
        path = self.folder / name
        path.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
        return path

    def test_rank_by_publication_pages_and_all(self):
        results = [match("A"), match("B", (3,)), match("C")]
        self.assertEqual(rank_of(results, {"expect": ["B"]}), 2)
        self.assertEqual(rank_of(results, {"expect": ["B"], "pages": [3, 4]}), 2)
        self.assertIsNone(rank_of(results, {"expect": ["B"], "pages": [9]}))
        self.assertEqual(rank_of(results, {"expect": ["C", "A"]}), 1)
        self.assertEqual(rank_of(results, {"expect": ["C", "A"], "all": True}), 3)
        self.assertIsNone(rank_of(results, {"expect": ["A", "Z"], "all": True}))

    def test_scores_and_not_found_warnings(self):
        records = [{"id": f"{d}-p1", "title": d, "text": text, "source": "s",
                    "metadata": {"document_id": d, "pages": [1]}}
                   for d, text in (("HAY", "hay fires start from excess moisture"),
                                   ("WHEAT", "wheat seeding rates in kansas"))]
        data = self.write("records.jsonl", records)
        questions = load_questions(self.write("q.jsonl", [
            {"id": "q1", "question": "what causes hay fires", "expect": ["HAY"], "category": "fact"},
            {"id": "q2", "question": "kansas wheat seeding", "expect": ["HAY"]},
            {"id": "q3", "question": "pistachio orchards in kansas", "expect": []}]))
        result = evaluate(RecordStore(data, "bm25"), questions, k=5)
        summary = result["summary"]["all"]
        self.assertEqual(summary["hit@1"], 0.5)
        self.assertEqual(summary["hit@k"], 0.5)
        self.assertEqual((summary["unanswerable"], summary["flagged"]), (1, 1))
        self.assertEqual(summary["false_warnings"], 1)  # q1: "causes" is in no result
        self.assertEqual(result["summary"]["categories"]["fact"]["hit@1"], 1.0)
        keyword = evaluate(RecordStore(data, "keyword"), questions, k=5)
        self.assertEqual(keyword["summary"]["all"]["flagged"], 0)

    def test_bad_question_files_name_the_line(self):
        for row in ({"question": "no id", "expect": []}, {"id": "x", "question": "q"},
                    {"id": "x", "question": "q", "expect": "MF991"},
                    {"id": "x", "question": "q", "expect": [], "pages": ["3"]}):
            with self.subTest(row=row), self.assertRaisesRegex(ValueError, "line 2"):
                load_questions(self.write("bad.jsonl", [{"id": "ok", "question": "q", "expect": []}, row]))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            load_questions(self.write("dup.jsonl", [{"id": "a", "question": "q", "expect": []}] * 2))

    def test_shipped_starter_set_is_valid(self):
        questions = load_questions(Path(__file__).parent.parent / "evals" / "starter.jsonl")
        self.assertGreaterEqual(len(questions), 20)


if __name__ == "__main__":
    unittest.main()
