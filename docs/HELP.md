# WordIndexer Quick Help

## Basic workflow

1. Browse for a Word manuscript (`.docx`).
2. Select a reviewed dictionary (`.json`).
3. Choose an output folder.
4. Select **Generate Index**, **Generate Glossary**, or both.
5. Select **Include table cells** when table content should be indexed.
6. Enter a Heading 1 section under **Remove section** when editorial material should be removed from the final copy.
7. Click **Run**.
8. Open the generated DOCX in Microsoft Word and press `Ctrl+A`, then `F9`.
9. Save the updated Word document.

## Dictionary workflow

Use **Generate Dictionary Draft** to discover candidate terms. Review the generated CSV in Excel, set approved entries to `TRUE`, add definitions/categories/aliases as needed, and finalize the reviewed CSV into a production dictionary.

## Output

WordIndexer never overwrites the source manuscript. Generated DOCX files, JSON reports, CSV review files, and glossary reports are written to the selected output folder.

## CLI equivalent

```powershell
python book_indexer.py index manuscript.docx dictionary.json output.docx
python book_indexer.py analyze manuscript.docx dictionary.json
python book_indexer.py glossary-docx manuscript.docx dictionary.json output_glossary.docx
```
