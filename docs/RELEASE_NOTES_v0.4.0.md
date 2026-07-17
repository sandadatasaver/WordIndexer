# WordIndexer 0.4.0

## Optional Table-Cell Indexing

WordIndexer 0.4.0 adds controlled table-cell traversal.

Use the option explicitly:

```powershell
python book_indexer.py index input/sample.docx dictionaries/technology/powershell.json output/sample_with_tables.docx --include-tables
```

The feature:

- Traverses top-level paragraphs and tables in document order.
- Preserves the body boundary when tables occur before the manuscript body.
- Searches table-cell paragraphs.
- Inserts XE fields inside table cells.
- Keeps paragraph-only behavior as the default.

## Validation

The table-aware workflow was validated with the real PowerShell manuscript:

```text
Body starts       : 147
Terms found       : 3
Terms missing     : 0
Total occurrences : 1138
Overlaps resolved : 22
XE fields         : 1138
```

## Remaining scope

Headers, footers, footnotes, endnotes, text boxes, and other embedded Word stories remain future work.
