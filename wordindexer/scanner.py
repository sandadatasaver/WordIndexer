"""
Run scanner for WordIndexer.

Locates the exact run(s) containing a search term.
"""

from __future__ import annotations

import re

from docx.document import Document

from wordindexer.models import RunLocation


class RunScanner:

    def __init__(self, document: Document):

        self.document = document

    def locate(
        self,
        paragraph_index: int,
        term: str,
    ) -> list[RunLocation]:

        results: list[RunLocation] = []

        paragraph = self.document.paragraphs[paragraph_index]

        pattern = re.compile(
            rf"\b{re.escape(term)}\b",
            re.IGNORECASE,
        )

        for run_index, run in enumerate(paragraph.runs):

            if not run.text:
                continue

            for match in pattern.finditer(run.text):

                results.append(
                    RunLocation(
                        paragraph_index=paragraph_index,
                        run_index=run_index,
                        start=match.start(),
                        end=match.end(),
                        matched_text=match.group(),
                    )
                )

        return results