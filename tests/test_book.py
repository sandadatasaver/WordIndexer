from wordindexer.document import DocumentReader


def test_load_book():

    reader = DocumentReader("input/sample.docx")

    book = reader.load_book()

    assert len(book.paragraphs) > 0