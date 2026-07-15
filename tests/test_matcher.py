from wordindexer.matcher import MatchResolver
from wordindexer.models import Match, RunLocation


def location(start: int, end: int, text: str) -> RunLocation:
    return RunLocation(
        paragraph_index=0,
        run_index=0,
        start=start,
        end=end,
        matched_text=text,
    )


def match(term: str, start: int, end: int, text: str) -> Match:
    return Match(
        term=term,
        matched_text=text,
        paragraph_index=0,
        paragraph_text="Windows PowerShell 7",
        locations=[location(start, end, text)],
    )


def test_overlap_resolution_within_one_match():
    item = Match(
        term="PowerShell",
        matched_text="PowerShell",
        paragraph_index=0,
        paragraph_text="PowerShell 7",
        locations=[
            location(0, 10, "PowerShell"),
            location(0, 12, "PowerShell 7"),
        ],
    )

    resolved = MatchResolver().resolve([item])

    assert len(resolved) == 1
    assert len(resolved[0].locations) == 1
    assert resolved[0].locations[0].matched_text == "PowerShell 7"


def test_global_overlap_prefers_longest_match():
    short = match("PowerShell", 9, 19, "PowerShell")
    long = match("Windows PowerShell", 0, 19, "Windows PowerShell")

    resolved = MatchResolver().resolve([short, long])

    assert len(resolved) == 1
    assert resolved[0].term == "Windows PowerShell"


def test_non_overlapping_matches_are_preserved():
    first = match("Windows", 0, 7, "Windows")
    second = match("PowerShell", 8, 18, "PowerShell")

    resolved = MatchResolver().resolve([first, second])

    assert len(resolved) == 2
    assert [item.term for item in resolved] == [
        "Windows",
        "PowerShell",
    ]


def test_split_run_match_overlaps_match_in_later_run():
    long = Match(
        term="PowerShell",
        matched_text="PowerShell",
        paragraph_index=0,
        paragraph_text="PowerShell",
        locations=[
            RunLocation(0, 0, 0, 5, "Power"),
            RunLocation(0, 1, 0, 5, "Shell"),
        ],
    )

    short = Match(
        term="Shell",
        matched_text="Shell",
        paragraph_index=0,
        paragraph_text="PowerShell",
        locations=[
            RunLocation(0, 1, 0, 5, "Shell"),
        ],
    )

    resolved = MatchResolver().resolve([short, long])

    assert len(resolved) == 1
    assert resolved[0].term == "PowerShell"
