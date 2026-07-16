"""
Logging support.
"""

import logging
from pathlib import Path


def setup_logger(log_folder: Path = Path("logs")) -> logging.Logger:

    log_folder.mkdir(exist_ok=True)

    logfile = log_folder / "wordindexer.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(logfile, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger("WordIndexer")