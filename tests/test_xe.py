from docx import Document

from wordindexer.models import Match, RunLocation
from wordindexer.xe import XEWriter


def test_xe_field_code_uses_canonical_term():
    assert XEWriter.field_code("PowerShell") == 'XE "PowerShell"'
    assert XEWriter.field_code("PowerShell: Basics") == (
        'XE "PowerShell\\: Basics"'
    )


def test_xe_field_code_escapes_special_characters():
    assert XEWriter.field_code('A "quoted"; term') == (
        'XE "A \\\"quoted\\\"\\; term"'
    )


def test_xe_writer_inserts_field_at_match_location():
    document = Document()
    paragraph = document.add_paragraph("Before PowerShell after")

    match = Match(
        term="PowerShell",
        matched_text="PowerShell",
        paragraph_index=0,
        paragraph_text=paragraph.text,
        locations=[
            RunLocation(
                paragraph_index=0,
                run_index=0,
                start=7,
                end=17,
                matched_text="PowerShell",
            )
        ],
    )

    XEWriter().insert_match(paragraph, match)

    assert paragraph.text == "Before PowerShell after"
    instructions = paragraph._p.xpath(".//w:instrText")
    assert [instruction.text for instruction in instructions] == [
        ' XE "',
        "PowerShell",
        '" ',
    ]


def test_xe_writer_indexes_alias_under_canonical_term():
    document = Document()
    paragraph = document.add_paragraph("Use gci here")

    match = Match(
        term="Get-ChildItem",
        matched_text="gci",
        paragraph_index=0,
        paragraph_text=paragraph.text,
        locations=[
            RunLocation(
                paragraph_index=0,
                run_index=0,
                start=4,
                end=7,
                matched_text="gci",
            )
        ],
    )

    XEWriter().insert_match(paragraph, match)

    instructions = paragraph._p.xpath(".//w:instrText")
    assert [instruction.text for instruction in instructions] == [
        ' XE "',
        "Get-ChildItem",
        '" ',
    ]
