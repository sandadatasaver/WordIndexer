"""
Microsoft Word XE field writer.

This module translates a resolved WordIndexer Match into an XE field and
delegates the low-level WordprocessingML work to XMLWriter.
"""

from __future__ import annotations

from docx.text.paragraph import Paragraph

from wordindexer.models import DictionaryEntry, Match
from wordindexer.xmlwriter import XMLWriter


class XEWriter:
    """Create Microsoft Word index-entry fields for matched text."""

    def __init__(self, xml_writer: XMLWriter | None = None):
        self.xml_writer = xml_writer or XMLWriter()

    @staticmethod
    def escape_entry_text(term: str) -> str:
        """
        Escape characters with meaning in Word's XE entry syntax.

        Colons are escaped when they occur inside one hierarchy component.
        Hierarchy separators are added separately by ``hierarchy_text``.
        """
        return (
            term.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace(":", "\\:")
            .replace(";", "\\;")
        )

    @classmethod
    def field_code(cls, term: str) -> str:
        """Return a flat canonical Word XE field instruction."""
        if not term or not term.strip():
            raise ValueError("An XE entry term must not be empty")

        escaped = cls.escape_entry_text(term.strip())
        return f'XE "{escaped}"'

    @classmethod
    def hierarchy_text(cls, entry: DictionaryEntry) -> str:
        """Return the primary/subentry hierarchy for one dictionary entry."""
        canonical = entry.index_as or entry.term

        if not canonical or not canonical.strip():
            raise ValueError("An XE entry term must not be empty")

        components = [
            component.strip()
            for component in (
                entry.parent,
                entry.subentry,
                canonical,
            )
            if component and component.strip()
        ]

        return ":".join(
            cls.escape_entry_text(component)
            for component in components
        )

    @classmethod
    def field_code_for_entry(cls, entry: DictionaryEntry) -> str:
        """Return a flat, hierarchical, or ``See`` XE instruction."""
        entry_text = cls.hierarchy_text(entry)

        if entry.see:
            target = cls.escape_entry_text(entry.see.strip())
            return f'XE "{entry_text}" \\t "See {target}"'

        return f'XE "{entry_text}"'

    @classmethod
    def see_also_text(cls, entry: DictionaryEntry) -> str:
        """Return the display text for a ``See also`` reference."""
        targets = [target.strip() for target in entry.see_also if target.strip()]

        if not targets:
            raise ValueError("see_also must contain at least one target")

        escaped_targets = "; ".join(
            cls.escape_entry_text(target)
            for target in targets
        )
        return f"See also {escaped_targets}"

    @classmethod
    def field_code_for_see_also(cls, entry: DictionaryEntry) -> str:
        """Return a Word XE cross-reference field for ``See also``."""
        return (
            f'XE "{cls.hierarchy_text(entry)}" '
            f'\\t "{cls.see_also_text(entry)}"'
        )

    @classmethod
    def instruction_parts_for_see_also(
        cls,
        entry: DictionaryEntry,
    ) -> list[str]:
        """Return Word-style instruction fragments for ``See also``."""
        return [
            ' XE "',
            cls.hierarchy_text(entry),
            '" \\t "',
            cls.see_also_text(entry),
            '" ',
        ]

    @classmethod
    def instruction_parts_for_entry(
        cls,
        entry: DictionaryEntry,
    ) -> list[str]:
        """Return Word-style instruction fragments for one dictionary entry."""
        entry_text = cls.hierarchy_text(entry)

        if entry.see:
            target = cls.escape_entry_text(entry.see.strip())
            return [
                ' XE "',
                entry_text,
                '" \\t "',
                f"See {target}",
                '" ',
            ]

        return [
            ' XE "',
            entry_text,
            '" ',
        ]

    def insert_match(
        self,
        paragraph: Paragraph,
        match: Match,
        include_see_also: bool = False,
    ) -> None:
        """Insert one XE field immediately after the matched text."""
        if not match.locations:
            raise ValueError(
                "Match must contain run locations before an XE field is inserted"
            )

        location = match.locations[-1]

        if match.dictionary_entry is not None:
            entry = match.dictionary_entry
            fields = [
                (
                    self.field_code_for_entry(entry),
                    self.instruction_parts_for_entry(entry),
                )
            ]

            if include_see_also and entry.see_also:
                fields.append(
                    (
                        self.field_code_for_see_also(entry),
                        self.instruction_parts_for_see_also(entry),
                    )
                )
        else:
            entry_text = self.escape_entry_text(match.term.strip())
            fields = [
                (
                    self.field_code(match.term),
                    [
                        ' XE "',
                        entry_text,
                        '" ',
                    ],
                )
            ]

        self.xml_writer.insert_fields(
            paragraph=paragraph,
            run_index=location.run_index,
            offset=location.end,
            fields=fields,
        )
