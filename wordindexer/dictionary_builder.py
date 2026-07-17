"""
Build reviewable dictionary drafts from discovery reports.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


class DictionaryDraftBuilder:
    """Convert discovery candidates into a standard dictionary draft."""

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
                    "category",
                    "enabled",
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
                        "category": entry.get("category", ""),
                        "enabled": entry.get("enabled", False),
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
