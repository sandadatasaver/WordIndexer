"""
High-level document workflows shared by the CLI and GUI.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from wordindexer.backmatter import BackMatterWriter
from wordindexer.dictionary import DictionaryEntry
from wordindexer.document import DocumentReader
from wordindexer.glossary import GlossaryBuilder, GlossaryReport
from wordindexer.index import IndexEngine


@dataclass(slots=True)
class WorkflowResult:
    output_path: Path
    index_fields: int
    glossary_entries: int


class DocumentWorkflow:
    """Coordinate index and glossary output without UI-specific logic."""

    def run(
        self,
        input_path: str | Path,
        dictionary: list[DictionaryEntry],
        output_path: str | Path,
        *,
        generate_index: bool = True,
        generate_glossary: bool = False,
        include_tables: bool = False,
        remove_sections: list[str] | None = None,
    ) -> WorkflowResult:
        """Generate a cleaned document with the selected output features."""
        destination = Path(output_path)
        report: GlossaryReport | None = None

        if generate_glossary:
            report = GlossaryBuilder().build(
                input_path,
                dictionary,
                include_tables=include_tables,
                remove_sections=remove_sections,
            )

        IndexEngine(
            include_index_field=False,
            include_tables=include_tables,
            remove_sections=remove_sections,
        ).index(
            input_path=input_path,
            dictionary=dictionary,
            output_path=destination,
        )

        document = DocumentReader(destination).doc
        BackMatterWriter().rebuild(
            document,
            report,
            include_index_field=generate_index,
            include_index_heading=generate_index,
            include_glossary=generate_glossary,
        )
        document.save(destination)

        index_fields = len(
            [
                element
                for paragraph in document.paragraphs
                for element in paragraph._p.xpath(".//w:instrText")
                if element.text and "INDEX" not in element.text
            ]
        )

        return WorkflowResult(
            output_path=destination,
            index_fields=index_fields,
            glossary_entries=len(report.entries) if report else 0,
        )
