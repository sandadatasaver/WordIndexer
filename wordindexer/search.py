"""
Search engine for WordIndexer.

Searches dictionary concepts and records every occurrence. When a source
python-docx document is supplied, each Match also contains the exact run
fragments needed by the XML writer.
"""

from __future__ import annotations

import re

from docx.document import Document

from wordindexer.matcher import MatchResolver
from wordindexer.models import Book, DictionaryEntry, Match
from wordindexer.scanner import RunScanner


class SearchEngine:
    """Search a :class:`Book` for dictionary concepts."""

    def __init__(
        self,
        book: Book,
        document: Document | None = None,
    ):
        self.book = book
        self.document = document
        self.scanner = RunScanner(document) if document is not None else None
        self.raw_match_count = 0
        self.resolved_match_count = 0

    @staticmethod
    def _pattern(term: str) -> re.Pattern[str]:
        """Build the default case-insensitive whole-word pattern."""
        return re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)

    @staticmethod
    def _location_key(locations) -> tuple[tuple[int, int, int], ...]:
        """Return a stable identity for one run-level occurrence."""
        return tuple(
            (location.run_index, location.start, location.end)
            for location in locations
        )

    @staticmethod
    def _sort_key(match: Match) -> tuple[int, int, int]:
        """Sort matches in document order."""
        if match.locations:
            first = match.locations[0]
            return match.paragraph_index, first.run_index, first.start

        position = match.paragraph_text.casefold().find(
            match.matched_text.casefold()
        )
        return match.paragraph_index, 0, max(position, 0)

    def search(
        self,
        dictionary: list[DictionaryEntry],
    ) -> dict[str, list[Match]]:
        """
        Find every occurrence of every enabled dictionary entry.

        Aliases are searched but reported under the canonical ``index_as``
        value. Duplicate results caused by identical aliases are removed.
        When a document is supplied, exact run locations are attached to each
        Match; otherwise paragraph-level matches are still returned.
        """
        self.book.matches.clear()
        self.book.term_matches.clear()

        results: dict[str, list[Match]] = {}

        heading_lookup = {
            heading.paragraph_index: heading.text
            for heading in self.book.headings
        }
        current_heading = ""
        paragraph_headings: dict[int, str] = {}

        for paragraph in self.book.paragraphs:
            if paragraph.index in heading_lookup:
                current_heading = heading_lookup[paragraph.index]
            paragraph_headings[paragraph.index] = current_heading

        for entry in dictionary:
            if not entry.enabled or not entry.term:
                continue

            canonical = entry.index_as or entry.term
            search_terms = list(dict.fromkeys([entry.term, *entry.aliases]))
            found: list[Match] = []
            seen: set[tuple] = set()

            for paragraph in self.book.paragraphs:
                text = paragraph.text
                if not text.strip():
                    continue

                for term in search_terms:
                    if self.scanner is not None:
                        occurrences = self.scanner.locate_occurrences(
                            paragraph.index,
                            term,
                        )

                        for locations in occurrences:
                            key = (
                                paragraph.index,
                                self._location_key(locations),
                            )

                            if key in seen:
                                continue

                            seen.add(key)
                            matched_text = "".join(
                                location.matched_text
                                for location in locations
                            )

                            found.append(
                                Match(
                                    term=canonical,
                                    matched_text=matched_text,
                                    paragraph_index=paragraph.index,
                                    paragraph_text=text,
                                    paragraph_style=paragraph.style,
                                    page=paragraph.page,
                                    section=paragraph.section,
                                    heading=paragraph_headings.get(
                                        paragraph.index,
                                        "",
                                    ),
                                    locations=locations,
                                )
                            )
                    else:
                        pattern = self._pattern(term)

                        for match in pattern.finditer(text):
                            key = (
                                paragraph.index,
                                match.start(),
                                match.end(),
                            )

                            if key in seen:
                                continue

                            seen.add(key)
                            found.append(
                                Match(
                                    term=canonical,
                                    matched_text=match.group(),
                                    paragraph_index=paragraph.index,
                                    paragraph_text=text,
                                    paragraph_style=paragraph.style,
                                    page=paragraph.page,
                                    section=paragraph.section,
                                    heading=paragraph_headings.get(
                                        paragraph.index,
                                        "",
                                    ),
                                )
                            )

            found.sort(key=self._sort_key)
            results[canonical] = found
            self.book.matches.extend(found)

        raw_matches = [
            match
            for term_matches in results.values()
            for match in term_matches
        ]

        self.raw_match_count = len(raw_matches)
        resolved_matches = MatchResolver().resolve(raw_matches)
        self.resolved_match_count = len(resolved_matches)

        resolved_results: dict[str, list[Match]] = {
            term: []
            for term in results
        }

        for match in resolved_matches:
            resolved_results.setdefault(match.term, []).append(match)

        for term_matches in resolved_results.values():
            term_matches.sort(key=self._sort_key)

        self.book.matches = sorted(
            resolved_matches,
            key=self._sort_key,
        )
        self.book.term_matches = resolved_results
        return resolved_results
