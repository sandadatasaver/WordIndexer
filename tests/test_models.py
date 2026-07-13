from wordindexer.models import IndexEntry


def test_index_entry():

    item = IndexEntry(term="Copy-Item")

    assert item.term == "Copy-Item"

    assert item.whole_word

    assert item.first_only

    assert item.enabled