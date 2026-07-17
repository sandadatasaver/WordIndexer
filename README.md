# WordIndexer

WordIndexer is an open-source Python tool that inserts native Microsoft Word XE (Index Entry) fields into `.docx` manuscripts. It helps authors, researchers, educators, publishers, and technical writers create professional indexes from configurable JSON dictionaries.

## Current release

**Version:** 0.5.0 — Hierarchical Entries and Cross-References

The current release has been tested against:

- A sample Word document.
- A torture-test document containing complex formatting and document structures.
- A real PowerShell manuscript.

## Features

- Reads Microsoft Word `.docx` documents.
- Loads JSON dictionaries with terms, aliases, and canonical index names.
- Finds every occurrence of enabled terms.
- Indexes aliases under one canonical term using `index_as`.
- Supports parent entries, subentries, `See`, and `See also` references.
- Resolves overlapping matches by preferring the most specific match.
- Preserves visible text and run formatting.
- Inserts Word-compatible XE fields.
- Appends a real Word `INDEX` field automatically.
- Adds an `Index` heading before the generated index field.
- Excludes front matter using an explicit TOC boundary or first-chapter fallback.
- Optionally searches table-cell paragraphs with `--include-tables`.
- Produces dry-run coverage reports and JSON reports.
- Saves a new indexed document without modifying the source document.
- Provides a command-line interface.

## Current limitations

Version 0.5.0 searches normal body paragraphs and headings. Table-cell indexing is available with `--include-tables`. It does not yet index text inside:

- Headers and footers.
- Footnotes and endnotes.
- Text boxes and other embedded Word stories.

The current scope is intentionally limited so that the core engine remains predictable and testable.

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
python book_indexer.py index input/sample.docx dictionaries/technology/powershell.json output/sample_indexed.docx
```

The command automatically adds XE fields, an `Index` heading, and a Word `INDEX` field. Open the output in Word and press `Ctrl+A`, then `F9`.

Use `--include-tables` to include table-cell paragraphs:

```powershell
python book_indexer.py index input/sample.docx dictionaries/technology/powershell.json output/sample_with_tables.docx --include-tables
```

Use `--no-index-field` when only XE fields are required.

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
      "parent": "PowerShell",
      "subentry": "Cmdlets",
      "category": "Cmdlet",
      "enabled": true
    },
    {
      "term": "pwsh",
      "index_as": "pwsh",
      "see": "PowerShell",
      "enabled": true
    },
    {
      "term": "PowerShell",
      "index_as": "PowerShell",
      "see_also": ["Windows PowerShell", "PowerShell Core"],
      "enabled": true
    }
  ]
}
```

A `parent` and `subentry` create a hierarchy such as `PowerShell:Cmdlets:Get-ChildItem`. A `see` entry redirects readers to a preferred entry. A `see_also` entry adds a related-topic reference while preserving the entry's normal page references.

## Development

```powershell
python -m pytest -q
```

The project follows a staged workflow: write a focused test, implement one capability, run the full suite, validate a generated DOCX in Word, and commit only after the result is confirmed.

## License

WordIndexer is released under the MIT License. See [LICENSE](LICENSE).
