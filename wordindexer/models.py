"""
WordIndexer Data Models

Author: Bishop David Sanda
License: MIT
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True)
class IndexEntry:
    """
    Represents one index term.
    """

    term: str

    aliases: List[str] = field(default_factory=list)

    category: Optional[str] = None

    parent: Optional[str] = None

    whole_word: bool = True

    case_sensitive: bool = False

    first_only: bool = True

    enabled: bool = True

    found: bool = False

    paragraph: Optional[int] = None

    character: Optional[int] = None

    matched_text: Optional[str] = None


@dataclass(slots=True)
class DictionaryMetadata:

    name: str

    version: str

    author: str = ""

    description: str = ""


@dataclass(slots=True)
class SearchResult:

    entry: IndexEntry

    paragraph_number: int

    character_position: int

    matched_text: str