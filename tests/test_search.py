from wordindexer.models import (
    Book,
    DictionaryEntry,
    Heading,
    Paragraph,
)

from wordindexer.search import SearchEngine


def test_search():

    book = Book()

    book.paragraphs.append(
        Paragraph(
            index=0,
            text="PowerShell uses Get-ChildItem.",
            style="Normal",
        )
    )

    dictionary = [

        DictionaryEntry(
            term="PowerShell",
            index_as="PowerShell",
        ),

        DictionaryEntry(
            term="Get-ChildItem",
            aliases=["gci"],
            index_as="Get-ChildItem",
        ),

    ]

    engine = SearchEngine(book)

    results = engine.search(dictionary)

    assert len(results["PowerShell"]) == 1
    assert len(results["Get-ChildItem"]) == 1


def test_heading_context():

    book = Book()

    book.paragraphs.append(
        Paragraph(
            index=0,
            text="Chapter One",
            style="Heading 1",
        )
    )

    book.headings.append(
        Heading(
            level=1,
            text="Chapter One",
            paragraph_index=0,
        )
    )

    book.paragraphs.append(
        Paragraph(
            index=1,
            text="PowerShell is powerful.",
            style="Normal",
        )
    )

    dictionary = [

        DictionaryEntry(
            term="PowerShell",
            index_as="PowerShell",
        )

    ]

    engine = SearchEngine(book)

    results = engine.search(dictionary)

    assert len(results["PowerShell"]) == 1
    assert results["PowerShell"][0].heading == "Chapter One"