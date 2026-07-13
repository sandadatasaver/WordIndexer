# WordIndexer Project

**Project Name:** WordIndexer

**Repository:** WordIndexer

**License:** MIT

**Project Owner:** Bishop David Sanda

---

# Vision

WordIndexer is an open-source Python application that automatically creates professional Microsoft Word indexes by inserting native Word XE (Index Entry) fields into `.docx` documents.

The goal is to provide authors, publishers, researchers, students, churches, and technical writers with a free, powerful, and extensible indexing tool.

Unlike existing solutions, WordIndexer will use customizable JSON dictionaries, intelligent matching, alias support, and nested index entries to generate publication-quality indexes.

---
# Mission

To become the world's leading open-source manuscript analysis and indexing platform for Microsoft Word documents.
---
# Project Objectives

* Read Microsoft Word (.docx) documents.
* Detect and skip the Table of Contents.
* Load one or more indexing dictionaries.
* Locate the first occurrence of each term.
* Insert native Microsoft Word XE fields.
* Generate a complete Word index.
* Produce CSV, JSON, and log reports.
* Support multiple subject dictionaries.
* Support aliases, subentries, and cross references.
* Provide both a command-line interface and, later, a graphical user interface.

---

# Current Status

## Phase

Project Initialization

## Current Milestone

Project structure completed.

Next milestone is the implementation of the application core.

---

# Completed

* Repository created.
* MIT License added.
* Initial project structure created.
* Virtual environment configured.
* Initial documentation created.
* Dictionary folder created.
* Example folder created.
* Test folder created.
* Output folder created.

---

# Next Tasks

1. Build the application core.
2. Implement configuration management.
3. Implement logging.
4. Implement command-line interface.
5. Implement dictionary loader.
6. Implement document reader.
7. Implement TOC detection.
8. Implement search engine.
9. Implement Word XML writer.
10. Produce first working prototype.

---

# Future Features

* Automatic dictionary builder.
* Dictionary editor.
* Nested indexes.
* "See" and "See also" references.
* Automatic glossary generation.
* Acronym generator.
* Figure index generation.
* Table index generation.
* Plugin architecture.
* GUI application.
* Windows installer.
* Cross-platform support.
* PyPI package.

---

# Coding Standards

* Python 3.12+
* Type hints throughout.
* Dataclasses where appropriate.
* Logging instead of print().
* Unit tests for all major modules.
* Modular architecture.
* Clear documentation.
* MIT License compatible dependencies only.

---

# Repository Branches

**main**

Stable releases only.

**develop**

Active development.

---

# Success Criteria

Version 1.0 will be considered complete when a user can:

1. Supply a Microsoft Word document.
2. Supply one or more JSON dictionaries.
3. Automatically insert Word XE fields.
4. Update the index in Microsoft Word.
5. Receive a professionally formatted back-of-book index.

---

*"Build tools that help people create knowledge."*
