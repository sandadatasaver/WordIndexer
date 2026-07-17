"""
End-to-end WordIndexer indexing pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from wordindexer.dictionary import DictionaryEntry
from wordindexer.document import DocumentReader
from wordindexer.index_field import IndexFieldWriter
from wordindexer.models import Match
from wordindexer.search import SearchEngine
from wordindexer.toc import TOCDetector
from wordindexer.xe import XEWriter


@dataclass(slots=True)
class IndexResult:
    """Summary of one indexing operation."""

    input_path: Path
    output_path: Path
    toc_detected: bool
    toc_method: str
    body_start: int
    terms_found: int
    terms_not_found: int
    occurrences: int
    fields_inserted: int
    index_field_inserted: bool


class IndexEngine:
    """Run the document, search, and XE-writing pipeline."""

    def __init__(
        self,
        toc_detector: TOCDetector | None = None,
        xe_writer: XEWriter | None = None,
        index_field_writer: IndexFieldWriter | None = None,
        include_index_field: bool = True,
        include_tables: bool = False,
    ):
        self.toc_detector = toc_detector or TOCDetector()
        self.xe_writer = xe_writer or XEWriter()
        self.index_field_writer = index_field_writer or IndexFieldWriter()
        self.include_index_field = include_index_field
        self.include_tables = include_tables

    @staticmethod
    def _position(match: Match) -> tuple[int, int, int]:
        if not match.locations:
            return match.paragraph_index, 0, 0

        first = match.locations[0]
        return match.paragraph_index, first.run_index, first.start

    @staticmethod
    def _canonical_terms(
        dictionary: list[DictionaryEntry],
    ) -> list[str]:
        return list(
            dict.fromkeys(
                entry.index_as or entry.term
                for entry in dictionary
                if entry.enabled and entry.term
            )
        )

    def index(
        self,
        input_path: str | Path,
        dictionary: list[DictionaryEntry],
        output_path: str | Path,
    ) -> IndexResult:
        """
        Index a DOCX file and save a new DOCX file.

        Matches are inserted in reverse document order so earlier run indexes
        remain valid while later fields are inserted.
        """
        source = Path(input_path)
        destination = Path(output_path)
        reader = DocumentReader(source)
        book = reader.load_book(include_tables=self.include_tables)

        toc = self.toc_detector.detect(reader.doc, book.paragraphs)
        book.paragraphs = [
            paragraph
            for paragraph in book.paragraphs
            if paragraph.index >= toc.body_start
        ]
        book.headings = [
            heading
            for heading in book.headings
            if heading.paragraph_index >= toc.body_start
        ]

        results = SearchEngine(book, reader.doc).search(dictionary)
        matches = list(book.matches)
        see_also_match_ids: set[int] = set()
        seen_see_also_terms: set[str] = set()

        for match in sorted(matches, key=self._position):
            entry = match.dictionary_entry

            if entry is None or not entry.see_also:
                continue

            canonical = entry.index_as or entry.term

            if canonical not in seen_see_also_terms:
                seen_see_also_terms.add(canonical)
                see_also_match_ids.add(id(match))

        for match in sorted(matches, key=self._position, reverse=True):
            paragraph = book.paragraph_targets[match.paragraph_index]
            self.xe_writer.insert_match(
                paragraph,
                match,
                include_see_also=id(match) in see_also_match_ids,
            )

        index_field_inserted = False

        if self.include_index_field:
            self.index_field_writer.insert_index_field(reader.doc)
            index_field_inserted = True

        destination.parent.mkdir(parents=True, exist_ok=True)
        reader.doc.save(destination)

        found_terms = sum(
            bool(results.get(term))
            for term in self._canonical_terms(dictionary)
        )
        terms_not_found = len(self._canonical_terms(dictionary)) - found_terms

        return IndexResult(
            input_path=source,
            output_path=destination,
            toc_detected=toc.found,
            toc_method=toc.method,
            body_start=toc.body_start,
            terms_found=found_terms,
            terms_not_found=terms_not_found,
            occurrences=len(matches),
            fields_inserted=len(matches),
            index_field_inserted=index_field_inserted,
        )
