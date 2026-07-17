# WordIndexer Specification

## Purpose

WordIndexer creates Microsoft Word indexes by inserting native XE (Index Entry) fields into `.docx` documents. It also appends a visible Word INDEX field so Microsoft Word can populate the index after a field update. The source document is preserved and a new indexed document is written to the requested output path.

## Version 0.2.0 objectives

- Load a DOCX document.
- Load a JSON dictionary.
- Search every occurrence of enabled terms and aliases.
- Map aliases to canonical `index_as` values.
- Exclude content before the detected manuscript body.
- Resolve overlapping matches.
- Preserve visible text and run formatting.
- Insert Word-compatible XE fields.
- Append an `Index` heading and INDEX field by default.
- Allow the INDEX field to be disabled with `--no-index-field`.
- Produce read-only console coverage reports.
- Export analysis reports as JSON when requested.
- Optionally traverse table-cell paragraphs in document order.
- Insert XE fields inside table-cell paragraphs when `--include-tables` is enabled.
- Save a new DOCX document.
- Support inspection, analysis, and indexing through the CLI.
- Produce read-only console coverage reports.
- Export analysis reports as JSON when requested.

## Supported input

- Microsoft Word `.docx` files.

## Supported output

- Microsoft Word `.docx` files containing XE fields and, by default, a Word INDEX field.
- The INDEX field is populated in Word with `Ctrl+A`, followed by `F9`.

## Dictionary format

A dictionary contains:

- `metadata` — name, version, author, and optional description.
- `entries` — searchable entries.
- `term` — primary search term.
- `aliases` — alternative forms.
- `index_as` — canonical text written into the XE field.
- `category` — optional classification.
- `enabled` — whether the entry is active.

## Matching rules

- Matching is case-insensitive.
- Matching is whole-word by default.
- Every occurrence is captured.
- Aliases are indexed under the canonical term.
- Overlapping matches prefer the longer, more specific occurrence.
- Matches split across formatted runs are supported.

## Document boundary rules

The detector tries, in order:

1. An explicit `Table of Contents` or `Contents` heading.
2. A first `Heading 1` beginning with `Chapter 1`.
3. The beginning of the document if no safe boundary is found.

## Current exclusions

Version 0.2.0 does not search:

- Table cells.
- Headers or footers.
- Footnotes or endnotes.
- Text boxes and other embedded Word stories.

## Deferred features

- Headers, footers, and additional Word-story traversal.
- Nested subentries and cross references.
- Further report formats and review workflows.
- Glossary generation.
- Acronym generation.
- Figure and table indexes.
- Citation analysis.
- AI-assisted suggestions.
- GUI and installer.
