# WordIndexer 0.2.0

## Automatic Index Field

WordIndexer 0.2.0 automatically appends an `Index` heading and a Word INDEX field to generated documents.

Run:

```powershell
python book_indexer.py index input/sample.docx dictionaries/technology/powershell.json output/sample_indexed.docx
```

Then open the output in Microsoft Word and update all fields:

```text
Ctrl+A → F9
```

The `--no-index-field` option is available when only XE fields are required.

## Validation

This release was validated with:

- Automated regression tests.
- A sample DOCX.
- A torture document with complex formatting and structures.
- A real PowerShell manuscript.
- Microsoft Word index generation with page numbers.

## Scope note

This release deliberately indexes normal body paragraphs and headings. Tables, headers, footers, footnotes, endnotes, and text boxes are deferred until separately tested support is implemented.
