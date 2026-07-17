import json

from wordindexer.dictionary import DictionaryLoader


def test_dictionary_loads_hierarchy_and_cross_references(tmp_path):
    filename = tmp_path / "references.json"
    filename.write_text(
        json.dumps(
            {
                "metadata": {
                    "name": "Reference Test",
                    "version": "1.0",
                },
                "entries": [
                    {
                        "term": "pwsh",
                        "index_as": "pwsh",
                        "see": "PowerShell",
                    },
                    {
                        "term": "PowerShell",
                        "parent": "Microsoft",
                        "subentry": "Commands",
                        "see_also": [
                            "Windows PowerShell",
                            "PowerShell Core",
                        ],
                    },
                    {
                        "term": "Windows PowerShell",
                        "see_also": "PowerShell",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    entries = DictionaryLoader(filename).load_entries()

    assert entries[0].see == "PowerShell"
    assert entries[0].see_also == []
    assert entries[1].parent == "Microsoft"
    assert entries[1].subentry == "Commands"
    assert entries[1].see_also == [
        "Windows PowerShell",
        "PowerShell Core",
    ]
    assert entries[2].see_also == ["PowerShell"]
