from docx import Document

from wordindexer.scanner import RunScanner


def test_run_scanner():

    doc = Document()

    p = doc.add_paragraph()

    p.add_run("PowerShell ")

    p.add_run("uses ")

    p.add_run("Get-ChildItem")

    scanner = RunScanner(doc)

    locations = scanner.locate(
        paragraph_index=0,
        term="Get-ChildItem",
    )

    assert len(locations) == 1

    assert locations[0].run_index == 2

    assert locations[0].matched_text == "Get-ChildItem"