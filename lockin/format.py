import os
import time


def scores(scores: dict[str, list[tuple[int, float]]]) -> str:
    current_date = time.time()
    scores_new = {}

    for ticker, submissions in scores.items():
        score = 0.0

        for tuplee in submissions:
            comments, date = tuplee

            date_diff = current_date - date
            multiplier = 1000.0

            if date_diff < 60 * 60 * 1:
                multiplier /= 1
            elif date_diff < 60 * 60 * 2:
                multiplier /= 2
            elif date_diff < 60 * 60 * 4:
                multiplier /= 4
            elif date_diff < 60 * 60 * 8:
                multiplier /= 8
            elif date_diff < 60 * 60 * 16:
                multiplier /= 16
            elif date_diff < 60 * 60 * 32:
                multiplier /= 32
            elif date_diff < 60 * 60 * 64:
                multiplier /= 64
            elif date_diff < 60 * 60 * 128:
                multiplier /= 128
            else:
                multiplier = 0.0

            score += comments * multiplier

        scores_new[ticker] = score

    sorted_dict = dict(sorted(scores_new.items(), key=lambda item: item[1]))
    os.system("clear")

    output = []
    for ticker, score in sorted_dict.items():
        rounded_score = round(score)
        output.append(f"{ticker:<20}\t{rounded_score}")

    return "\n".join(output)
