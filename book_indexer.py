#!/usr/bin/env python3

"""
WordIndexer
"""

from __future__ import annotations

import argparse

from wordindexer.config import ConfigManager
from wordindexer.dictionary import DictionaryLoader
from wordindexer.dictionary_builder import DictionaryDraftBuilder
from wordindexer.document import DocumentReader
from wordindexer.discovery import TermDiscovery
from wordindexer.glossary import GlossaryBuilder
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
    report = ReportBuilder().build(
        args.document,
        entries,
        include_tables=args.include_tables,
    )

    print(report.render_console())

    if args.json_output:
        report_path = report.write_json(args.json_output)
        print()
        print(f"JSON report       : {report_path}")


def cmd_build_dictionary(args):

    output = DictionaryDraftBuilder().build(
        args.discovery,
        args.output,
        name=args.name,
        version=args.dictionary_version,
        author=args.author,
        enable_candidates=args.enable_candidates,
        csv_output=args.csv_output,
    )

    print(f"Dictionary draft : {output}")
    print(f"Candidates enabled: {args.enable_candidates}")

    if args.csv_output:
        print(f"CSV review file  : {args.csv_output}")


def cmd_discover(args):

    entries = []

    if args.dictionary:
        loader = DictionaryLoader(args.dictionary)
        entries = loader.load_entries()

    report = TermDiscovery(
        minimum_occurrences=args.minimum_occurrences,
    ).discover(
        args.document,
        entries,
        include_tables=args.include_tables,
    )

    output = report.write_json(args.output)
    print(f"Candidates       : {len(report.candidates)}")
    print(f"JSON report      : {output}")


def cmd_glossary(args):

    loader = DictionaryLoader(args.dictionary)
    entries = loader.load_entries()
    report = GlossaryBuilder().build(
        args.document,
        entries,
        include_tables=args.include_tables,
    )

    json_path = report.write_json(args.output)
    print(f"Glossary entries : {len(report.entries)}")
    print(f"JSON report      : {json_path}")

    if args.csv_output:
        csv_path = report.write_csv(args.csv_output)
        print(f"CSV report       : {csv_path}")


def cmd_index(args):

    loader = DictionaryLoader(args.dictionary)
    entries = loader.load_entries()

    result = IndexEngine(
        include_index_field=not args.no_index_field,
        include_tables=args.include_tables,
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

    analyze_parser.add_argument(
        "--include-tables",
        action="store_true",
        help="Include table-cell paragraphs in analysis",
    )

    analyze_parser.set_defaults(func=cmd_analyze)

    build_parser = sub.add_parser(
        "build-dictionary",
        help="Build a dictionary draft from discovery candidates",
    )
    build_parser.add_argument("discovery")
    build_parser.add_argument("output")
    build_parser.add_argument(
        "--name",
        default="Generated Dictionary Draft",
    )
    build_parser.add_argument(
        "--version",
        dest="dictionary_version",
        default="0.1",
    )
    build_parser.add_argument(
        "--author",
        default="WordIndexer",
    )
    build_parser.add_argument(
        "--enable-candidates",
        action="store_true",
        help="Enable all candidates without manual review",
    )
    build_parser.add_argument(
        "--csv-output",
        help="Also write a review CSV",
    )
    build_parser.set_defaults(func=cmd_build_dictionary)

    discover_parser = sub.add_parser(
        "discover",
        help="Discover candidate terms for review",
    )
    discover_parser.add_argument("document")
    discover_parser.add_argument("output")
    discover_parser.add_argument(
        "--dictionary",
        help="Existing dictionary whose terms should be excluded",
    )
    discover_parser.add_argument(
        "--minimum-occurrences",
        type=int,
        default=2,
        help="Minimum occurrences required for a candidate",
    )
    discover_parser.add_argument(
        "--include-tables",
        action="store_true",
        help="Include table-cell paragraphs",
    )
    discover_parser.set_defaults(func=cmd_discover)

    glossary_parser = sub.add_parser(
        "glossary",
        help="Generate a glossary report",
    )

    glossary_parser.add_argument("document")
    glossary_parser.add_argument("dictionary")
    glossary_parser.add_argument("output")
    glossary_parser.add_argument(
        "--csv-output",
        help="Also write the glossary as CSV",
    )
    glossary_parser.add_argument(
        "--include-tables",
        action="store_true",
        help="Include table-cell paragraphs in glossary analysis",
    )
    glossary_parser.set_defaults(func=cmd_glossary)

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

    index_parser.add_argument(
        "--include-tables",
        action="store_true",
        help="Include table-cell paragraphs in indexing",
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