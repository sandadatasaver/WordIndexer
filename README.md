# WordIndexer

WordIndexer is an open-source Python tool that inserts native Microsoft Word XE (Index Entry) fields into `.docx` manuscripts. It helps authors, researchers, educators, publishers, and technical writers create professional indexes from configurable JSON dictionaries.

## Current release

**Version:** 0.1.0 — First Usable Core

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
- Excludes front matter using an explicit TOC boundary or first-chapter fallback.
- Saves a new indexed document without modifying the source document.
- Provides a command-line interface.

## Current limitations

Version 0.1.0 searches normal body paragraphs and headings. It does not yet index text inside:

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

The source document is not modified. The output document contains XE fields. To create the visible index in Microsoft Word, open the output document and choose:

```text
References → Insert Index → OK
```

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
