#!/usr/bin/env python3

"""
WordIndexer
"""

from __future__ import annotations

import argparse

from wordindexer.version import VERSION
from wordindexer.logger import setup_logger
from wordindexer.config import ConfigManager


logger = setup_logger()


def cmd_inspect(args):
    logger.info("Inspect command selected.")
    print(f"Document : {args.document}")


def cmd_index(args):
    logger.info("Index command selected.")
    print(f"Indexing : {args.document}")


def build_parser():

    parser = argparse.ArgumentParser(
        prog="book_indexer.py",
        description="Automatic Microsoft Word Index Generator"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"WordIndexer {VERSION}"
    )

    sub = parser.add_subparsers(dest="command")

    inspect_parser = sub.add_parser(
        "inspect",
        help="Inspect a document"
    )

    inspect_parser.add_argument(
        "document"
    )

    inspect_parser.set_defaults(func=cmd_inspect)

    index_parser = sub.add_parser(
        "index",
        help="Insert index entries"
    )

    index_parser.add_argument(
        "document"
    )

    index_parser.set_defaults(func=cmd_index)

    return parser


def main():

    ConfigManager().load()

    parser = build_parser()

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()