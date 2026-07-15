"""
Global match resolver for WordIndexer.

Removes overlapping occurrences and keeps the most specific match, normally
the one with the greatest visible length.
"""

from __future__ import annotations

from wordindexer.models import Match, RunLocation


class MatchResolver:
    """Resolve overlapping run-level occurrences."""

    @staticmethod
    def _location_length(location: RunLocation) -> int:
        return location.end - location.start

    @classmethod
    def _normalize_locations(
        cls,
        locations: list[RunLocation],
    ) -> list[RunLocation]:
        """Remove overlapping fragments within one Match."""
        accepted: list[RunLocation] = []

        ordered = sorted(
            locations,
            key=lambda location: (
                -cls._location_length(location),
                location.run_index,
                location.start,
            ),
        )

        for candidate in ordered:
            overlaps = any(
                candidate.run_index == existing.run_index
                and candidate.start < existing.end
                and existing.start < candidate.end
                for existing in accepted
            )

            if not overlaps:
                accepted.append(candidate)

        return sorted(
            accepted,
            key=lambda location: (location.run_index, location.start),
        )

    @staticmethod
    def _matches_overlap(left: Match, right: Match) -> bool:
        """Return whether two Matches occupy any of the same run text."""
        if left.paragraph_index != right.paragraph_index:
            return False

        return any(
            left_location.run_index == right_location.run_index
            and left_location.start < right_location.end
            and right_location.start < left_location.end
            for left_location in left.locations
            for right_location in right.locations
        )

    @classmethod
    def _match_length(cls, match: Match) -> int:
        return sum(cls._location_length(location) for location in match.locations)

    @staticmethod
    def _document_position(match: Match) -> tuple[int, int, int]:
        if not match.locations:
            return match.paragraph_index, 0, 0

        first = match.locations[0]
        return match.paragraph_index, first.run_index, first.start

    def resolve(self, matches: list[Match]) -> list[Match]:
        """
        Resolve overlaps across all supplied matches.

        Longer matches are considered first. If two matches have the same
        length, their original order is used as the deterministic tie-breaker.
        Matches without run locations are retained because their overlap cannot
        be determined safely.
        """
        located: list[tuple[int, Match]] = []
        unlocated: list[tuple[int, Match]] = []

        for original_index, match in enumerate(matches):
            if match.locations:
                match.locations = self._normalize_locations(match.locations)
                located.append((original_index, match))
            else:
                unlocated.append((original_index, match))

        located.sort(
            key=lambda item: (
                -self._match_length(item[1]),
                item[1].paragraph_index,
                self._document_position(item[1])[1],
                self._document_position(item[1])[2],
                item[0],
            )
        )

        accepted: list[Match] = []

        for _, candidate in located:
            if any(
                self._matches_overlap(candidate, existing)
                for existing in accepted
            ):
                continue

            accepted.append(candidate)

        resolved = [match for _, match in unlocated] + accepted
        resolved.sort(key=self._document_position)
        return resolved
