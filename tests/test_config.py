from wordindexer.config import ConfigManager


def test_defaults_loaded():
    cfg = ConfigManager("does_not_exist.json")
    cfg.load()

    assert cfg.get("ignore_before_toc") is True
    assert cfg.get("whole_word_only") is True
    assert cfg.get("case_sensitive") is False