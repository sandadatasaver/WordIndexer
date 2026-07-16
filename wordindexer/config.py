"""
Configuration Manager for WordIndexer.

Loads, validates and provides access to config.json.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_CONFIG = {
    "ignore_before_toc": True,
    "whole_word_only": True,
    "case_sensitive": False,
    "insert_first_occurrence_only": True,
    "expand_aliases": True,
    "generate_csv": True,
    "generate_json": True,
    "generate_log": True,
    "fuzzy_matching": False,
    "fuzzy_score": 90,
}


class ConfigManager:
    """
    Loads and validates the application configuration.
    """

    def __init__(self, filename: str = "config.json") -> None:
        self.path = Path(filename)
        self.data = DEFAULT_CONFIG.copy()

    def load(self) -> None:
        """
        Load configuration from disk.
        Missing values automatically receive defaults.
        """
        if not self.path.exists():
            return

        with self.path.open("r", encoding="utf-8") as f:
            user_config = json.load(f)

        if not isinstance(user_config, dict):
            raise ValueError("config.json must contain a JSON object.")

        self.data.update(user_config)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a configuration value.
        """
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def as_dict(self) -> dict[str, Any]:
        return dict(self.data)