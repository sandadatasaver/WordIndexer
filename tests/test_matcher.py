from wordindexer.matcher import MatchResolver
from wordindexer.models import Match, RunLocation


def test_overlap_resolution():

    match = Match(
        term="PowerShell",
        matched_text="PowerShell",
        paragraph_index=0,
        paragraph_text="PowerShell 7",
    )

    match.locations = [

        RunLocation(
            paragraph_index=0,
            run_index=0,
            start=0,
            end=10,
            matched_text="PowerShell",
        ),

        RunLocation(
            paragraph_index=0,
            run_index=0,
            start=0,
            end=12,
            matched_text="PowerShell 7",
        ),

    ]

    resolver = MatchResolver()

    resolved = resolver.resolve([match])

    assert len(resolved[0].locations) == 1

    assert resolved[0].locations[0].matched_text == "PowerShell 7"