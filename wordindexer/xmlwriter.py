"""
Low-level WordprocessingML writer.

This module contains generic complex-field insertion logic. Domain-specific
field syntax belongs in modules such as ``xe.py``.
"""

from __future__ import annotations

from copy import deepcopy

from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph


class XMLWriter:
    """Insert low-level WordprocessingML fields into paragraphs."""

    def insert_field(
        self,
        paragraph: Paragraph,
        run_index: int,
        offset: int,
        field_code: str,
        instruction_parts: list[str] | None = None,
    ) -> None:
        """
        Insert a complex field at an exact position in a run.

        The original visible text is retained. If the insertion point is in
        the middle of a run, that run is split into before and after runs,
        preserving its run properties on both sides.

        ``instruction_parts`` can be used when a producer requires the field
        instruction to be represented by multiple ``w:instrText`` elements,
        as Microsoft Word does for XE fields.
        """
        if not field_code or not field_code.strip():
            raise ValueError("field_code must not be empty")

        runs = paragraph.runs

        if run_index < 0 or run_index >= len(runs):
            raise IndexError(f"Invalid run index: {run_index}")

        source_run = runs[run_index]
        source_text = source_run.text or ""

        if offset < 0 or offset > len(source_text):
            raise ValueError(
                f"offset {offset} is outside run text of length {len(source_text)}"
            )

        source_element = source_run._r
        parent = source_element.getparent()
        source_position = parent.index(source_element)

        before_text = source_text[:offset]
        after_text = source_text[offset:]

        replacement: list[object] = []

        if before_text:
            replacement.append(
                self._copy_run_with_text(source_element, before_text)
            )

        replacement.extend(
            self._field_runs(
                field_code=field_code.strip(),
                instruction_parts=instruction_parts,
            )
        )

        if after_text:
            replacement.append(
                self._copy_run_with_text(source_element, after_text)
            )

        parent.remove(source_element)

        for index, element in enumerate(replacement):
            parent.insert(source_position + index, element)

    @staticmethod
    def _copy_run_with_text(source_element, text: str):
        """Copy a run's properties and replace its visible text."""
        copied = deepcopy(source_element)
        run_properties = copied.find(qn("w:rPr"))

        for child in list(copied):
            if child is not run_properties:
                copied.remove(child)

        text_element = OxmlElement("w:t")

        if text[:1].isspace() or text[-1:].isspace():
            text_element.set(qn("xml:space"), "preserve")

        text_element.text = text
        copied.append(text_element)
        return copied

    @classmethod
    def _field_runs(
        cls,
        field_code: str,
        instruction_parts: list[str] | None = None,
    ) -> list[object]:
        """Build the begin, instruction, and end runs for a complex field."""
        begin_run = OxmlElement("w:r")
        begin_char = OxmlElement("w:fldChar")
        begin_char.set(qn("w:fldCharType"), "begin")
        begin_run.append(begin_char)

        parts = instruction_parts or [f" {field_code} "]
        instruction_runs: list[object] = []

        for part in parts:
            instruction_run = OxmlElement("w:r")
            instruction = OxmlElement("w:instrText")

            if part[:1].isspace() or part[-1:].isspace():
                instruction.set(qn("xml:space"), "preserve")

            instruction.text = part
            instruction_run.append(instruction)
            instruction_runs.append(instruction_run)

        end_run = OxmlElement("w:r")
        end_char = OxmlElement("w:fldChar")
        end_char.set(qn("w:fldCharType"), "end")
        end_run.append(end_char)

        return [begin_run, *instruction_runs, end_run]
