"""
Reviewable candidate-term discovery from DOCX manuscripts.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from wordindexer.dictionary import DictionaryEntry
from wordindexer.document import DocumentReader
from wordindexer.toc import TOCDetector


@dataclass(slots=True)
class CandidateTerm:
    """One candidate term with evidence for human review."""

    term: str
    occurrences: int
    variants: list[str]
    paragraphs: list[int]
    contexts: list[str]
    category: str = ""

    def suggested_entry(self) -> dict:
        """Return a dictionary-compatible suggestion."""
        aliases = [variant for variant in self.variants if variant != self.term]
        return {
            "term": self.term,
            "aliases": aliases,
            "index_as": self.term,
            "category": self.category,
            "enabled": True,
        }


@dataclass(slots=True)
class DiscoveryReport:
    """Reviewable output from one candidate-discovery run."""

    input_path: str
    body_start: int
    toc_method: str
    candidates: list[CandidateTerm]

    def as_dict(self) -> dict:
        return {
            "input_path": self.input_path,
            "body_start": self.body_start,
            "toc_method": self.toc_method,
            "candidates": [
                {
                    **asdict(candidate),
                    "suggested_entry": candidate.suggested_entry(),
                }
                for candidate in self.candidates
            ],
        }

    def write_json(self, filename: str | Path) -> Path:
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.as_dict(), indent=2),
            encoding="utf-8",
        )
        return path


class TermDiscovery:
    """Discover repeated technical-looking terms for human review."""

    _token_pattern = re.compile(
        r"(?<![\w$])"
        r"(?:[A-Za-z][A-Za-z0-9]*(?:[-_][A-Za-z0-9]+)+|"
        r"[A-Z][A-Za-z0-9]*|"
        r"[A-Z]{2,})"
        r"(?![\w])"
    )

    def __init__(self, minimum_occurrences: int = 2):
        if minimum_occurrences < 1:
            raise ValueError("minimum_occurrences must be at least 1")
        self.minimum_occurrences = minimum_occurrences

    @staticmethod
    def _is_candidate(token: str) -> bool:
        if len(token) < 3:
            return False
        if "-" in token or "_" in token:
            return True
        if token.isupper():
            return True
        return any(character.isupper() for character in token[1:])

    @staticmethod
    def _is_path_fragment(text: str, start: int, end: int) -> bool:
        """Exclude tokens that are visibly embedded in paths or URLs."""
        if start > 0 and text[start - 1] in "\\/":
            return True
        if end < len(text) and text[end] in "\\/":
            return True

        window = text[max(0, start - 80):min(len(text), end + 80)]
        return "://" in window and (
            start > 0 and text[start - 1] in "\\/"
            or end < len(text) and text[end] in "\\/"
        )

    @staticmethod
    def _existing_terms(
        dictionary: list[DictionaryEntry],
    ) -> set[str]:
        terms: set[str] = set()

        for entry in dictionary:
            terms.add(entry.term.casefold())
            terms.update(alias.casefold() for alias in entry.aliases)
            if entry.index_as:
                terms.add(entry.index_as.casefold())

        return terms

    def discover(
        self,
        input_path: str | Path,
        dictionary: list[DictionaryEntry] | None = None,
        include_tables: bool = False,
    ) -> DiscoveryReport:
        source = Path(input_path)
        reader = DocumentReader(source)
        book = reader.load_book(include_tables=include_tables)
        toc = TOCDetector().detect(reader.doc, book.paragraphs)

        body_paragraphs = [
            paragraph
            for paragraph in book.paragraphs
            if paragraph.index >= toc.body_start
        ]
        existing_terms = self._existing_terms(dictionary or [])
        data: dict[str, dict] = {}

        for paragraph in body_paragraphs:
            for match in self._token_pattern.finditer(paragraph.text):
                token = match.group()

                if not self._is_candidate(token):
                    continue

                if self._is_path_fragment(
                    paragraph.text,
                    match.start(),
                    match.end(),
                ):
                    continue

                key = token.casefold()

                if key in existing_terms:
                    continue

                item = data.setdefault(
                    key,
                    {
                        "term": token,
                        "variants": [],
                        "paragraphs": [],
                        "contexts": [],
                        "occurrences": 0,
                    },
                )
                item["occurrences"] += 1

                if token not in item["variants"]:
                    item["variants"].append(token)

                if paragraph.index not in item["paragraphs"]:
                    item["paragraphs"].append(paragraph.index)

                if len(item["contexts"]) < 3:
                    context = " ".join(paragraph.text.split())
                    if context and context not in item["contexts"]:
                        item["contexts"].append(context[:240])

        candidates = [
            CandidateTerm(**item)
            for item in data.values()
            if item["occurrences"] >= self.minimum_occurrences
        ]
        candidates.sort(
            key=lambda candidate: (
                -candidate.occurrences,
                candidate.term.casefold(),
            )
        )

        return DiscoveryReport(
            input_path=str(source),
            body_start=toc.body_start,
            toc_method=toc.method,
            candidates=candidates,
        )
