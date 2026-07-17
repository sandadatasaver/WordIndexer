"""
Deterministic glossary generation from dictionary definitions.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from wordindexer.dictionary import DictionaryEntry
from wordindexer.reports import ReportBuilder


@dataclass(slots=True)
class GlossaryEntry:
    """One glossary term and its dictionary-provided definition."""

    term: str
    definition: str
    category: str
    aliases: list[str]
    occurrences: int
    found: bool
    source: str


@dataclass(slots=True)
class GlossaryReport:
    """Structured glossary output."""

    input_path: str
    entries: list[GlossaryEntry]

    def as_dict(self) -> dict:
        return {
            "input_path": self.input_path,
            "entries": [asdict(entry) for entry in self.entries],
        }

    def write_json(self, filename: str | Path) -> Path:
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.as_dict(), indent=2),
            encoding="utf-8",
        )
        return path

    def write_csv(self, filename: str | Path) -> Path:
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(
                stream,
                fieldnames=[
                    "term",
                    "definition",
                    "category",
                    "aliases",
                    "occurrences",
                    "found",
                    "source",
                ],
            )
            writer.writeheader()

            for entry in self.entries:
                row = asdict(entry)
                row["aliases"] = "; ".join(entry.aliases)
                writer.writerow(row)

        return path


class GlossaryBuilder:
    """Build a glossary without modifying the source document."""

    def build(
        self,
        input_path: str | Path,
        dictionary: list[DictionaryEntry],
        include_tables: bool = False,
    ) -> GlossaryReport:
        analysis = ReportBuilder().build(
            input_path,
            dictionary,
            include_tables=include_tables,
        )

        counts = analysis.term_counts
        entries: list[GlossaryEntry] = []
        seen: set[str] = set()

        for dictionary_entry in dictionary:
            if not dictionary_entry.enabled:
                continue
            if not dictionary_entry.include_in_glossary:
                continue
            if not dictionary_entry.definition:
                continue

            canonical = dictionary_entry.index_as or dictionary_entry.term

            if canonical in seen:
                continue

            seen.add(canonical)
            occurrences = counts.get(canonical, 0)

            entries.append(
                GlossaryEntry(
                    term=canonical,
                    definition=dictionary_entry.definition,
                    category=dictionary_entry.category,
                    aliases=list(dictionary_entry.aliases),
                    occurrences=occurrences,
                    found=occurrences > 0,
                    source=dictionary_entry.source or "dictionary",
                )
            )

        entries.sort(key=lambda entry: entry.term.casefold())

        return GlossaryReport(
            input_path=str(input_path),
            entries=entries,
        )
