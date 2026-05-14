from llm import LLM
from twitter import Twitter
from selenium.webdriver import Chrome
import sys


def main() -> None:
    args_cur_amount, args_cor_amount = len(sys.argv), 4
    if args_cur_amount != args_cor_amount:
        message = f"Invalid amount of arguments provided ({args_cur_amount} != {args_cor_amount})"
        return print(message)

    _, username, password, api_key = sys.argv
    llm = LLM(api_key)
    chrome = Chrome()
    twitter = Twitter(llm, chrome, username, password)

    twitter.login()
    while True:
        for _ in range(10):
            twitter.next()
        twitter.refresh()


if __name__ == "__main__":
    main()
