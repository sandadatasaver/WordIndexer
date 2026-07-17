"""
Table of Contents and indexing-boundary detection for WordIndexer.

Version 1 uses a conservative cascade:

1. An explicit "Table of Contents" or "Contents" heading.
2. A first-chapter heading fallback for documents whose TOC is stored as a
   Word field, image, or unsupported structure.
3. The whole document when no boundary can be identified.
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
    method: str = "none"


class TOCDetector:
    """Detect a Table of Contents or a safe body-start boundary."""

    _toc_title = re.compile(
        r"^(?:table\s+of\s+contents|contents)\s*$",
        re.IGNORECASE,
    )
    _toc_entry = re.compile(
        r"(?:\.{2,}|\t+)\s*(?:[ivxlcdm]+|\d+)\s*$",
        re.IGNORECASE,
    )
    _first_chapter = re.compile(
        r"^(?:chapter|ch\.?)\s+(?:1|one|i)\b",
        re.IGNORECASE,
    )

    @classmethod
    def _is_toc_title(cls, text: str) -> bool:
        normalized = re.sub(r"\s+", " ", text.strip())
        return bool(cls._toc_title.fullmatch(normalized))

    @classmethod
    def _looks_like_toc_entry(cls, text: str) -> bool:
        return bool(cls._toc_entry.search(text.strip()))

    @classmethod
    def _is_first_chapter_heading(cls, paragraph) -> bool:
        style = paragraph.style
        style_name = style.name if hasattr(style, "name") else style or ""
        return (
            style_name.startswith("Heading 1")
            and bool(cls._first_chapter.match(paragraph.text.strip()))
        )

    def detect(self, document: Document, paragraphs=None) -> TOCResult:
        """Return the first paragraph that should be indexed."""
        paragraphs = list(paragraphs or document.paragraphs)
        toc_index: int | None = None

        for index, paragraph in enumerate(paragraphs):
            if self._is_toc_title(paragraph.text):
                toc_index = index
                break

        if toc_index is not None:
            # Prefer the first post-TOC heading. This avoids treating table
            # cells containing TOC entries as the manuscript body.
            for index in range(toc_index + 1, len(paragraphs)):
                paragraph = paragraphs[index]
                style = paragraph.style
                style_name = (
                    style.name
                    if hasattr(style, "name")
                    else style or ""
                )

                if style_name.startswith("Heading 1"):
                    return TOCResult(
                        found=True,
                        toc_start=toc_index,
                        body_start=index,
                        method="title",
                    )

            for index in range(toc_index + 1, len(paragraphs)):
                paragraph = paragraphs[index]
                text = paragraph.text.strip()

                if not text or self._looks_like_toc_entry(text):
                    continue

                return TOCResult(
                    found=True,
                    toc_start=toc_index,
                    body_start=index,
                    method="title",
                )

            return TOCResult(
                found=True,
                toc_start=toc_index,
                body_start=len(paragraphs),
                method="title",
            )

        for index, paragraph in enumerate(paragraphs):
            if self._is_first_chapter_heading(paragraph):
                return TOCResult(
                    found=False,
                    toc_start=None,
                    body_start=index,
                    method="first_chapter_heading",
                )

        return TOCResult(
            found=False,
            toc_start=None,
            body_start=0,
            method="none",
        )
