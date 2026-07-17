# Changelog

## 0.4.0 — 2026-07-16

Optional table-cell indexing release.

### Added

- Ordered traversal of top-level body paragraphs and tables.
- Table-cell paragraph metadata and exact targets.
- `--include-tables` option for `analyze` and `index`.
- Table-cell XE insertion with formatting preservation.
- Body-boundary protection for tables before the manuscript body.
- Regression tests for table traversal, reports, indexing, and boundary handling.

### Validated

- The complete regression suite passes.
- The real PowerShell manuscript produced 1,138 table-aware occurrences.
- Word generated a valid page-numbered index from the table-aware output.

### Remaining limitations

- Headers, footers, footnotes, endnotes, and text boxes remain unsupported.

## 0.3.0 — 2026-07-16

Analysis and coverage reports release.

### Added

- Dry-run analysis and coverage reports.
- JSON report export through `analyze --json-output`.
- Report metrics for body boundaries, ignored paragraphs, missing terms, occurrences, and overlaps resolved.
- Ignore rules for generated JSON, CSV, TXT, and HTML files under `output/`.

## 0.2.0 — 2026-07-16

Automatic visible INDEX field release.

### Added

- Automatic `Index` heading insertion.
- Automatic Word `INDEX` field insertion.
- `--no-index-field` CLI option for XE-only output.
- Documentation for updating the generated index with `Ctrl+A`, then `F9`.

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
