from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True)
class Paragraph:
    """Represents one paragraph in the document."""

    index: int
    text: str
    style: str = ""
    section: int = 0
    page: Optional[int] = None


@dataclass(slots=True)
class Heading:
    """Represents a document heading."""

    level: int
    text: str
    paragraph_index: int


@dataclass(slots=True)
class Match:
    """Represents one indexed occurrence."""

    term: str
    paragraph_index: int
    paragraph_text: str


@dataclass(slots=True)
class DictionaryEntry:
    """Represents one dictionary entry."""

    term: str
    aliases: List[str] = field(default_factory=list)
    category: str = ""
    enabled: bool = True


@dataclass(slots=True)
class Book:
    """Internal representation of the document."""

    title: str = ""
    author: str = ""

    paragraphs: List[Paragraph] = field(default_factory=list)
    headings: List[Heading] = field(default_factory=list)

    matches: List[Match] = field(default_factory=list)