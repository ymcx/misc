from llm import LLM
from twitter import Twitter
from selenium.webdriver import Chrome
import sys


def main() -> None:
    if len(sys.argv) != 4:
        print("Invalid amount of arguments")
        return

    _, username, password, api_key = sys.argv
    llm = LLM(api_key)
    chrome = Chrome()
    twitter = Twitter(llm, chrome, username, password)

    twitter.login()
    for _ in range(10):
        twitter.next()


if __name__ == "__main__":
    main()
