"""
Dictionary loader for WordIndexer.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class DictionaryInfo:
    name: str
    version: str
    author: str
    entries: int


class DictionaryLoader:

    def __init__(self, filename: str | Path):

        self.path = Path(filename)

        if not self.path.exists():
            raise FileNotFoundError(self.path)

        with self.path.open("r", encoding="utf-8") as f:
            self.data = json.load(f)

    def info(self) -> DictionaryInfo:

        meta = self.data.get("metadata", {})
        entries = self.data.get("entries", [])

        return DictionaryInfo(
            name=meta.get("name", ""),
            version=meta.get("version", ""),
            author=meta.get("author", ""),
            entries=len(entries),
        )