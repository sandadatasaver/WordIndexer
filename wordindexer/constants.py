"""
Application-wide constants.
"""

from pathlib import Path

APP_NAME = "WordIndexer"

CONFIG_FILE = "config.json"

DEFAULT_DICTIONARY_FOLDER = Path("dictionaries")

INPUT_FOLDER = Path("input")

OUTPUT_FOLDER = Path("output")

LOG_FOLDER = Path("logs")

SUPPORTED_EXTENSIONS = [".docx"]