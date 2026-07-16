from wordindexer.models import RunLocation


def test_run_location():

    loc = RunLocation(
        paragraph_index=1,
        run_index=2,
        start=5,
        end=15,
        matched_text="PowerShell",
    )

    assert loc.run_index == 2
    assert loc.start == 5
    assert loc.end == 15