"""
Search engine for WordIndexer.
"""

from __future__ import annotations

import re

from wordindexer.models import Book, DictionaryEntry, Match


class SearchEngine:

    def __init__(self, book: Book):
        self.book = book

    def search(
        self,
        dictionary: list[DictionaryEntry],
    ) -> dict[str, list[Match]]:

        self.book.matches.clear()
        self.book.term_matches.clear()

        results: dict[str, list[Match]] = {}

        current_heading = ""

        heading_lookup = {}

        for h in self.book.headings:
            heading_lookup[h.paragraph_index] = h.text

        for entry in dictionary:

            if not entry.enabled:
                continue

            canonical = entry.index_as or entry.term

            search_terms = [entry.term] + entry.aliases

            matches = []

            for paragraph in self.book.paragraphs:

                if paragraph.index in heading_lookup:
                    current_heading = heading_lookup[paragraph.index]

                if not paragraph.text.strip():
                    continue

                for term in search_terms:

                    pattern = re.compile(
                        rf"\b{re.escape(term)}\b",
                        re.IGNORECASE,
                    )

                    if pattern.search(paragraph.text):

                        m = Match(
                            term=canonical,
                            matched_text=term,
                            paragraph_index=paragraph.index,
                            paragraph_text=paragraph.text,
                            paragraph_style=paragraph.style,
                            page=paragraph.page,
                            section=paragraph.section,
                            heading=current_heading,
                        )

                        matches.append(m)
                        self.book.matches.append(m)

            results[canonical] = matches

        self.book.term_matches = results

        return results