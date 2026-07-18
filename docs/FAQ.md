# WordIndexer FAQ

## Why does the window say it is working?

Large DOCX files and documents containing many tables can take time to scan and save. WordIndexer runs these tasks in the background so the GUI remains responsive. The progress bar is indeterminate because the underlying document libraries do not yet provide exact percentage progress.

## Why do I need to press Ctrl+A and F9?

WordIndexer inserts XE and INDEX fields. Microsoft Word calculates page numbers and populates the visible index when fields are updated.

## Why is my Table of Contents not detected by name?

Some Word TOCs are stored as fields, images, or embedded structures that are not exposed as ordinary paragraph text. WordIndexer uses a first-chapter fallback when it finds a Heading 1 beginning with Chapter 1.

## How do I index table content?

Enable **Include table cells** in the GUI or pass `--include-tables` on the CLI.

## Why is a glossary entry missing?

Only dictionary entries with a `definition` are included in the glossary. Add a definition in the reviewed CSV, finalize the dictionary, and generate the glossary again.

## Why are discovered terms disabled?

Discovery produces candidates for human review. Set `enabled` to `TRUE` in the CSV only after deciding that a term belongs in the index.

## What does See mean?

`See` redirects a reader from one entry to a preferred entry without normal page references.

## What does See also mean?

`See also` points to a related entry while preserving the normal page references for the current entry.

## Is my original manuscript changed?

No. WordIndexer always writes a new output document.

## What should not be committed to Git?

Do not commit private manuscripts, generated DOCX files, output reports, temporary ZIP files, virtual environments, or Python caches.
