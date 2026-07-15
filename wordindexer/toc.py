"""
Table of Contents detection for WordIndexer.

Version 1 uses a conservative text-and-style heuristic. A paragraph titled
"Table of Contents" or "Contents" starts the TOC; following TOC-like lines
are skipped until the first non-TOC paragraph, preferably a heading.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from docx.document import Document


@dataclass(slots=True)
class TOCResult:
    """Detected indexing boundary information."""

    found: bool
    toc_start: int | None
    body_start: int


class TOCDetector:
    """Detect a basic Table of Contents boundary."""

    _toc_title = re.compile(
        r"^(?:table\s+of\s+contents|contents)\s*$",
        re.IGNORECASE,
    )
    _toc_entry = re.compile(
        r"(?:\.{2,}|\t+)\s*(?:[ivxlcdm]+|\d+)\s*$",
        re.IGNORECASE,
    )

    @classmethod
    def _is_toc_title(cls, text: str) -> bool:
        normalized = re.sub(r"\s+", " ", text.strip())
        return bool(cls._toc_title.fullmatch(normalized))

    @classmethod
    def _looks_like_toc_entry(cls, text: str) -> bool:
        return bool(cls._toc_entry.search(text.strip()))

    def detect(self, document: Document) -> TOCResult:
        """Return the first paragraph that should be indexed."""
        paragraphs = document.paragraphs
        toc_index: int | None = None

        for index, paragraph in enumerate(paragraphs):
            if self._is_toc_title(paragraph.text):
                toc_index = index
                break

        if toc_index is None:
            return TOCResult(
                found=False,
                toc_start=None,
                body_start=0,
            )

        for index in range(toc_index + 1, len(paragraphs)):
            paragraph = paragraphs[index]
            text = paragraph.text.strip()

            if not text or self._looks_like_toc_entry(text):
                continue

            style_name = paragraph.style.name if paragraph.style else ""

            if style_name.startswith("Heading") or text:
                return TOCResult(
                    found=True,
                    toc_start=toc_index,
                    body_start=index,
                )

        return TOCResult(
            found=True,
            toc_start=toc_index,
            body_start=len(paragraphs),
        )
