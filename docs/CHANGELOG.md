# Changelog

## 0.2.0 — 2026-07-16

Automatic visible INDEX field release.

### Added

- Automatic `Index` heading insertion.
- Automatic Word `INDEX` field insertion.
- `--no-index-field` CLI option for XE-only output.
- Documentation for updating the generated index with `Ctrl+A`, then `F9`.

### Validated

- The complete regression suite passes.
- Generated documents open in Microsoft Word without repair warnings.
- Word recognizes the XE fields and creates page-numbered indexes.
- The visible INDEX field is populated by updating fields in Word.
- The source document remains unchanged.

### Known limitations

- Table cells, headers, footers, footnotes, endnotes, and text boxes are not searched in this release.

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
