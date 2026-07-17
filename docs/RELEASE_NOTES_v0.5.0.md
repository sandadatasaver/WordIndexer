# WordIndexer 0.5.0

## Hierarchical Entries and Cross-References

WordIndexer 0.5.0 adds professional index relationships:

- Parent entries.
- Subentries.
- `See` references.
- `See also` references.

Example hierarchy:

```json
{
  "term": "Get-ChildItem",
  "index_as": "Get-ChildItem",
  "parent": "PowerShell",
  "subentry": "Cmdlets"
}
```

This produces:

```text
PowerShell
    Cmdlets
        Get-ChildItem
```

A `See` entry redirects the reader:

```json
{
  "term": "pwsh",
  "index_as": "pwsh",
  "see": "PowerShell"
}
```

A `See also` entry preserves normal page references and adds a related-topic reference:

```json
{
  "term": "PowerShell",
  "index_as": "PowerShell",
  "see_also": ["Windows PowerShell", "PowerShell Core"]
}
```

## Validation

This release was validated with:

- 45 automated tests.
- Nested index entries in Microsoft Word.
- `See` references in Microsoft Word.
- `See also` references in Microsoft Word.

Table-cell indexing remains available through `--include-tables`.
