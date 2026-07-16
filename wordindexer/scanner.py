"""
Run scanner for WordIndexer.

Locates every occurrence of a term in a paragraph while preserving the
relationship between the paragraph's combined text and its individual Word
runs. This allows a later writer to modify only the affected runs and retain
formatting.
"""

from __future__ import annotations

import re

from docx.document import Document

from wordindexer.models import RunLocation


class RunScanner:
    """Locate term occurrences in the runs of a Word document."""

    def __init__(self, document: Document):
        self.document = document

    @staticmethod
    def _pattern(term: str) -> re.Pattern[str]:
        """Build the project's default case-insensitive whole-word pattern."""
        return re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)

    def locate_occurrences(
        self,
        paragraph_index: int,
        term: str,
    ) -> list[list[RunLocation]]:
        """
        Locate every occurrence of ``term`` in one paragraph.

        The returned outer list contains one item per occurrence. Each inner
        list contains the run fragments occupied by that occurrence. A term
        split across differently formatted runs therefore remains grouped as
        one occurrence while retaining exact per-run offsets.
        """
        paragraph = self.document.paragraphs[paragraph_index]

        run_offsets: list[tuple[int, int, str]] = []
        parts: list[str] = []
        offset = 0

        for run_index, run in enumerate(paragraph.runs):
            text = run.text or ""
            start = offset
            offset += len(text)
            run_offsets.append((run_index, start, text))
            parts.append(text)

        combined_text = "".join(parts)
        occurrences: list[list[RunLocation]] = []

        for match in self._pattern(term).finditer(combined_text):
            fragments: list[RunLocation] = []
            match_start = match.start()
            match_end = match.end()

            for run_index, run_start, run_text in run_offsets:
                run_end = run_start + len(run_text)

                if not run_text:
                    continue

                fragment_start = max(match_start, run_start)
                fragment_end = min(match_end, run_end)

                if fragment_start >= fragment_end:
                    continue

                local_start = fragment_start - run_start
                local_end = fragment_end - run_start

                fragments.append(
                    RunLocation(
                        paragraph_index=paragraph_index,
                        run_index=run_index,
                        start=local_start,
                        end=local_end,
                        matched_text=run_text[local_start:local_end],
                    )
                )

            if fragments:
                occurrences.append(fragments)

        return occurrences

    def locate(
        self,
        paragraph_index: int,
        term: str,
    ) -> list[RunLocation]:
        """
        Locate every matching run fragment in a paragraph.

        This compatibility method returns a flat list. New code that needs to
        distinguish repeated occurrences or terms split across runs should use
        ``locate_occurrences``.
        """
        return [
            location
            for occurrence in self.locate_occurrences(paragraph_index, term)
            for location in occurrence
        ]