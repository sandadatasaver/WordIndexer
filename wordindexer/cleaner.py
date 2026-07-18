"""
Safe document cleanup operations for final manuscript output.
"""

from __future__ import annotations

from docx import Document
from docx.oxml.ns import qn


class DocumentCleaner:
    """Remove explicitly requested top-level sections."""

    @staticmethod
    def _normalize(value: str) -> str:
        return " ".join(value.split()).casefold()

    def remove_sections(
        self,
        document: Document,
        headings: list[str] | None = None,
    ) -> list[str]:
        """
        Remove each named Heading 1 section through the next Heading 1.

        The source document is modified in memory only; callers decide where
        to save the cleaned copy. Exact heading names are used deliberately so
        ordinary paragraphs are never removed by a loose text match.
        """
        requested = {
            self._normalize(heading)
            for heading in (headings or [])
            if heading.strip()
        }
        removed: list[str] = []

        if not requested:
            return removed

        body = document.element.body
        body_children = list(body.iterchildren())
        top_level_paragraphs = list(document.paragraphs)
        headings = []

        for paragraph in top_level_paragraphs:
            style = paragraph.style.name if paragraph.style else ""
            normalized = self._normalize(paragraph.text)

            if (
                style.startswith("Heading 1")
                and normalized in requested
            ):
                headings.append(paragraph)

        for anchor in headings:
            current_children = list(body.iterchildren())

            if anchor._p.getparent() is not body:
                continue

            start = current_children.index(anchor._p)
            end = next(
                (
                    index
                    for index in range(start + 1, len(current_children))
                    if self._is_heading1_element(
                        current_children[index]
                    )
                ),
                next(
                    (
                        index
                        for index, child in enumerate(current_children)
                        if child.tag == qn("w:sectPr")
                        and index > start
                    ),
                    len(current_children),
                ),
            )

            for child in current_children[start:end]:
                body.remove(child)

            removed.append(anchor.text.strip())

        return removed

    @staticmethod
    def _is_heading1_element(element) -> bool:
        if element.tag != qn("w:p"):
            return False

        ppr = element.find(qn("w:pPr"))
        if ppr is None:
            return False

        style = ppr.find(qn("w:pStyle"))
        if style is None:
            return False

        return style.get(qn("w:val")) == "Heading1"
