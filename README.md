# WordIndexer

WordIndexer is an open-source Python tool that inserts native Microsoft Word XE (Index Entry) fields into `.docx` manuscripts. It helps authors, researchers, educators, publishers, and technical writers create professional indexes from configurable JSON dictionaries.

## Current release

**Version:** 0.4.0 — Optional Table-Cell Indexing

The current release has been tested against:

- A sample Word document.
- A torture-test document containing complex formatting and document structures.
- A real PowerShell manuscript.

## Features

- Reads Microsoft Word `.docx` documents.
- Loads JSON dictionaries with terms, aliases, and canonical index names.
- Finds every occurrence of enabled terms.
- Indexes aliases under one canonical term using `index_as`.
- Resolves overlapping matches by preferring the most specific match.
- Preserves visible text and run formatting.
- Inserts Word-compatible XE fields.
- Appends a real Word `INDEX` field automatically.
- Adds an `Index` heading before the generated index field.
- Excludes front matter using an explicit TOC boundary or first-chapter fallback.
- Saves a new indexed document without modifying the source document.
- Provides a command-line interface.
- Produces dry-run coverage reports without modifying the manuscript.
- Exports analysis reports as JSON.

## Current limitations

Version 0.2.0 searches normal body paragraphs and headings. It does not yet index text inside:

- Table cells.
- Headers and footers.
- Footnotes and endnotes.
- Text boxes and other embedded Word stories.

These are planned for later hardening and Version 2 work. The current scope is intentionally limited so that the core engine remains predictable and testable.

## Installation

WordIndexer requires Python 3.12 or newer.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

Use `python -m pytest`, rather than a possibly unrelated global `pytest`, so tests run with the active virtual environment.

## Command-line usage

### Inspect a document

```powershell
python book_indexer.py inspect input/sample.docx
```

### Analyze a document

```powershell
python book_indexer.py analyze input/sample.docx dictionaries/technology/powershell.json
```

### Create an indexed document

```powershell
python book_indexer.py index `
    input/sample.docx `
    dictionaries/technology/powershell.json `
    output/sample_indexed.docx
```

For a single-line command:

```powershell
python book_indexer.py index input/sample.docx dictionaries/technology/powershell.json output/sample_indexed.docx
```

The command automatically adds:

- XE fields for matched entries.
- An `Index` heading.
- A Word `INDEX` field on a new page.

Open the output document in Word and press:

```text
Ctrl+A → F9
```

Word will populate the visible index. To create only XE fields without appending the INDEX field, use:

```powershell
python book_indexer.py index input/sample.docx dictionaries/technology/powershell.json output/sample_indexed.docx --no-index-field
```

The source document is never modified.

To include table-cell content explicitly:

```powershell
python book_indexer.py index input/sample.docx dictionaries/technology/powershell.json output/sample_with_tables.docx --include-tables
```

The default remains paragraph-only indexing.

## Dictionary format

```json
{
  "metadata": {
    "name": "PowerShell Dictionary",
    "version": "1.0",
    "author": "WordIndexer"
  },
  "entries": [
    {
      "term": "Get-ChildItem",
      "aliases": ["gci", "dir", "ls"],
      "index_as": "Get-ChildItem",
      "category": "Cmdlet",
      "enabled": true
    }
  ]
}
```

## Development

Run the test suite from the project root:

```powershell
python -m pytest -q
```

The project follows a staged workflow: write a focused test, implement one capability, run the full suite, validate a generated DOCX in Word, and commit only after the result is confirmed.

## Project structure

```text
WordIndexer/
├── book_indexer.py
├── config.json
├── requirements.txt
├── requirements-dev.txt
├── dictionaries/
├── docs/
├── examples/
├── input/
├── output/
├── test_documents/
├── tests/
└── wordindexer/
```

## License

WordIndexer is released under the MIT License. See [LICENSE](LICENSE).
