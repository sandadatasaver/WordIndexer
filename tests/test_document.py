from pathlib import Path

from wordindexer.document import DocumentReader


def test_sample_document_exists():
    assert Path("input/sample.docx").exists()


def test_document_reader():
    reader = DocumentReader("input/sample.docx")

    info = reader.inspect()

    assert info.paragraphs >= 0
    assert info.tables >= 0
    assert info.images >= 0