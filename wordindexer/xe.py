"""
Microsoft Word XE field writer.

This module translates a resolved WordIndexer Match into an XE field and
delegates the low-level WordprocessingML work to XMLWriter.
"""

from __future__ import annotations

from docx.text.paragraph import Paragraph

from wordindexer.models import Match
from wordindexer.xmlwriter import XMLWriter


class XEWriter:
    """Create Microsoft Word index-entry fields for matched text."""

    def __init__(self, xml_writer: XMLWriter | None = None):
        self.xml_writer = xml_writer or XMLWriter()

    @staticmethod
    def escape_entry_text(term: str) -> str:
        """
        Escape characters with meaning in Word's XE entry syntax.

        Version 1 treats the canonical term as one primary entry. Colons and
        semicolons are therefore escaped so punctuation in a term is not
        interpreted as a subentry or sort override.
        """
        return (
            term.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace(":", "\\:")
            .replace(";", "\\;")
        )

    @classmethod
    def field_code(cls, term: str) -> str:
        """Return the canonical Word XE field instruction."""
        if not term or not term.strip():
            raise ValueError("An XE entry term must not be empty")

        escaped = cls.escape_entry_text(term.strip())
        return f'XE "{escaped}"'

    def insert_match(
        self,
        paragraph: Paragraph,
        match: Match,
    ) -> None:
        """Insert one XE field immediately after the matched text."""
        if not match.locations:
            raise ValueError(
                "Match must contain run locations before an XE field is inserted"
            )

        location = match.locations[-1]
        escaped = self.escape_entry_text(match.term.strip())

        self.xml_writer.insert_field(
            paragraph=paragraph,
            run_index=location.run_index,
            offset=location.end,
            field_code=self.field_code(match.term),
            instruction_parts=[
                ' XE "',
                escaped,
                '" ',
            ],
        )
