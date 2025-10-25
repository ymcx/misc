from praw import Reddit
from collections import defaultdict
import os
import format
import parse
import time
import sys
import graph

SUBREDDITS = ["wallstreetbets", "pennystocks"]
POLL_INTERVAL = 5
AMOUNT_TO_LIST = 10


def read_credentials(path: str) -> dict[str, str]:
    file = open(path)
    credentials = [line.strip().split("=") for line in file]
    file.close()

    return dict(credentials)


def get_reddit(credentials: dict[str, str]) -> Reddit:
    return Reddit(
        client_id=credentials["client_id"],
        client_secret=credentials["client_secret"],
        password=credentials["password"],
        username=credentials["username"],
        user_agent="Mozarella Firecat",
    )


def main() -> None:
    credentials = read_credentials(sys.argv[1])
    reddit = get_reddit(credentials)
    figure, axes, lines = graph.create()

    scores = defaultdict(defaultdict)
    subreddits = "+".join(SUBREDDITS)
    iteration = 0

    while True:
        submissions = reddit.subreddit(subreddits).new()

        for submission in submissions:
            id = submission.id
            title = submission.title
            comments = submission.num_comments
            score = submission.score
            ratio = submission.upvote_ratio
            epoch = submission.created_utc

            tickers = parse.tickers(title)

            for ticker in tickers:
                scores[ticker][id] = (comments, score, ratio, epoch)

        scores_str = format.scores_str(scores, AMOUNT_TO_LIST)
        os.system("clear")
        print(scores_str)

        scores_data = format.scores_data(scores, AMOUNT_TO_LIST)
        graph.update(iteration, scores_data, figure, axes, lines)

        iteration += 1
        time.sleep(60 * POLL_INTERVAL)


if __name__ == "__main__":
    main()
