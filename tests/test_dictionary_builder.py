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
        "term,aliases,category,enabled,source,occurrences,paragraphs,contexts"
    )


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
