"""
Build and finalize reviewable dictionary drafts from discovery reports.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


class DictionaryDraftBuilder:
    """Convert discovery candidates into standard dictionary files."""

    def _build_data(
        self,
        discovery_path: str | Path,
        *,
        name: str,
        version: str,
        author: str,
        enable_candidates: bool,
    ) -> dict:
        source = Path(discovery_path)
        data = json.loads(source.read_text(encoding="utf-8"))
        entries: list[dict] = []

        for candidate in data.get("candidates", []):
            suggested = dict(candidate.get("suggested_entry", {}))

            if not suggested:
                suggested = {
                    "term": candidate.get("term", ""),
                    "aliases": candidate.get("variants", [])[1:],
                    "index_as": candidate.get("term", ""),
                    "category": candidate.get("category", ""),
                }

            suggested["enabled"] = enable_candidates
            suggested["source"] = "discovery"
            suggested["evidence"] = {
                "occurrences": candidate.get("occurrences", 0),
                "paragraphs": candidate.get("paragraphs", []),
                "contexts": candidate.get("contexts", []),
            }
            entries.append(suggested)

        return {
            "metadata": {
                "name": name,
                "version": version,
                "author": author,
                "generated_from": str(source),
                "review_required": not enable_candidates,
            },
            "entries": entries,
        }

    def build(
        self,
        discovery_path: str | Path,
        output_path: str | Path,
        *,
        name: str = "Generated Dictionary Draft",
        version: str = "0.1",
        author: str = "WordIndexer",
        enable_candidates: bool = False,
        csv_output: str | Path | None = None,
    ) -> Path:
        """Write a JSON draft and optionally a review CSV."""
        result = self._build_data(
            discovery_path,
            name=name,
            version=version,
            author=author,
            enable_candidates=enable_candidates,
        )
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(result, indent=2),
            encoding="utf-8",
        )

        if csv_output:
            self.write_csv(result, csv_output)

        return destination

    @staticmethod
    def _split_values(value: str | None) -> list[str]:
        if not value:
            return []
        return [part.strip() for part in value.split(";") if part.strip()]

    @staticmethod
    def _parse_bool(value: str | None) -> bool:
        return str(value or "").strip().casefold() in {
            "1",
            "true",
            "yes",
            "y",
            "on",
        }

    def finalize_csv(
        self,
        csv_path: str | Path,
        output_path: str | Path,
        *,
        name: str = "Reviewed Dictionary",
        version: str = "1.0",
        author: str = "WordIndexer",
    ) -> Path:
        """Convert an edited review CSV into a production dictionary."""
        source = Path(csv_path)
        entries: list[dict] = []

        with source.open("r", newline="", encoding="utf-8-sig") as stream:
            for row in csv.DictReader(stream):
                term = (row.get("term") or "").strip()
                if not term:
                    continue

                entry = {
                    "term": term,
                    "aliases": self._split_values(row.get("aliases")),
                    "index_as": (
                        row.get("index_as") or term
                    ).strip(),
                    "parent": (row.get("parent") or "").strip(),
                    "subentry": (row.get("subentry") or "").strip(),
                    "definition": (row.get("definition") or "").strip(),
                    "see": (row.get("see") or "").strip(),
                    "see_also": self._split_values(row.get("see_also")),
                    "category": (row.get("category") or "").strip(),
                    "enabled": self._parse_bool(row.get("enabled")),
                    "include_in_glossary": self._parse_bool(
                        row.get("include_in_glossary", "true")
                    ),
                    "source": (row.get("source") or "reviewed").strip(),
                }

                entries.append(
                    {
                        key: value
                        for key, value in entry.items()
                        if value not in ("", [], None)
                    }
                )

        result = {
            "metadata": {
                "name": name,
                "version": version,
                "author": author,
                "generated_from": str(source),
                "review_required": False,
            },
            "entries": entries,
        }
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(result, indent=2),
            encoding="utf-8",
        )
        return destination

    @staticmethod
    def write_csv(data: dict, filename: str | Path) -> Path:
        """Write a flat review CSV from dictionary draft data."""
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(
                stream,
                fieldnames=[
                    "term",
                    "aliases",
                    "index_as",
                    "parent",
                    "subentry",
                    "definition",
                    "see",
                    "see_also",
                    "category",
                    "enabled",
                    "include_in_glossary",
                    "source",
                    "occurrences",
                    "paragraphs",
                    "contexts",
                ],
            )
            writer.writeheader()

            for entry in data.get("entries", []):
                evidence = entry.get("evidence", {})
                writer.writerow(
                    {
                        "term": entry.get("term", ""),
                        "aliases": "; ".join(entry.get("aliases", [])),
                        "index_as": entry.get(
                            "index_as",
                            entry.get("term", ""),
                        ),
                        "parent": entry.get("parent", ""),
                        "subentry": entry.get("subentry", ""),
                        "definition": entry.get("definition", ""),
                        "see": entry.get("see", ""),
                        "see_also": "; ".join(
                            entry.get("see_also", [])
                        ),
                        "category": entry.get("category", ""),
                        "enabled": entry.get("enabled", False),
                        "include_in_glossary": entry.get(
                            "include_in_glossary",
                            True,
                        ),
                        "source": entry.get("source", ""),
                        "occurrences": evidence.get("occurrences", 0),
                        "paragraphs": "; ".join(
                            str(value)
                            for value in evidence.get("paragraphs", [])
                        ),
                        "contexts": " | ".join(
                            evidence.get("contexts", [])
                        ),
                    }
                )

        return path
