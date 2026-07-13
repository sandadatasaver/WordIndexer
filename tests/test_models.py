from wordindexer.models import Book


def test_book():

    book = Book()

    assert book.title == ""

    assert len(book.paragraphs) == 0