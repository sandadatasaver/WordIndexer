"""
Back-matter layout writer for Index and Glossary sections.
"""

from __future__ import annotations

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from wordindexer.glossary import GlossaryReport


class BackMatterWriter:
    """Replace and rebuild the Index/Glossary back-matter sections."""

    _about_headings = {
        "about the author",
        "contact",
    }

    @staticmethod
    def _heading_paragraphs(document: Document, text: str):
        matches = []
        wanted = text.casefold()

        for paragraph in document.paragraphs:
            style = paragraph.style.name if paragraph.style else ""
            if (
                style.startswith("Heading 1")
                and paragraph.text.strip().casefold() == wanted
            ):
                matches.append(paragraph)

        return matches

    @staticmethod
    def _new_text_paragraph(
        text: str,
        style: str,
        page_break_before: bool = False,
    ):
        paragraph = OxmlElement("w:p")
        properties = OxmlElement("w:pPr")
        paragraph.append(properties)

        paragraph_style = OxmlElement("w:pStyle")
        paragraph_style.set(qn("w:val"), style.replace(" ", ""))
        properties.append(paragraph_style)

        if page_break_before:
            properties.append(OxmlElement("w:pageBreakBefore"))

        run = OxmlElement("w:r")
        text_element = OxmlElement("w:t")
        text_element.text = text
        run.append(text_element)
        paragraph.append(run)
        return paragraph

    @staticmethod
    def _new_glossary_entry(entry):
        paragraph = OxmlElement("w:p")
        run = OxmlElement("w:r")
        properties = OxmlElement("w:rPr")
        properties.append(OxmlElement("w:b"))
        run.append(properties)

        term = OxmlElement("w:t")
        term.text = entry.term
        run.append(term)
        paragraph.append(run)

        suffix = OxmlElement("w:r")
        suffix_text = OxmlElement("w:t")
        suffix_text.text = (
            f" ({entry.category})" if entry.category else ""
        ) + f": {entry.definition}"
        suffix.append(suffix_text)
        paragraph.append(suffix)
        return paragraph

    @staticmethod
    def _new_index_field_paragraph():
        paragraph = OxmlElement("w:p")

        begin_run = OxmlElement("w:r")
        begin = OxmlElement("w:fldChar")
        begin.set(qn("w:fldCharType"), "begin")
        begin.set(qn("w:dirty"), "true")
        begin_run.append(begin)

        instruction_run = OxmlElement("w:r")
        instruction = OxmlElement("w:instrText")
        instruction.set(qn("xml:space"), "preserve")
        instruction.text = " INDEX "
        instruction_run.append(instruction)

        separator_run = OxmlElement("w:r")
        separator = OxmlElement("w:fldChar")
        separator.set(qn("w:fldCharType"), "separate")
        separator_run.append(separator)

        end_run = OxmlElement("w:r")
        end = OxmlElement("w:fldChar")
        end.set(qn("w:fldCharType"), "end")
        end_run.append(end)

        paragraph.extend(
            [begin_run, instruction_run, separator_run, end_run]
        )
        return paragraph

    def rebuild(
        self,
        document: Document,
        report: GlossaryReport | None,
        include_index_field: bool = True,
        include_index_heading: bool = True,
        include_glossary: bool = True,
    ) -> None:
        """Replace an existing Index section and add Glossary before author/contact matter."""
        body = document.element.body
        children = list(body.iterchildren())
        paragraphs = list(document.paragraphs)

        index_candidates = [
            paragraph
            for paragraph in paragraphs
            if paragraph.style
            and paragraph.style.name.startswith("Heading 1")
            and paragraph.text.strip().casefold() == "index"
        ]
        existing_index = index_candidates[-1] if index_candidates else None

        boundary_candidates = [
            paragraph
            for paragraph in paragraphs
            if paragraph.style
            and paragraph.style.name.startswith("Heading 1")
            and paragraph.text.strip().casefold() in self._about_headings
        ]

        boundary = None
        if existing_index is not None:
            index_position = children.index(existing_index._p)
            following = [
                paragraph
                for paragraph in boundary_candidates
                if children.index(paragraph._p) > index_position
            ]
            if following:
                boundary = min(
                    following,
                    key=lambda paragraph: children.index(paragraph._p),
                )

            start_position = index_position
            end_position = (
                children.index(boundary._p)
                if boundary is not None
                else next(
                    (
                        index
                        for index, child in enumerate(children)
                        if child.tag == qn("w:sectPr")
                    ),
                    len(children),
                )
            )

            for child in children[start_position:end_position]:
                body.remove(child)

            children = list(body.iterchildren())

        if boundary is not None and boundary._p.getparent() is body:
            insertion_position = body.index(boundary._p)
        else:
            insertion_position = next(
                (
                    index
                    for index, child in enumerate(children)
                    if child.tag == qn("w:sectPr")
                ),
                len(children),
            )

        new_elements: list[object] = []

        if include_index_heading:
            new_elements.append(
                self._new_text_paragraph(
                    "Index",
                    "Heading1",
                    page_break_before=True,
                )
            )

            if include_index_field:
                new_elements.append(self._new_index_field_paragraph())

        if include_glossary:
            new_elements.append(
                self._new_text_paragraph(
                    "Glossary",
                    "Heading1",
                    page_break_before=True,
                )
            )
            new_elements.extend(
                self._new_glossary_entry(entry)
                for entry in (report.entries if report is not None else [])
            )

        for offset, element in enumerate(new_elements):
            body.insert(insertion_position + offset, element)
