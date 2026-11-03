"""Read and search a neutral ingestion export without choosing a dataset.

JSONL means one JSON object per line. This adapter reads small exports into
memory on every call, validates them, and returns source-linked text. It never
writes the file or fetches the source references. Future ingestion/semantic
retrieval can replace this adapter while preserving the tools in server.py.
"""
import json
import re
from collections import Counter
from pathlib import Path


class RecordStore:
    """One configured file, shared by the MCP status/search/read tools."""

    def __init__(self, path: Path):
        """Expand ~ and anchor the path now, independent of later directory changes."""
        self.path = path.expanduser().resolve()

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
                "record_count": len(records), "search_mode": "keyword",
                "notice": "Records come from an ingestion export; this file is empty until ingestion publishes it."}

    @staticmethod
    def reference(record):
        """Keep search and read responses consistent about identity and provenance."""
        return {"id": record["id"], "title": record["title"], "source": record["source"],
                "citation": f"[{record['id']}]"}

    def search(self, query: str, limit: int = 5) -> dict:
        """Return bounded excerpts ranked by distinct query words found in each record.

        This is a transparent keyword baseline, not embedding/semantic search.
        A match provides candidate evidence, not proof that a claim is correct.
        """
        if not isinstance(query, str) or not 1 <= len(query.strip()) <= 2000:
            raise ValueError("query must contain 1–2000 characters")
        if type(limit) is not int or not 1 <= limit <= 10:
            raise ValueError("limit must be between 1 and 10")
        # casefold normalizes case; \w+ extracts word/number tokens. Sets mean
        # repeating a word does not inflate its importance. Phrases are not kept.
        terms = set(re.findall(r"\w+", query.casefold()))
        if not terms:
            raise ValueError("query must contain a word or number")
        ranked = []
        for record in self.records():
            words = set(re.findall(r"\w+", (record["title"] + " " + record["text"]).casefold()))
            matched = terms & words  # Set intersection: words present in both.
            if matched:
                ranked.append((record, matched))
        # More distinct matches sort first; ID breaks ties deterministically.
        ranked.sort(key=lambda pair: (-len(pair[1]), pair[0]["id"]))
        matches = []
        for record, matched in ranked[:limit]:
            start = self.excerpt_start(record["text"], matched)
            end = min(len(record["text"]), start + 600)
            # Metadata rides along so a client can compare attributes such as
            # dates before choosing which records to read in full.
            matches.append({**self.reference(record), "metadata": record.get("metadata", {}),
                            "text": record["text"][start:end],
                            "offset": start, "next_offset": end if end < len(record["text"]) else None,
                            "matched_terms": sorted(matched)})
        return {"matches": matches, "search_mode": "keyword",
                "notice": "Matches any query word; ranks by distinct words matched. Not semantic search or answer confidence. Read records before citing claims."}

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
