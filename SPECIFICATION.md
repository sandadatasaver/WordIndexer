# WordIndexer Specification

## Purpose

WordIndexer creates Microsoft Word indexes by inserting native XE (Index Entry) fields into `.docx` documents. The source document is preserved and a new indexed document is written to the requested output path.

## Version 0.1.0 objectives

- Load a DOCX document.
- Load a JSON dictionary.
- Search every occurrence of enabled terms and aliases.
- Map aliases to canonical `index_as` values.
- Exclude content before the detected manuscript body.
- Resolve overlapping matches.
- Preserve visible text and run formatting.
- Insert Word-compatible XE fields.
- Save a new DOCX document.
- Support inspection, analysis, and indexing through the CLI.

## Supported input

- Microsoft Word `.docx` files.

## Supported output

- Microsoft Word `.docx` files containing XE fields.
- The visible index is created in Word with **References → Insert Index**.

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

Version 0.1.0 does not search:

- Table cells.
- Headers or footers.
- Footnotes or endnotes.
- Text boxes and other embedded Word stories.

## Deferred features

- Automatic visible INDEX-field insertion.
- Nested subentries and cross references.
- Glossary generation.
- Acronym generation.
- Figure and table indexes.
- Citation analysis.
- AI-assisted suggestions.
- GUI and installer.
