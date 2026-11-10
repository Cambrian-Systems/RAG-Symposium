"""Read and search a neutral ingestion export without choosing a dataset.

JSONL means one JSON object per line. This adapter reads small exports into
memory on every call, validates them, and returns source-linked text. It never
writes the file or fetches the source references. Future ingestion/semantic
retrieval can replace this adapter while preserving the tools in server.py.

Two search modes share the same records and citations:
- keyword: counts distinct query words in each record. Simple and easy to fool.
- bm25: weighs rare words above common ones, boosts titles, and puts records
  whose document ID or alias is in the query first. It also reports query words
  no result contains, so a client can notice when the evidence isn't there.
- hybrid: bm25 plus embedding similarity (see embeddings.py), so a question
  can find a record that uses different words for the same thing.
"""
import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

SEARCH_MODES = ("keyword", "bm25", "hybrid")

# Words too common to say anything about a record, plus instructions such as
# "summarize". BM25 leaves them out of scoring: in a corpus of formal documents,
# "my" and "I" are rare, so without this list the one document written in the
# first person outranks pages that actually mention the query's subject.
STOPWORDS = frozenset("""
a about after all also am an and any are as at be been before being between both
but by can could did do does doing during each for from had has have how i if in
into is it its me more most my no not of on or other our should so some such than
that the their them then there these they this those to too under up very was we
were what when where which while who whom why will with would you your
describe explain list say says summarize tell
""".split())

# Standard BM25 constants: K1 limits how much repeating a word helps, B scales
# for record length. TITLE_WEIGHT is how much a title match counts next to text.
K1, B, TITLE_WEIGHT = 1.2, 0.75, 0.5
# Hybrid search fuses each method's top CANDIDATES. RRF_K = 60 is the usual
# constant; it keeps one method's first place from swamping the other's list.
CANDIDATES, RRF_K = 50, 60
# The longest document ID or alias, in words, that a query can match.
MAX_ID_WORDS = 12


def tokens(text: str) -> list[str]:
    """Lowercase word/number tokens, the same way for queries and records."""
    return re.findall(r"\w+", text.casefold())


def id_key(name: str) -> str:
    """Reduce a document ID or alias to letters and digits: "M-24-10" -> "m2410".

    People write the same ID many ways (M-24-10, m 24 10, M‑24‑10 with a
    non-breaking hyphen), so IDs are compared with case, spaces and
    punctuation removed.
    """
    return "".join(re.findall(r"[^\W_]+", name.casefold()))


def id_spans(query: str) -> dict[str, list[str]]:
    """Every run of consecutive query words, joined as id_key would join them.

    Returns joined run -> the words in it. "omb m-24-10" gives "omb", "ombm",
    "m2410", "2410", "10" and so on. Runs start and end on whole words, so the
    alias "EO 14110" matches "eo 14110" and "EO-14110" but not "EO 141105".
    """
    words = re.findall(r"[^\W_]+", query.casefold())
    spans = {}
    for start in range(len(words)):
        for end in range(start + 1, min(len(words), start + MAX_ID_WORDS) + 1):
            spans.setdefault("".join(words[start:end]), words[start:end])
    return spans


def stem(word: str) -> str:
    """Fold simple English plurals together: regulations -> regulation, agencies -> agency.

    This is the Harman "S" stemmer, the lightest common stemmer. It leaves
    other endings (rated vs ratings, governing vs govern) for semantic search.
    """
    if len(word) <= 3 or not word.isalpha():
        return word
    if word.endswith("ies") and not word.endswith(("eies", "aies")):
        return word[:-3] + "y"
    if word.endswith("es") and not word.endswith(("aes", "ees", "oes")):
        return word[:-1]
    if word.endswith("s") and not word.endswith(("us", "ss")):
        return word[:-1]
    return word


def status_line(metadata: dict) -> str:
    """Summarize a document's standing in one line, or "" if it has no status.

    "rescinded; published Oct 2023; replaced by EO 14179" tells an agent, in
    the search result itself, not to present a rescinded rule as current.
    """
    status = metadata.get("status")
    if not isinstance(status, str) or not status.strip():
        return ""
    parts = [status]
    if metadata.get("revised"):
        parts.append(f"revised {metadata['revised']}")
    elif metadata.get("published"):
        parts.append(f"published {metadata['published']}")
    if isinstance(metadata.get("replaced_by"), list) and metadata["replaced_by"]:
        parts.append("replaced by " + ", ".join(map(str, metadata["replaced_by"])))
    return "; ".join(parts)


class RecordStore:
    """One configured file, shared by the MCP status/search/read tools."""

    def __init__(self, path: Path, mode: str = "keyword", embedder=None):
        """Expand ~ and anchor the path now, independent of later directory changes.

        embedder is used only in hybrid mode; it defaults to embeddings.Embedder.
        """
        if mode not in SEARCH_MODES:
            raise ValueError(f"search mode must be one of {', '.join(SEARCH_MODES)}")
        self.path = path.expanduser().resolve()
        self.mode = mode
        if embedder is None and mode == "hybrid":
            from .embeddings import Embedder
            embedder = Embedder()
        self.embedder = embedder
        self._index, self._index_key = None, None

    def records(self) -> list[dict]:
        """Load a complete valid export, or fail with the offending line number."""
        # Read each time so a new ingestion export needs no server restart.
        # A missing export is normal before the first ingestion.
        try:
            stream = self.path.open(encoding="utf-8")
        except FileNotFoundError:
            return []
        records, ids = [], set()
        with stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                    self.validate(record)
                    # IDs become citations and exact lookup keys. Duplicates
                    # would make a citation point to more than one record.
                    if record["id"] in ids:
                        raise ValueError("Duplicate record ID")
                except (ValueError, TypeError) as exc:
                    # Do not silently skip a broken record and make an incomplete
                    # export look successful. The SDK reports this as a tool error.
                    raise ValueError(f"Invalid data on line {line_number}: {exc}") from exc
                ids.add(record["id"])
                records.append(record)
        return records

    @staticmethod
    def validate(record):
        """Require only shared fields; domain-specific attributes go in metadata."""
        if not isinstance(record, dict):
            raise ValueError("Each line must be a JSON object")
        if not isinstance(record.get("id"), str) or not re.fullmatch(r"[\w.-]{1,200}", record["id"]):
            raise ValueError("id must contain 1–200 letters, numbers, underscores, dots or dashes")
        for field in ("title", "text", "source"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                raise ValueError(f"{field} must be nonempty text")
        if not isinstance(record.get("metadata", {}), dict):
            raise ValueError("metadata must be a JSON object")

    def status(self) -> dict:
        """Distinguish a missing export from an existing empty export."""
        records = self.records()
        return {"data_file": str(self.path), "data_available": self.path.is_file(),
                "record_count": len(records), "search_mode": self.mode,
                "notice": "Records come from an ingestion export; this file is empty until ingestion publishes it."}

    @staticmethod
    def reference(record):
        """Keep search and read responses consistent about identity and provenance.

        document_status sits next to the title so it is hard to miss; the full
        status_note stays in metadata.
        """
        reference = {"id": record["id"], "title": record["title"], "source": record["source"],
                     "citation": f"[{record['id']}]"}
        status = status_line(record.get("metadata", {}))
        if status:
            reference["document_status"] = status
        return reference

    def search(self, query: str, limit: int = 5) -> dict:
        """Check the request, then rank records with the configured search mode."""
        if not isinstance(query, str) or not 1 <= len(query.strip()) <= 2000:
            raise ValueError("query must contain 1–2000 characters")
        if type(limit) is not int or not 1 <= limit <= 10:
            raise ValueError("limit must be between 1 and 10")
        # casefold normalizes case; \w+ extracts word/number tokens. Sets mean
        # repeating a word does not inflate its importance. Phrases are not kept.
        terms = set(tokens(query))
        if not terms:
            raise ValueError("query must contain a word or number")
        if self.mode == "bm25":
            return self.search_bm25(query, terms, limit)
        if self.mode == "hybrid":
            return self.search_hybrid(query, terms, limit)
        return self.search_keyword(terms, limit)

    def match(self, record: dict, matched: set[str], **extra) -> dict:
        """Shape one search result: reference, metadata and an excerpt near the hits."""
        start = self.excerpt_start(record["text"], matched)
        end = min(len(record["text"]), start + 600)
        # Metadata rides along so a client can compare attributes such as
        # dates before choosing which records to read in full.
        return {**self.reference(record), "metadata": record.get("metadata", {}),
                "text": record["text"][start:end],
                "offset": start, "next_offset": end if end < len(record["text"]) else None,
                "matched_terms": sorted(matched), **extra}

    def search_keyword(self, terms: set[str], limit: int) -> dict:
        """Return bounded excerpts ranked by distinct query words found in each record.

        This is a transparent keyword baseline, not embedding/semantic search.
        A match provides candidate evidence, not proof that a claim is correct.
        """
        ranked = []
        for record in self.records():
            words = set(re.findall(r"\w+", (record["title"] + " " + record["text"]).casefold()))
            matched = terms & words  # Set intersection: words present in both.
            if matched:
                ranked.append((record, matched))
        # More distinct matches sort first; ID breaks ties deterministically.
        ranked.sort(key=lambda pair: (-len(pair[1]), pair[0]["id"]))
        matches = [self.match(record, matched) for record, matched in ranked[:limit]]
        return {"matches": matches, "search_mode": "keyword",
                "notice": "Matches any query word; ranks by distinct words matched. Not semantic search or answer confidence. Read records before citing claims."}

    def index(self) -> dict:
        """Count words per record once per export version, for BM25 scoring.

        Tokenizing thousands of pages takes about a second, so the counts are
        kept until the file's size or modification time changes.
        """
        try:
            stat = self.path.stat()
            key = (stat.st_mtime_ns, stat.st_size)
        except FileNotFoundError:
            key = None
        if self._index is not None and key == self._index_key:
            return self._index
        records = self.records()
        entries = []
        for record in records:
            metadata = record.get("metadata", {})
            # Names a query can use to mean this record's document: its own ID,
            # its document's ID, and any aliases ("EO 14110"), compared by id_key.
            names = [record["id"], metadata.get("document_id")]
            if isinstance(metadata.get("aliases"), list):
                names += metadata["aliases"]
            ids = {id_key(n) for n in names if isinstance(n, str)} - {""}
            entries.append({"record": record, "text": Counter(map(stem, tokens(record["text"]))),
                            "title": Counter(map(stem, tokens(record["title"]))), "ids": ids})
        index = {"entries": entries}
        for field in ("text", "title"):
            # Document frequency: how many records contain each word at least once.
            frequency = Counter()
            for entry in entries:
                frequency.update(entry[field].keys())
            lengths = [sum(entry[field].values()) for entry in entries]
            index[field] = {"df": frequency, "avg": (sum(lengths) / len(lengths)) if lengths else 0}
        self._index, self._index_key = index, key
        return index

    @staticmethod
    def bm25(counts: Counter, terms: set[str], stats: dict, total: int) -> float:
        """Score one field: rare words count more, and long records don't win by size."""
        length, score = sum(counts.values()), 0.0
        for term in terms:
            tf = counts.get(term, 0)
            if not tf:
                continue
            df = stats["df"][term]
            idf = math.log(1 + (total - df + 0.5) / (df + 0.5))
            norm = 1 - B + B * length / stats["avg"] if stats["avg"] else 1
            score += idf * tf * (K1 + 1) / (tf + K1 * norm)
        return score

    def rank_bm25(self, query: str, terms: set[str]) -> tuple[list, dict, set, set]:
        """Score every record containing a meaningful query word.

        Returns (ranked entries, stem -> word as typed, meaningful stems, stems
        that were part of a matched document ID). Each ranked entry is
        (id_match, score, index entry, stems present).
        """
        index = self.index()
        entries, total = index["entries"], len(index["entries"])
        # Reports use the words as typed; scoring uses their stems.
        typed = {}
        for term in sorted(terms):
            typed.setdefault(stem(term), term)
        stems = set(typed)
        content = {t for t in stems if typed[t] not in STOPWORDS} or stems
        spans = id_spans(query)
        ranked, matched_ids = [], set()
        for entry in entries:
            present = self.present(entry, stems)
            # Someone who types a document ID or alias means that document, not
            # every page that cites it. ID matches sort ahead of everything else.
            hits = {key for key in entry["ids"] if key in spans}
            matched_ids |= hits
            id_match = bool(hits)
            if not id_match and not present & content:
                continue
            score = (self.bm25(entry["text"], content, index["text"], total)
                     + TITLE_WEIGHT * self.bm25(entry["title"], content, index["title"], total))
            ranked.append((id_match, score, entry, present))
        ranked.sort(key=lambda item: (-item[0], -item[1], item[2]["record"]["id"]))
        # "600" and "1" in "NIST AI 600-1" named a document; a page that never
        # spells them out is not missing anything the query asked about.
        id_words = {stem(word) for key in matched_ids for word in spans[key]}
        return ranked, typed, content, id_words

    @staticmethod
    def present(entry: dict, stems: set[str]) -> set[str]:
        return {t for t in stems if t in entry["text"] or t in entry["title"]}

    def results(self, picked: list[tuple[dict, dict]], typed: dict, content: set, mode: str,
                notice: str, id_words: set = frozenset()) -> dict:
        """Shape ranked (index entry, extra fields) pairs into a search response,
        with the words each result and the whole response lack. Words that were
        part of a matched document ID are never reported as missing."""
        matches, covered = [], set()
        reported = content - id_words
        for entry, extra in picked:
            present = self.present(entry, set(typed))
            covered |= present
            record = entry["record"]
            # The excerpt finder looks for whole words, so give it the forms
            # this record actually contains, plural or not.
            words = {w for w in set(tokens(record["title"] + " " + record["text"]))
                     if stem(w) in (present & content or present)}
            matches.append(self.match(record, words, **extra,
                                      missing_terms=sorted(typed[t] for t in reported - present)))
        index = self.index()
        missing = sorted(typed[t] for t in reported - covered)
        unknown = sorted(typed[t] for t in reported
                         if not index["text"]["df"][t] and not index["title"]["df"][t])
        if missing:
            notice += (f" No result contains: {', '.join(missing)}. The answer may not be "
                       "in the data; say so unless the text you read supports it.")
        return {"matches": matches, "search_mode": mode, "missing_terms": missing,
                "unknown_terms": unknown, "notice": notice}

    def search_bm25(self, query: str, terms: set[str], limit: int) -> dict:
        """Rank by BM25 over text and title, with exact document IDs and aliases first.

        Results also say which meaningful query words they lack. A word that no
        result contains is a sign the answer may not be in the data at all.
        """
        ranked, typed, content, id_words = self.rank_bm25(query, terms)
        picked = [(entry, {"score": round(score, 3), "id_match": id_match})
                  for id_match, score, entry, _ in ranked[:limit]]
        return self.results(picked, typed, content, "bm25", (
            "BM25: rare words count more than common ones; titles are boosted; "
            "exact document IDs and aliases rank first. Scores compare results for this "
            "query only. Read records before citing claims."), id_words)

    def vectors(self, index: dict):
        """Embed every record once per export version and keep the vectors with the index."""
        if "vectors" not in index:
            texts = [e["record"]["title"] + "\n" + e["record"]["text"] for e in index["entries"]]
            index["vectors"] = self.embedder.encode(texts) if texts else None
        return index["vectors"]

    def search_hybrid(self, query: str, terms: set[str], limit: int) -> dict:
        """Combine BM25 with embedding similarity using reciprocal rank fusion.

        Each method ranks the records on its own. A record's fused score is the
        sum of 1 / (60 + rank) over the methods that ranked it in their top
        CANDIDATES, so something both methods like rises, and something only
        one finds can still make the list. Exact document IDs and aliases stay first.
        """
        ranked, typed, content, id_words = self.rank_bm25(query, terms)
        index = self.index()
        vectors = self.vectors(index)
        entries = {e["record"]["id"]: e for e in index["entries"]}
        bm25_rank = {item[2]["record"]["id"]: r for r, item in enumerate(ranked[:CANDIDATES], 1)}
        semantic_rank = {}
        if vectors is not None:
            # Rows are unit length, so this dot product is cosine similarity.
            similarity = vectors @ self.embedder.encode([query])[0]
            for r, position in enumerate(np.argsort(-similarity)[:CANDIDATES], 1):
                semantic_rank[index["entries"][position]["record"]["id"]] = r
        id_matches = {item[2]["record"]["id"] for item in ranked if item[0]}
        fused = {}
        for ranks in (bm25_rank, semantic_rank):
            for key, r in ranks.items():
                fused[key] = fused.get(key, 0.0) + 1 / (RRF_K + r)
        order = sorted(fused, key=lambda key: (key not in id_matches, -fused[key], key))
        picked = [(entries[key], {"score": round(fused[key], 5), "id_match": key in id_matches,
                                 "ranks": {"bm25": bm25_rank.get(key), "semantic": semantic_rank.get(key)}})
                  for key in order[:limit]]
        return self.results(picked, typed, content, "hybrid", (
            "Hybrid: BM25 keyword ranking fused with embedding similarity. Each result's "
            "ranks show which method found it. Exact document IDs and aliases rank first. "
            "Read records before citing claims."), id_words)

    @staticmethod
    def excerpt_start(text: str, matched: set[str]) -> int:
        """Choose where a 600-character excerpt starts: near the most distinct hits.

        The first hit is often a common word near the top of a long record, so
        a two-pointer scan finds the 500-character span with the most distinct
        matched words, keeping 100 characters of lead-in. Ties keep the earliest
        span. If only the title matched, the excerpt starts at the beginning.
        """
        # Escape query tokens before building a regex so they are literal text.
        pattern = re.compile(r"\b(?:" + "|".join(re.escape(t) for t in sorted(matched)) + r")\b",
                             re.IGNORECASE)
        hits = [(m.start(), m.group(0).casefold()) for m in pattern.finditer(text)]
        best_start, best_count, window, end = 0, 0, Counter(), 0
        for position, term in hits:
            # Extend the window to every hit within 500 characters of this one.
            while end < len(hits) and hits[end][0] < position + 500:
                window[hits[end][1]] += 1
                end += 1
            if len(window) > best_count:
                best_start, best_count = max(0, position - 100), len(window)
            # Drop this hit before the window moves on to the next one.
            window[term] -= 1
            if not window[term]:
                del window[term]
        return best_start

    def get(self, document_id: str, offset: int = 0, max_chars: int = 4000) -> dict:
        """Find an ID in the export and return a bounded slice of its text.

        document_id is a lookup key, never a filename to open. Offsets count
        Python characters, not bytes or model tokens. next_offset is None at EOF.
        """
        if type(offset) is not int or offset < 0:
            raise ValueError("offset must be a nonnegative integer")
        if type(max_chars) is not int or not 1 <= max_chars <= 10000:
            raise ValueError("max_chars must be between 1 and 10000")
        for record in self.records():
            if record["id"] == document_id:
                if offset > len(record["text"]):
                    raise ValueError("offset exceeds the record length")
                end = min(len(record["text"]), offset + max_chars)
                # Pagination keeps a long document from filling a tool response.
                # Clients can follow next_offset until they have enough context.
                return {**self.reference(record), "metadata": record.get("metadata", {}),
                        "text": record["text"][offset:end], "offset": offset,
                        "total_chars": len(record["text"]),
                        "next_offset": end if end < len(record["text"]) else None}
        raise ValueError("Record not found. Search for an available record ID first.")
