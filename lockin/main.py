from praw import Reddit
from collections import defaultdict
import format
import parse
import time
import sys

SUBREDDITS = ["wallstreetbets", "pennystocks"]


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

    titles_old = set()
    scores = defaultdict(list)
    subreddits = "+".join(SUBREDDITS)

    while True:
        submissions = reddit.subreddit(subreddits).new(limit=100)

        for submission in submissions:
            if submission.title in titles_old:
                break

            titles_old.add(submission.title)

            tickers = parse.tickers(submission.title)
            score = submission.num_comments + submission.score
            epoch = submission.created_utc

            for ticker in tickers:
                scores[ticker].append((score, epoch))

        scores_format = format.scores(scores)
        print(scores_format)

        time.sleep(60)


if __name__ == "__main__":
    main()
