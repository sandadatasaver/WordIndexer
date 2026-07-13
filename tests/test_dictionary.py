from wordindexer.dictionary import DictionaryLoader


def test_dictionary():

    loader = DictionaryLoader("dictionaries/powershell.json")

    info = loader.info()

    assert info.entries > 0
    assert info.name == "PowerShell Dictionary"