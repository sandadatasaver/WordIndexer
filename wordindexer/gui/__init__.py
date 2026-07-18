"""Optional PySide6 desktop interface for WordIndexer."""

from __future__ import annotations


def run() -> int:
    """Launch the WordIndexer desktop application."""
    from wordindexer.gui.app import main

    return main()
