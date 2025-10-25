from praw import Reddit
from collections import defaultdict
import format
import parse
import time
import sys


def main() -> None:
    arguments = sys.argv

    reddit = Reddit(
        client_id=arguments[1],
        client_secret=arguments[2],
        password=arguments[3],
        username=arguments[4],
        user_agent="android:com.app.spiritedfly:v12.4321.321 (by u/Spirited_Fly3248)",
    )

    last_title_new = ""
    last_title = ""

    scores = defaultdict(list)

    while True:
        submissions = reddit.subreddit("wallstreetbets").new(limit=100)

        first = True

        for submission in submissions:
            if first:
                last_title_new = submission.title
                first = False

            if submission.title == last_title:
                break

            tickers = parse.tickers(submission.title)
            score = submission.num_comments + submission.score
            epoch = submission.created_utc

            for ticker in tickers:
                scores[ticker].append((score, epoch))

        last_title = last_title_new

        scores_format = format.scores(scores)
        print(scores_format)

        time.sleep(60)


if __name__ == "__main__":
    main()
