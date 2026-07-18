# Windows Packaging

WordIndexer is packaged in two stages:

1. PyInstaller bundles Python, the WordIndexer engine, PySide6, and application data.
2. Inno Setup creates the user-facing Windows installer.

## Build the executable

From the project root in PowerShell:

```powershell
.\packaging\build_windows.ps1
```

The expected executable is:

```text
dist\WordIndexer\WordIndexer.exe
```

This executable launches the GUI directly. The CLI remains available from the source checkout with `python book_indexer.py ...`.

Test that executable before creating the installer.

## Build the installer

Open this file in Inno Setup Compiler:

```text
installer\WordIndexer.iss
```

Click **Compile**. The installer will be written to:

```text
installer-output\WordIndexer-Setup-0.5.0.exe
```

## Release checklist

- Run `python -m pytest -q`.
- Test the GUI from source.
- Run the PyInstaller build.
- Launch `dist\WordIndexer\WordIndexer.exe`.
- Test browsing, analysis, indexing, glossary generation, table support, and section cleanup.
- Compile the Inno Setup installer.
- Install into a clean Windows user profile.
- Test the installed application.
- Update the version in `installer\WordIndexer.iss` before each release.
