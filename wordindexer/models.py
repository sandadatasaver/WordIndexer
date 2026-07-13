"""
Domain models used throughout WordIndexer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True)
class Paragraph:
    index: int
    text: str
    style: str = ""
    section: int = 0
    page: Optional[int] = None


@dataclass(slots=True)
class Heading:
    level: int
    text: str
    paragraph_index: int


@dataclass(slots=True)
class DictionaryEntry:
    term: str
    aliases: List[str] = field(default_factory=list)
    category: str = ""
    enabled: bool = True
    index_as: str = ""


@dataclass(slots=True)
class RunLocation:
    """
    Exact location of text inside a paragraph.
    """

    paragraph_index: int
    run_index: int
    start: int
    end: int
    matched_text: str


@dataclass(slots=True)
class Match:
    term: str
    matched_text: str
    paragraph_index: int
    paragraph_text: str

    paragraph_style: str = ""
    page: Optional[int] = None
    section: int = 0
    heading: str = ""

    locations: List[RunLocation] = field(default_factory=list)


@dataclass(slots=True)
class Book:
    title: str = ""
    author: str = ""

    paragraphs: List[Paragraph] = field(default_factory=list)
    headings: List[Heading] = field(default_factory=list)

    matches: List[Match] = field(default_factory=list)
    term_matches: dict[str, List[Match]] = field(default_factory=dict)