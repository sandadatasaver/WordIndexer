"""First WordIndexer desktop GUI prototype."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

from wordindexer.dictionary import DictionaryLoader
from wordindexer.dictionary_builder import DictionaryDraftBuilder
from wordindexer.gui.help_dialog import HelpDialog
from wordindexer.discovery import TermDiscovery
from wordindexer.reports import ReportBuilder
from wordindexer.workflow import DocumentWorkflow

from PySide6.QtCore import QObject, QThread, Qt, Signal, Slot
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (

    QApplication,
    QCheckBox,
    QFileDialog,
    QFormLayout,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


def resource_path(relative_path: str) -> Path:
    """Resolve an asset in source and PyInstaller layouts."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    return base / relative_path


class TaskWorker(QObject):
    """Run one document task outside the GUI thread."""

    finished = Signal(object)
    failed = Signal(str)

    def __init__(self, task: Callable[[], object]):
        super().__init__()
        self.task = task

    @Slot()
    def run(self):
        try:
            self.finished.emit(self.task())
        except Exception as error:
            self.failed.emit(str(error))


class MainWindow(QMainWindow):
    """Simple desktop workflow for indexing and glossary generation."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("WordIndexer")
        icon_path = resource_path("branding/WordIndexer_icon_user.png")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        self.resize(820, 520)
        self.thread: QThread | None = None
        self.worker: TaskWorker | None = None
        self.success_callback: Callable[[object], None] | None = None
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        header = QHBoxLayout()
        logo_label = QLabel()
        icon_path = resource_path("branding/WordIndexer_icon_user.png")
        if icon_path.exists():
            pixmap = QPixmap(str(icon_path)).scaled(
                112,
                112,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            logo_label.setPixmap(pixmap)
        logo_label.setFixedSize(120, 120)
        header.addWidget(logo_label)

        brand_text = QVBoxLayout()
        title = QLabel("WordIndexer")
        title.setStyleSheet(
            "font-size: 28px; font-weight: 700; color: #c99700;"
        )
        mission = QLabel(
            "Professional indexing and glossary tools for authors, "
            "researchers, and educators."
        )
        mission.setWordWrap(True)
        mission.setStyleSheet("color: #a87900; font-weight: 600;")
        brand_text.addWidget(title)
        brand_text.addWidget(mission)
        brand_text.addWidget(
            QLabel(
                "This tool is provided 100% free for the Glory of Jesus "
                "and for the advancement of Academic Research."
            )
        )
        header.addLayout(brand_text, 1)

        help_button = QPushButton("Help / FAQ")
        help_button.clicked.connect(self.show_help)
        header.addWidget(help_button)

        about_button = QPushButton("About")
        about_button.clicked.connect(self.show_about)
        header.addWidget(about_button)
        layout.addLayout(header)

        form = QFormLayout()

        self.document_edit = QLineEdit()
        form.addRow(
            "Manuscript:",
            self._browse_row(
                self.document_edit,
                self._choose_document,
                "Browse DOCX",
            ),
        )

        self.dictionary_edit = QLineEdit()
        form.addRow(
            "Dictionary:",
            self._browse_row(
                self.dictionary_edit,
                self._choose_dictionary,
                "Browse JSON",
            ),
        )

        self.output_edit = QLineEdit()
        form.addRow(
            "Output folder:",
            self._browse_row(
                self.output_edit,
                self._choose_output,
                "Browse folder",
            ),
        )

        self.remove_section_edit = QLineEdit()
        self.remove_section_edit.setPlaceholderText(
            "Optional Heading 1 section to remove"
        )
        form.addRow("Remove section:", self.remove_section_edit)
        layout.addLayout(form)

        options = QHBoxLayout()
        self.index_check = QCheckBox("Generate Index")
        self.index_check.setChecked(True)
        self.glossary_check = QCheckBox("Generate Glossary")
        self.tables_check = QCheckBox("Include table cells")
        options.addWidget(self.index_check)
        options.addWidget(self.glossary_check)
        options.addWidget(self.tables_check)
        layout.addLayout(options)

        buttons = QHBoxLayout()
        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.clicked.connect(self.analyze)
        self.draft_button = QPushButton("Generate Dictionary Draft")
        self.draft_button.clicked.connect(self.generate_draft)
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_workflow)
        buttons.addWidget(self.analyze_button)
        buttons.addWidget(self.draft_button)
        buttons.addWidget(self.run_button)
        layout.addLayout(buttons)
        self.buttons = [
            self.analyze_button,
            self.draft_button,
            self.run_button,
        ]

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Ready")
        layout.addWidget(self.progress_bar)

        layout.addWidget(QLabel("Progress and report output"))
        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        layout.addWidget(self.log_edit)

    @staticmethod
    def _browse_row(edit: QLineEdit, callback, label: str):
        widget = QWidget()
        row = QHBoxLayout(widget)
        row.setContentsMargins(0, 0, 0, 0)
        row.addWidget(edit)
        button = QPushButton(label)
        button.clicked.connect(callback)
        row.addWidget(button)
        return widget

    def show_help(self):
        HelpDialog(self).exec()

    def show_about(self):
        from wordindexer.version import VERSION

        QMessageBox.about(
            self,
            "About WordIndexer",
            "<h2>WordIndexer {}</h2>"
            "<p><b>Publisher:</b> Bishop David Sanda Ph.D</p>"
            "<p><b>License:</b> MIT</p>"
            "<p>This tool is provided 100% free for the Glory of Jesus "
            "and for the advancement of Academic Research.</p>"
            "<p>WordIndexer helps authors, researchers, educators, and "
            "publishers create professional indexes and glossaries.</p>".format(VERSION),
        )

    def _choose_document(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select manuscript",
            "",
            "Word documents (*.docx)",
        )
        if filename:
            self.document_edit.setText(filename)

    def _choose_dictionary(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select dictionary",
            "",
            "JSON files (*.json)",
        )
        if filename:
            self.dictionary_edit.setText(filename)

    def _choose_output(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select output folder",
        )
        if folder:
            self.output_edit.setText(folder)

    def _paths(self):
        document = Path(self.document_edit.text().strip())
        dictionary = Path(self.dictionary_edit.text().strip())
        output_folder = Path(self.output_edit.text().strip())

        if not document.exists():
            raise ValueError("Select an existing manuscript DOCX file")
        if not dictionary.exists():
            raise ValueError("Select an existing dictionary JSON file")
        output_folder.mkdir(parents=True, exist_ok=True)

        return document, dictionary, output_folder

    def _entries(self):
        _, dictionary, _ = self._paths()
        return DictionaryLoader(dictionary).load_entries()

    def _remove_sections(self):
        value = self.remove_section_edit.text().strip()
        return [value] if value else []

    def _start_task(
        self,
        task: Callable[[], object],
        success: Callable[[object], None],
        label: str,
    ):
        if self.thread is not None:
            return

        for button in self.buttons:
            button.setEnabled(False)

        self.progress_bar.setRange(0, 0)
        self.progress_bar.setFormat("Working...")
        self.statusBar().showMessage(label)

        self.log_edit.setPlainText(
            f"{label}\nWorking in the background; the window should remain responsive..."
        )

        self.success_callback = success
        self.thread = QThread()
        self.worker = TaskWorker(task)
        thread = self.thread
        worker = self.worker
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(self._task_finished)
        worker.failed.connect(self._task_failed)
        worker.finished.connect(thread.quit)
        worker.failed.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.failed.connect(worker.deleteLater)
        thread.finished.connect(self._thread_finished)
        thread.finished.connect(thread.deleteLater)
        thread.start()

    @Slot(object)
    def _task_finished(self, result):
        if self.success_callback is not None:
            self.success_callback(result)

    @Slot(str)
    def _task_failed(self, message: str):
        self._show_error(ValueError(message))

    @Slot()
    def _thread_finished(self):
        for button in self.buttons:
            button.setEnabled(True)

        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        self.progress_bar.setFormat("Complete")
        self.statusBar().showMessage("Ready")

        self.thread = None
        self.worker = None
        self.success_callback = None

    def analyze(self):
        try:
            document, _, _ = self._paths()
            entries = self._entries()
            include_tables = self.tables_check.isChecked()
            remove_sections = self._remove_sections()

            def task():
                return ReportBuilder().build(
                    document,
                    entries,
                    include_tables=include_tables,
                    remove_sections=remove_sections,
                )

            self._start_task(
                task,
                lambda report: self.log_edit.setPlainText(
                    report.render_console()
                ),
                "Analyzing manuscript",
            )
        except Exception as error:
            self._show_error(error)

    def generate_draft(self):
        try:
            document, _, output_folder = self._paths()
            entries = self._entries()
            candidates = output_folder / "generated_candidates.json"
            draft = output_folder / "generated_dictionary_draft.json"
            csv = output_folder / "generated_dictionary_draft.csv"
            include_tables = self.tables_check.isChecked()
            remove_sections = self._remove_sections()

            def task():
                report = TermDiscovery(
                    minimum_occurrences=2,
                ).discover(
                    document,
                    entries,
                    include_tables=include_tables,
                    remove_sections=remove_sections,
                )
                report.write_json(candidates)
                DictionaryDraftBuilder().build(
                    candidates,
                    draft,
                    csv_output=csv,
                )
                return report, draft, csv

            def completed(result):
                report, draft_path, csv_path = result
                self.dictionary_edit.setText(str(draft_path))
                self.log_edit.setPlainText(
                    f"Candidates: {len(report.candidates)}\n"
                    f"JSON draft: {draft_path}\n"
                    f"CSV review: {csv_path}"
                )

            self._start_task(task, completed, "Generating dictionary draft")
        except Exception as error:
            self._show_error(error)

    def run_workflow(self):
        try:
            document, _, output_folder = self._paths()
            entries = self._entries()
            suffix = "_indexed"
            if self.glossary_check.isChecked():
                suffix += "_glossary"
            output = output_folder / f"{document.stem}{suffix}.docx"
            generate_index = self.index_check.isChecked()
            generate_glossary = self.glossary_check.isChecked()
            include_tables = self.tables_check.isChecked()
            remove_sections = self._remove_sections()

            def task():
                return DocumentWorkflow().run(
                    document,
                    entries,
                    output,
                    generate_index=generate_index,
                    generate_glossary=generate_glossary,
                    include_tables=include_tables,
                    remove_sections=remove_sections,
                )

            def completed(result):
                self.log_edit.setPlainText(
                    f"Output: {result.output_path}\n"
                    f"Index fields: {result.index_fields}\n"
                    f"Glossary entries: {result.glossary_entries}"
                )

            self._start_task(task, completed, "Generating document")
        except Exception as error:
            self._show_error(error)

    def _show_error(self, error: Exception):
        QMessageBox.critical(self, "WordIndexer error", str(error))


def main() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()
