#!/usr/bin/env python3

"""
WordIndexer
"""

from __future__ import annotations

import argparse

from wordindexer.config import ConfigManager
from wordindexer.dictionary import DictionaryLoader
from wordindexer.document import DocumentReader
from wordindexer.index import IndexEngine
from wordindexer.logger import setup_logger
from wordindexer.reports import ReportBuilder
from wordindexer.version import VERSION


logger = setup_logger()


def cmd_inspect(args):

    reader = DocumentReader(args.document)

    info = reader.inspect()

    print()
    print("Document Information")
    print("--------------------")
    print(f"Title       : {info.title}")
    print(f"Author      : {info.author}")
    print(f"Subject     : {info.subject}")

    print()
    print("Statistics")
    print("----------")
    print(f"Paragraphs  : {info.paragraphs}")
    print(f"Tables      : {info.tables}")
    print(f"Images      : {info.images}")
    print()


def cmd_analyze(args):

    loader = DictionaryLoader(args.dictionary)
    entries = loader.load_entries()
    report = ReportBuilder().build(args.document, entries)

    print(report.render_console())

    if args.json_output:
        report_path = report.write_json(args.json_output)
        print()
        print(f"JSON report       : {report_path}")


def cmd_index(args):

    loader = DictionaryLoader(args.dictionary)
    entries = loader.load_entries()

    result = IndexEngine(
        include_index_field=not args.no_index_field,
    ).index(
        input_path=args.document,
        dictionary=entries,
        output_path=args.output,
    )

    print()
    print("Indexing Complete")
    print("-----------------")
    print(f"TOC detected  : {result.toc_detected}")
    print(f"TOC method    : {result.toc_method}")
    print(f"Body starts   : {result.body_start}")
    print(f"Terms found   : {result.terms_found}")
    print(f"Terms missing : {result.terms_not_found}")
    print(f"Occurrences   : {result.occurrences}")
    print(f"XE fields    : {result.fields_inserted}")
    print(f"INDEX field  : {result.index_field_inserted}")
    print(f"Output        : {result.output_path}")
    print()


def build_parser():

    parser = argparse.ArgumentParser(
        prog="book_indexer.py",
        description="Automatic Microsoft Word Index Generator",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"WordIndexer {VERSION}",
    )

    sub = parser.add_subparsers(dest="command")

    inspect_parser = sub.add_parser(
        "inspect",
        help="Inspect a document",
    )

    inspect_parser.add_argument("document")

    inspect_parser.set_defaults(func=cmd_inspect)

    analyze_parser = sub.add_parser(
        "analyze",
        help="Analyze a document",
    )

    analyze_parser.add_argument("document")

    analyze_parser.add_argument("dictionary")

    analyze_parser.add_argument(
        "--json-output",
        help="Write the analysis report as JSON",
    )

    analyze_parser.set_defaults(func=cmd_analyze)

    index_parser = sub.add_parser(
        "index",
        help="Insert index entries",
    )

    index_parser.add_argument("document")

    index_parser.add_argument("dictionary")

    index_parser.add_argument("output")

    index_parser.add_argument(
        "--no-index-field",
        action="store_true",
        help="Do not append a visible Word INDEX field",
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