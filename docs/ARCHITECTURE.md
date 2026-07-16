# WordIndexer Architecture

## Pipeline

```text
CLI
 │
 ▼
DocumentReader
 │
 ▼
Book model
 │
 ▼
TOC/body boundary
 │
 ▼
DictionaryLoader
 │
 ▼
SearchEngine
 │
 ▼
RunScanner
 │
 ▼
MatchResolver
 │
 ▼
XMLWriter
 │
 ▼
XEWriter
 │
 ▼
Indexed DOCX
```

## Responsibilities

### `DocumentReader`

Opens the DOCX with `python-docx`, exposes document properties, and creates the internal `Book` representation.

### `DictionaryLoader`

Loads JSON dictionaries and converts entries into typed `DictionaryEntry` objects.

### `SearchEngine`

Searches enabled terms and aliases, preserves the matched text, attaches context, and records exact run locations when a source document is supplied.

### `RunScanner`

Maps matches in combined paragraph text back to the individual Word runs. It supports a match split across multiple runs with different formatting.

### `MatchResolver`

Removes overlapping candidates globally. The longest valid match wins, with deterministic document-order output.

### `XMLWriter`

Performs low-level WordprocessingML run splitting and complex-field insertion while preserving the visible text and run properties around the insertion point.

### `XEWriter`

Builds the Word-compatible XE instruction structure and delegates XML manipulation to `XMLWriter`.

### `IndexEngine`

Coordinates document loading, body-boundary detection, searching, reverse-order XE insertion, and output saving.

## Important invariants

- The input document is never overwritten.
- Visible manuscript text must remain unchanged.
- Field insertion is performed from later locations to earlier locations so original run indexes remain valid.
- Canonical dictionary terms, not aliases, are written into XE fields.
- Every major behavior has a regression test.

## Current scope

Version 0.1.0 searches normal body paragraphs and headings. Table cells, headers, footers, footnotes, endnotes, and text boxes are intentionally excluded until they have their own traversal and regression tests.
