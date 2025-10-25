from operator import itemgetter
from collections import defaultdict
import calculate


def _sum(scores: dict[str, list[tuple[int, float]]]) -> dict[str, int]:
    scores_summed = defaultdict(int)

    for ticker, entries in scores.items():
        for score, date in entries:
            scores_summed[ticker] += calculate.score(score, date)

    return scores_summed


def _sort(scores: dict[str, int]) -> dict[str, int]:
    scores_sorted = sorted(scores.items(), key=itemgetter(1))

    return dict(scores_sorted)


def _format(scores: dict[str, int]) -> str:
    scores_formatted = []

    for ticker, score in scores.items():
        line = f"{ticker:<20} {score:>20.0f}"
        scores_formatted.append(line)

    return "\n".join(scores_formatted)


def scores(scores: dict[str, list[tuple[int, float]]]) -> str:
    scores_summed = _sum(scores)
    scores_sorted = _sort(scores_summed)
    scores_formatted = _format(scores_sorted)

    return scores_formatted
