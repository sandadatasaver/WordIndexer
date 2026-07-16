"""
Custom exceptions used throughout WordIndexer.
"""


class WordIndexerError(Exception):
    """Base exception."""


class ConfigurationError(WordIndexerError):
    """Configuration error."""


class DictionaryError(WordIndexerError):
    """Dictionary error."""


class DocumentError(WordIndexerError):
    """Document error."""


class TOCNotFoundError(DocumentError):
    """Table of Contents not found."""


class IndexInsertionError(DocumentError):
    """Failed inserting XE fields."""