# WordIndexer Project

**Project:** WordIndexer  
**Owner:** Bishop David Sanda  
**License:** MIT  
**Python:** 3.12+

## Vision

WordIndexer is an open-source engine for creating professional Microsoft Word indexes from customizable dictionaries. It begins with automatic XE-field insertion and is intended to grow into a broader document-intelligence platform for authors, researchers, educators, and publishers.

## Current release

**Version 0.1.0 — First Usable Core**

The core indexing workflow has been validated with automated tests, a torture document, and a real PowerShell manuscript.

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
- Validation in Microsoft Word with generated page-numbered indexes.

## Version 0.1.0 scope

The current release indexes normal body paragraphs and headings. It excludes content before the detected body boundary and preserves the original visible text and formatting.

The following are deliberately deferred:

- Table-cell indexing.
- Headers and footers.
- Footnotes and endnotes.
- Text boxes and other embedded stories.
- Automatic visible INDEX-field insertion.
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

Release hardening:

1. Keep the current paragraph-based scope explicit in documentation.
2. Maintain the regression suite for the sample, torture, and real-book workflows.
3. Publish the first stable core release.
4. Add table and additional Word-story support only as a separately tested milestone.

## Repository branches

- `main` — stable releases.
- `develop` — active development.

## Development rules

- Work on one focused capability at a time.
- Add or update tests with each capability.
- Run the complete suite with `python -m pytest -q`.
- Validate generated documents in Microsoft Word.
- Never commit private manuscripts or generated output documents.
- Keep Version 1 focused before adding Version 2 features.

> Build tools that help people create knowledge.
