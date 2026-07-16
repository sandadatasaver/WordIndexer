# Changelog

## 0.1.0 — 2026-07-16

First usable WordIndexer core release.

### Added

- DOCX inspection and analysis commands.
- JSON dictionary loading with aliases and canonical `index_as` terms.
- Every-occurrence search.
- Exact run-level scanning, including terms split across formatted runs.
- Global overlap resolution.
- Generic WordprocessingML complex-field writer.
- Microsoft Word-compatible XE writer.
- Explicit TOC detection and first-chapter fallback.
- End-to-end indexing command that saves a new DOCX.
- Regression tests for sample, torture, and real-book workflows.

### Validated

- Generated documents open in Microsoft Word without repair warnings.
- Word recognizes the XE fields and creates an index with page numbers.
- The source document remains unchanged.

### Known limitations

- Table cells, headers, footers, footnotes, endnotes, and text boxes are not searched in this release.
- The visible INDEX field is added through Microsoft Word after generation.
