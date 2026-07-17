# Analysis and Coverage Reports

WordIndexer can analyze a manuscript without modifying it.

## Console report

```powershell
python book_indexer.py analyze input/sample.docx dictionaries/technology/powershell.json
```

The report includes:

- Total paragraphs.
- Body-start paragraph.
- Ignored paragraphs before the body boundary.
- TOC detection method.
- Active dictionary entries.
- Terms found and missing.
- Total occurrences.
- Overlaps resolved.
- Per-term occurrence counts.

## JSON report

Use `--json-output` to save a machine-readable report:

```powershell
python book_indexer.py analyze `
    input/sample.docx `
    dictionaries/technology/powershell.json `
    --json-output output/sample_analysis.json
```

The JSON report contains the same metrics as the console report and is intended for later GUI, CSV, dashboard, and manuscript-review workflows.

Analysis is read-only. It never inserts fields and never overwrites the source document.

Generated reports under `output/` are excluded from Git by `.gitignore`.
