"""Help and FAQ dialog for the WordIndexer GUI."""

from __future__ import annotations

from pathlib import Path
import sys

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QTabWidget,
    QTextBrowser,
    QVBoxLayout,
)


def resource_path(relative_path: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    return base / relative_path


class HelpDialog(QDialog):
    """Display concise help and frequently asked questions."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("WordIndexer Help and FAQ")
        self.resize(720, 520)

        tabs = QTabWidget()
        tabs.addTab(self._document_tab("docs/HELP.md"), "Quick Help")
        tabs.addTab(self._document_tab("docs/FAQ.md"), "FAQ")

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(tabs)
        layout.addWidget(buttons)

    @staticmethod
    def _document_tab(relative_path: str) -> QTextBrowser:
        browser = QTextBrowser()
        path = resource_path(relative_path)

        if path.exists():
            browser.setMarkdown(
                Path(path).read_text(encoding="utf-8")
            )
        else:
            browser.setPlainText("Help content is not available.")

        return browser
