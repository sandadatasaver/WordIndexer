# WordIndexer Project

**Project:** WordIndexer  
**Owner:** Bishop David Sanda  
**License:** MIT  
**Python:** 3.12+

## Vision

WordIndexer is an open-source engine for creating professional Microsoft Word indexes from customizable dictionaries. It begins with automatic XE-field insertion and is intended to grow into a broader document-intelligence platform for authors, researchers, educators, and publishers.

## Current release

**Version 0.2.0 — Automatic Index Field**

The core indexing workflow has been validated with automated tests, a torture document, and a real PowerShell manuscript. The command now adds a visible Word INDEX field and an `Index` heading automatically.

## Completed

- Configuration manager and logging foundation.
- Command-line interface with `inspect`, `analyze`, and `index` commands.
- DOCX document reader.
- JSON dictionary loader with aliases and canonical terms.
- Search engine that captures every occurrence.
- Exact run-level scanning, including terms split across formatted runs.
- Global overlap resolution.
- Word-compatible generic XML field writer.
- XE writer using the Word-generated instruction structure.
- TOC/body boundary detection with first-chapter fallback.
- End-to-end DOCX indexing and save/reopen tests.
- Automatic Word INDEX field insertion.
- Automatic `Index` heading insertion.
- Validation in Microsoft Word with generated page-numbered indexes.

## Version 0.2.0 scope

The current release indexes normal body paragraphs and headings. It excludes content before the detected body boundary and preserves the original visible text and formatting. It appends a Word INDEX field by default; `--no-index-field` disables that behavior.

The following are deliberately deferred:

- Table-cell indexing.
- Headers and footers.
- Footnotes and endnotes.
- Text boxes and other embedded stories.
- Nested indexes and cross references.
- Glossary and acronym generation.
- AI-assisted suggestions.
- GUI and packaging for end users.

## Current limitations

Some Word documents store their TOC as a field, image, or embedded structure that `python-docx` does not expose as ordinary paragraph text. WordIndexer therefore uses a detection cascade:

1. Explicit `Table of Contents` or `Contents` heading.
2. First `Heading 1` beginning with `Chapter 1`, when no explicit TOC text is available.
3. Whole-document fallback when no safe boundary is found.

The selected method is reported by the indexing command.

## Immediate next milestone

Begin Version 2 planning and document traversal hardening:

1. Decide how to support table cells and additional Word stories.
2. Add a dry-run and coverage report.
3. Add nested entries and cross references.
4. Begin glossary and terminology workflows only after the indexing core remains stable.

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
