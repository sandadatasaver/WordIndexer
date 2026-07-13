"""
Match resolver for WordIndexer.

Removes overlapping matches and keeps the most
specific (longest) match.
"""

from __future__ import annotations

from wordindexer.models import Match, RunLocation


class MatchResolver:
    """
    Resolves overlapping matches.

    Rule:
        Longer matches win.
    """

    def resolve(
        self,
        matches: list[Match],
    ) -> list[Match]:

        resolved: list[Match] = []

        for match in matches:

            # sort locations by longest match first
            ordered = sorted(
                match.locations,
                key=lambda x: (x.end - x.start),
                reverse=True,
            )

            accepted: list[RunLocation] = []

            for candidate in ordered:

                overlap = False

                for existing in accepted:

                    if (
                        candidate.start < existing.end
                        and candidate.end > existing.start
                    ):
                        overlap = True
                        break

                if not overlap:
                    accepted.append(candidate)

            match.locations = sorted(
                accepted,
                key=lambda x: x.start,
            )

            resolved.append(match)

        return resolved