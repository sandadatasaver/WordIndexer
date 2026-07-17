# WordIndexer Project

**Project:** WordIndexer  
**Owner:** Bishop David Sanda  
**License:** MIT  
**Python:** 3.12+

## Vision

WordIndexer is an open-source engine for creating professional Microsoft Word indexes from customizable dictionaries. It begins with automatic XE-field insertion and is intended to grow into a broader document-intelligence platform for authors, researchers, educators, and publishers.

## Current release

**Version 0.5.0 — Hierarchical Entries and Cross-References**

The core workflow has been validated with automated tests, a torture document, and a real PowerShell manuscript. The tool supports automatic INDEX fields, optional table-cell indexing, hierarchy, `See`, and `See also` references.

## Completed

- Configuration manager and logging foundation.
- CLI with `inspect`, `analyze`, and `index` commands.
- DOCX reader and ordered body/table traversal.
- JSON dictionary loader with aliases, canonical terms, hierarchy, and cross-reference metadata.
- Every-occurrence search and exact run-level scanning.
- Global overlap resolution.
- Word-compatible XML and XE field writers.
- Automatic `Index` heading and INDEX field.
- TOC/body boundary detection with first-chapter fallback.
- Optional table-cell indexing with `--include-tables`.
- Dry-run console and JSON coverage reports.
- Hierarchical XE fields.
- `See` and `See also` XE fields.
- Validation in Microsoft Word with generated page-numbered indexes.

## Version 0.5.0 scope

The current release indexes normal body paragraphs and headings. With `--include-tables`, it also indexes table-cell paragraphs in document order. It excludes content before the detected body boundary and preserves visible text and formatting.

The following remain deferred:

- Headers and footers.
- Footnotes and endnotes.
- Text boxes and other embedded Word stories.
- Glossary and acronym generation.
- AI-assisted suggestions.
- GUI and packaging for end users.

## Validation results

The real PowerShell manuscript produced:

- Paragraph-only mode: 369 occurrences.
- Table-aware mode: 1,138 occurrences.
- Table-aware overlaps resolved: 22.
- All three dictionary terms found.

## Immediate next milestone

Begin additional Word-story support and Version 2 document-intelligence features:

1. Add headers and footers only if the indexing scope requires them.
2. Add footnotes, endnotes, and text boxes through separate tested traversals.
3. Begin glossary and terminology workflows only after the indexing core remains stable.

## Repository branches

- `main` — stable releases.
- `develop` — active development.

## Development rules

- Work on one focused capability at a time.
- Add or update tests with each capability.
- Run the complete suite with `python -m pytest -q`.
- Validate generated documents in Microsoft Word.
- Never commit private manuscripts or generated output documents.
- Keep Version 2 work separate from the stable release.

> Build tools that help people create knowledge.
