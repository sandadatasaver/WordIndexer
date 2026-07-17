# Changelog

## 0.5.0 — 2026-07-17

Hierarchical entries and cross-reference release.

### Added

- `parent` and `subentry` dictionary metadata.
- Hierarchical XE fields.
- `See` references.
- `See also` references.
- One-time `See also` insertion per canonical entry.
- Regression tests for dictionary metadata, hierarchy, and cross-reference XML.

### Validated

- The complete regression suite passes with 45 tests.
- Nested index entries display correctly in Microsoft Word.
- `See` references display correctly in Microsoft Word.
- `See also` references preserve normal page references.

## 0.4.0 — 2026-07-16

Optional table-cell indexing release.

### Added

- Ordered traversal of top-level body paragraphs and tables.
- Table-cell paragraph metadata and exact targets.
- `--include-tables` option for `analyze` and `index`.
- Table-cell XE insertion with formatting preservation.
- Body-boundary protection for tables before the manuscript body.

## 0.3.0 — 2026-07-16

Analysis and coverage reports release.

- Dry-run analysis and JSON report export.
- Coverage metrics for boundaries, missing terms, occurrences, and overlaps.

## 0.2.0 — 2026-07-16

Automatic visible INDEX field release.

- Automatic `Index` heading and Word INDEX field.
- `--no-index-field` option.

## 0.1.0 — 2026-07-16

First usable WordIndexer core release.
