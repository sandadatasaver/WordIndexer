"""
Dry-run analysis and coverage reports for WordIndexer.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from wordindexer.dictionary import DictionaryEntry
from wordindexer.document import DocumentReader
from wordindexer.search import SearchEngine
from wordindexer.toc import TOCDetector


@dataclass(slots=True)
class AnalysisReport:
    """Structured result of a non-modifying analysis run."""

    input_path: str
    total_paragraphs: int
    body_start: int
    ignored_paragraphs: int
    toc_detected: bool
    toc_method: str
    dictionary_entries: int
    terms_found: int
    terms_missing: int
    total_occurrences: int
    overlaps_resolved: int
    term_counts: dict[str, int]
    missing_terms: list[str]

    def as_dict(self) -> dict:
        """Return a JSON-serializable representation."""
        return asdict(self)

    def write_json(self, filename: str | Path) -> Path:
        """Write the report as formatted JSON."""
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.as_dict(), indent=2),
            encoding="utf-8",
        )
        return path

    def render_console(self) -> str:
        """Render a human-readable console report."""
        lines = [
            "",
            "WordIndexer Analysis Report",
            "============================",
            f"Document          : {self.input_path}",
            f"Paragraphs        : {self.total_paragraphs}",
            f"Body starts       : {self.body_start}",
            f"Ignored paragraphs: {self.ignored_paragraphs}",
            f"TOC detected      : {self.toc_detected}",
            f"TOC method        : {self.toc_method}",
            "",
            "Coverage",
            "--------",
            f"Dictionary entries: {self.dictionary_entries}",
            f"Terms found       : {self.terms_found}",
            f"Terms missing     : {self.terms_missing}",
            f"Total occurrences : {self.total_occurrences}",
            f"Overlaps resolved : {self.overlaps_resolved}",
            "",
            "Term counts",
            "-----------",
        ]

        if self.term_counts:
            for term, count in sorted(
                self.term_counts.items(),
                key=lambda item: (-item[1], item[0].casefold()),
            ):
                lines.append(f"{term:<35} {count}")
        else:
            lines.append("No dictionary terms were found.")

        lines.extend(["", "Missing terms", "-------------"])

        if self.missing_terms:
            lines.extend(self.missing_terms)
        else:
            lines.append("None")

        return "\n".join(lines)


class ReportBuilder:
    """Build a dry-run analysis report without modifying the DOCX."""

    def build(
        self,
        input_path: str | Path,
        dictionary: list[DictionaryEntry],
        include_tables: bool = False,
    ) -> AnalysisReport:
        """Analyze a document and return its structured coverage report."""
        source = Path(input_path)
        reader = DocumentReader(source)
        book = reader.load_book(include_tables=include_tables)
        toc = TOCDetector().detect(reader.doc, book.paragraphs)

        book.paragraphs = [
            paragraph
            for paragraph in book.paragraphs
            if paragraph.index >= toc.body_start
        ]
        book.headings = [
            heading
            for heading in book.headings
            if heading.paragraph_index >= toc.body_start
        ]

        engine = SearchEngine(book, reader.doc)
        results = engine.search(dictionary)

        active_entries = [
            entry
            for entry in dictionary
            if entry.enabled and entry.term
        ]
        canonical_terms = list(
            dict.fromkeys(
                entry.index_as or entry.term
                for entry in active_entries
            )
        )
        term_counts = {
            term: len(results.get(term, []))
            for term in canonical_terms
        }
        missing_terms = [
            term
            for term, count in term_counts.items()
            if count == 0
        ]

        return AnalysisReport(
            input_path=str(source),
            total_paragraphs=len(reader.doc.paragraphs),
            body_start=toc.body_start,
            ignored_paragraphs=toc.body_start,
            toc_detected=toc.found,
            toc_method=toc.method,
            dictionary_entries=len(canonical_terms),
            terms_found=len(canonical_terms) - len(missing_terms),
            terms_missing=len(missing_terms),
            total_occurrences=sum(term_counts.values()),
            overlaps_resolved=(
                engine.raw_match_count - engine.resolved_match_count
            ),
            term_counts=term_counts,
            missing_terms=missing_terms,
        )
