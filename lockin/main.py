import os
import re
import time
import praw

reddit = praw.Reddit(
    client_id="c2fnLb3DhuhQhIBko1o7uw",
    client_secret="vd1cEvYZhTyjC3tjioBRPUkli_DPFQ",
    password="fominoh946@ametitas.comfominoh946@ametitas.com",
    user_agent="android:com.app.spiritedfly:v12.4321.321 (by u/Spirited_Fly3248)",
    username="Spirited_Fly3248",
)

last_title_new = ""
last_title = ""

weights = {}


def contains_no_numbers(match:str) -> bool:
    return not any(char.isdigit() for char in match)
    
def get_ticker(title: str)->list[str]:
    matches = re.findall(r'\b[A-Z]+\b|\$\w+', title)
    matches = [match.replace("$", "").upper() for match in matches]
    matches = [match for match in matches if contains_no_numbers(match)]
    return matches

def ok_lets_work_with_weigths(weights:dict[str, list[tuple[int, float]]]):
    current_date = time.time()
    scores = {}
    
    for ticker, submissions in weights.items():

        score = 0.0

        for tuplee in submissions:

            comments, date = tuplee

            date_diff = current_date - date
            multiplier = 1000.0

            if date_diff < 60*60*1:
                multiplier /= 1
            elif date_diff < 60*60*2:
                multiplier /= 2
            elif date_diff < 60*60*4:
                multiplier /= 4
            elif date_diff < 60*60*8:
                multiplier /= 8
            elif date_diff < 60*60*16:
                multiplier /= 16
            elif date_diff < 60*60*32:
                multiplier /= 32
            elif date_diff < 60*60*64:
                multiplier /= 64
            elif date_diff < 60*60*128:
                multiplier /= 128
            else:
                multiplier = 0.0

            
            score += comments * multiplier
            
        scores[ticker] = score

    sorted_dict = dict(sorted(scores.items(), key=lambda item: item[1]))
    os.system('clear')
    for ticker,score in sorted_dict.items():
        rounded_score = round(score)
        print(f"{ticker:<20}\t{rounded_score}")

while True:
    submissions = reddit.subreddit("wallstreetbets").new(limit=100)

    first = True
    
    for submission in submissions:
        if first:
            last_title_new = submission.title
            first = False
            
        if submission.title == last_title:
            break
        
        tickers = get_ticker(submission.title)
        comments = submission.num_comments
        date = submission.created_utc
        for ticker in tickers:
            if ticker not in weights:
                weights[ticker] = []
            weights[ticker].append((comments, date))

    last_title = last_title_new

    ok_lets_work_with_weigths(weights)
        
    time.sleep(60)

