# Word XML Design

## Field representation

Microsoft Word creates an XE field as a complex field with a begin character, one or more `w:instrText` elements, and an end character. A typical entry is represented as:

```xml
<w:r>
  <w:fldChar w:fldCharType="begin"/>
</w:r>
<w:r>
  <w:instrText xml:space="preserve"> XE "</w:instrText>
</w:r>
<w:r>
  <w:instrText>PowerShell</w:instrText>
</w:r>
<w:r>
  <w:instrText xml:space="preserve">" </w:instrText>
</w:r>
<w:r>
  <w:fldChar w:fldCharType="end"/>
</w:r>
```

Word places the XE field immediately after the marked text. Word also formats the field as hidden through its field behavior; the writer does not add a custom `w:vanish` property to the field runs.

## Insertion strategy

1. Search and resolve matches before modifying the document.
2. Locate the final run fragment of each match.
3. Insert the field at that fragment's end offset.
4. Split a run when the insertion occurs in the middle of visible text.
5. Copy the original run properties to the visible before/after fragments.
6. Process matches in reverse document order.
7. Save to a new DOCX path.

## Safety requirements

- Do not edit `word/document.xml` as a text file.
- Use `OxmlElement`, `qn`, and the underlying run elements exposed by `python-docx`.
- Keep the input document unchanged.
- Reopen the generated DOCX in tests.
- Inspect the resulting `w:instrText` and `w:fldChar` elements.
- Validate the generated output in Microsoft Word.

## XE syntax

Version 0.1.0 writes a canonical primary entry:

```text
XE "PowerShell"
```

Quotation marks, backslashes, colons, and semicolons are escaped before they are written. Nested subentries and sort overrides are deferred until the dictionary model explicitly supports them.
