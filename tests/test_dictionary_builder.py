import json

from wordindexer.dictionary import DictionaryLoader
from wordindexer.dictionary_builder import DictionaryDraftBuilder


def discovery_payload():
    return {
        "input_path": "book.docx",
        "body_start": 10,
        "toc_method": "first_chapter_heading",
        "candidates": [
            {
                "term": "ImportExcel",
                "occurrences": 4,
                "variants": ["ImportExcel"],
                "paragraphs": [20, 25],
                "contexts": ["ImportExcel is useful."],
                "suggested_entry": {
                    "term": "ImportExcel",
                    "aliases": [],
                    "index_as": "ImportExcel",
                    "category": "",
                    "enabled": True,
                },
            }
        ],
    }


def test_dictionary_draft_is_disabled_by_default(tmp_path):
    discovery = tmp_path / "discovery.json"
    discovery.write_text(json.dumps(discovery_payload()), encoding="utf-8")
    output = tmp_path / "draft.json"
    csv_output = tmp_path / "draft.csv"

    DictionaryDraftBuilder().build(
        discovery,
        output,
        csv_output=csv_output,
    )

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["metadata"]["review_required"] is True
    assert data["entries"][0]["enabled"] is False
    assert data["entries"][0]["evidence"]["occurrences"] == 4

    entries = DictionaryLoader(output).load_entries()
    assert entries[0].term == "ImportExcel"
    assert entries[0].enabled is False
    assert csv_output.read_text(encoding="utf-8").startswith(
        "term,aliases,index_as,parent,subentry,definition,see,see_also,category,enabled"
    )


def test_finalize_csv_creates_reviewed_dictionary(tmp_path):
    reviewed = tmp_path / "reviewed.csv"
    reviewed.write_text(
        "term,aliases,index_as,parent,subentry,definition,see,see_also,"
        "category,enabled,include_in_glossary,source,occurrences,paragraphs,contexts\n"
        "ImportExcel,ie,ImportExcel,PowerShell,Modules,"
        "An import module.,,PowerShell Core,Technology,True,True,reviewed,4,20;25,Useful term\n",
        encoding="utf-8",
    )
    output = tmp_path / "final.json"

    DictionaryDraftBuilder().finalize_csv(reviewed, output)
    entries = DictionaryLoader(output).load_entries()

    assert entries[0].term == "ImportExcel"
    assert entries[0].aliases == ["ie"]
    assert entries[0].parent == "PowerShell"
    assert entries[0].subentry == "Modules"
    assert entries[0].definition == "An import module."
    assert entries[0].see_also == ["PowerShell Core"]
    assert entries[0].enabled is True


def test_dictionary_draft_can_enable_candidates_explicitly(tmp_path):
    discovery = tmp_path / "discovery.json"
    discovery.write_text(json.dumps(discovery_payload()), encoding="utf-8")
    output = tmp_path / "draft_enabled.json"

    DictionaryDraftBuilder().build(
        discovery,
        output,
        enable_candidates=True,
    )

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["metadata"]["review_required"] is False
    assert data["entries"][0]["enabled"] is True
