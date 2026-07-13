"""
Document reader for WordIndexer.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from docx import Document

from wordindexer.exceptions import DocumentError


@dataclass(slots=True)
class DocumentInfo:
    title: str
    author: str
    subject: str
    paragraphs: int
    tables: int
    images: int


class DocumentReader:

    def __init__(self, filename: str | Path):

        self.path = Path(filename)

        if not self.path.exists():
            raise DocumentError(f"Document not found: {self.path}")

        self.doc = Document(self.path)

    def inspect(self) -> DocumentInfo:

        props = self.doc.core_properties

        image_count = 0

        for rel in self.doc.part.rels.values():
            if "image" in rel.target_ref:
                image_count += 1

        return DocumentInfo(
            title=props.title or "",
            author=props.author or "",
            subject=props.subject or "",
            paragraphs=len(self.doc.paragraphs),
            tables=len(self.doc.tables),
            images=image_count,
        )
        def load_book(self) -> Book: