from operator import itemgetter
from collections import defaultdict
from itertools import islice
import calculate


def _sum(
    scores: dict[str, dict[int, tuple[int, int, float, float]]],
) -> dict[str, float]:
    scores_summed = defaultdict(float)

    for ticker, submissions in scores.items():
        for _, submission in submissions.items():
            comments, score, ratio, epoch = submission
            scores_summed[ticker] += calculate.score(comments, score, ratio, epoch)

    return scores_summed


def _sort(scores: dict[str, float]) -> dict[str, float]:
    scores_sorted = sorted(scores.items(), key=itemgetter(1), reverse=True)

    return dict(scores_sorted)


def _format(scores: dict[str, float], n: int) -> str:
    scores_formatted = []

    for ticker, score in islice(scores.items(), n):
        line = f"{ticker:<20} {score:>10.0f}"
        scores_formatted.append(line)

    return "\n".join(scores_formatted)


def scores(scores: dict[str, dict[int, tuple[int, int, float, float]]], n: int) -> str:
    scores_summed = _sum(scores)
    scores_sorted = _sort(scores_summed)
    scores_formatted = _format(scores_sorted, n)

    return scores_formatted
