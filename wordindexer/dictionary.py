"""
Dictionary loader for WordIndexer.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from wordindexer.models import DictionaryEntry


@dataclass(slots=True)
class DictionaryInfo:
    """Basic information about a dictionary."""

    name: str
    version: str
    author: str
    entries: int


class DictionaryLoader:
    """Load WordIndexer JSON dictionaries."""

    def __init__(self, filename: str | Path):
        self.path = Path(filename)

        if not self.path.exists():
            raise FileNotFoundError(f"Dictionary not found: {self.path}")

        with self.path.open("r", encoding="utf-8") as f:
            self.data = json.load(f)

    def info(self) -> DictionaryInfo:
        """Return dictionary metadata."""
        metadata = self.data.get("metadata", {})
        entries = self.data.get("entries", [])

        return DictionaryInfo(
            name=metadata.get("name", ""),
            version=metadata.get("version", ""),
            author=metadata.get("author", ""),
            entries=len(entries),
        )

    def load_entries(self) -> list[DictionaryEntry]:
        """Load all dictionary entries, including reference metadata."""
        entries: list[DictionaryEntry] = []

        for item in self.data.get("entries", []):
            see_also = item.get("see_also", [])

            if isinstance(see_also, str):
                see_also = [see_also]

            entries.append(
                DictionaryEntry(
                    term=item.get("term", ""),
                    aliases=item.get("aliases", []),
                    category=item.get("category", ""),
                    enabled=item.get("enabled", True),
                    index_as=item.get("index_as", item.get("term", "")),
                    parent=item.get("parent"),
                    subentry=item.get("subentry"),
                    see=item.get("see"),
                    see_also=see_also,
                )
            )

        return entries
