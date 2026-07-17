"""
Writer for the visible Microsoft Word INDEX field.
"""

from __future__ import annotations

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph


class IndexFieldWriter:
    """Append a titled Word INDEX field to a document."""

    def insert_index_field(
        self,
        document: Document,
        field_code: str = "INDEX",
        heading: str = "Index",
        heading_style: str = "Heading 1",
        page_break_before: bool = True,
    ) -> Paragraph:
        """
        Append an Index heading and a pending INDEX field.

        Word populates the field result when the document fields are updated
        with F9 or Ctrl+A followed by F9.
        """
        if not field_code or not field_code.strip():
            raise ValueError("field_code must not be empty")

        if not heading or not heading.strip():
            raise ValueError("heading must not be empty")

        heading_paragraph = document.add_paragraph(
            heading,
            style=heading_style,
        )

        if page_break_before:
            heading_paragraph.paragraph_format.page_break_before = True

        paragraph = document.add_paragraph()

        begin_run = OxmlElement("w:r")
        begin_char = OxmlElement("w:fldChar")
        begin_char.set(qn("w:fldCharType"), "begin")
        begin_char.set(qn("w:dirty"), "true")
        begin_run.append(begin_char)

        instruction_run = OxmlElement("w:r")
        instruction = OxmlElement("w:instrText")
        instruction.set(qn("xml:space"), "preserve")
        instruction.text = f" {field_code.strip()} "
        instruction_run.append(instruction)

        separator_run = OxmlElement("w:r")
        separator = OxmlElement("w:fldChar")
        separator.set(qn("w:fldCharType"), "separate")
        separator_run.append(separator)

        end_run = OxmlElement("w:r")
        end_char = OxmlElement("w:fldChar")
        end_char.set(qn("w:fldCharType"), "end")
        end_run.append(end_char)

        paragraph._p.extend(
            [
                begin_run,
                instruction_run,
                separator_run,
                end_run,
            ]
        )

        return paragraph
