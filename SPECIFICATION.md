# WordIndexer Specification

## Purpose

WordIndexer creates Microsoft Word indexes by inserting native XE fields into `.docx` documents. It also appends a visible Word INDEX field so Microsoft Word can populate the index after a field update. The source document is preserved and a new indexed document is written to the requested output path.

## Version 0.5.0 objectives

- Load a DOCX document.
- Load a JSON dictionary.
- Search every occurrence of enabled terms and aliases.
- Map aliases to canonical `index_as` values.
- Support `parent` and `subentry` hierarchy metadata.
- Support `See` and `See also` references.
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

## Supported input

- Microsoft Word `.docx` files.

## Supported output

- Microsoft Word `.docx` files containing XE fields and, by default, a Word INDEX field.
- The INDEX field is populated in Word with `Ctrl+A`, followed by `F9`.

## Dictionary format

Entries may contain:

- `term` — primary search term.
- `aliases` — alternative forms.
- `index_as` — canonical text written into the XE field.
- `parent` — top-level hierarchy component.
- `subentry` — second-level hierarchy component.
- `see` — redirect to a preferred entry.
- `see_also` — related entries.
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

Version 0.5.0 does not search:

- Headers and footers.
- Footnotes or endnotes.
- Text boxes and other embedded Word stories.

Table cells are excluded by default and included only with `--include-tables`.

## Deferred features

- Additional Word-story traversal.
- Glossary generation.
- Acronym generation.
- Figure and table indexes.
- Citation analysis.
- AI-assisted suggestions.
- GUI and installer.
