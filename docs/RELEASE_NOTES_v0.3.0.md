# WordIndexer 0.3.0

## Analysis and Coverage Reports

WordIndexer 0.3.0 adds a read-only analysis workflow for reviewing dictionary coverage before modifying a manuscript.

Run a console report:

```powershell
python book_indexer.py analyze input/sample.docx dictionaries/technology/powershell.json
```

Save a JSON report:

```powershell
python book_indexer.py analyze `
    input/sample.docx `
    dictionaries/technology/powershell.json `
    --json-output output/sample_analysis.json
```

Reports include:

- Document paragraph count.
- Body-start boundary.
- Ignored paragraphs.
- TOC detection method.
- Dictionary coverage.
- Missing terms.
- Total occurrences.
- Overlaps resolved.
- Per-term occurrence counts.

Analysis is read-only and does not modify the source document.

## Validation

The report workflow was validated against the real PowerShell manuscript:

```text
Paragraphs        : 2867
Body starts       : 107
Ignored paragraphs: 107
Terms found       : 3
Terms missing     : 0
Total occurrences : 369
Overlaps resolved : 12
```

## Scope note

This release continues to index normal body paragraphs and headings. Tables, headers, footers, footnotes, endnotes, and text boxes remain planned future work.
