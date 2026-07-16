# WordIndexer 0.1.0

## First Usable Core

WordIndexer 0.1.0 is the first release that can take a DOCX manuscript and JSON dictionary, insert Word-compatible XE fields for every resolved occurrence, and save a new indexed DOCX.

## Validation

This release was validated with:

- Automated regression tests.
- A sample DOCX.
- A torture document with complex formatting and structures.
- A real PowerShell manuscript.
- Microsoft Word index generation with page numbers.

## Usage

```powershell
python book_indexer.py index input/sample.docx dictionaries/technology/powershell.json output/sample_indexed.docx
```

Open the output in Word and choose **References → Insert Index**.

## Scope note

This release deliberately indexes normal body paragraphs and headings. Tables, headers, footers, footnotes, endnotes, and text boxes are deferred until separately tested support is implemented.
