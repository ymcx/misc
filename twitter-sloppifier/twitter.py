from sleep import Amount
from tweet import Tweet
from llm import LLM
from selenium.webdriver import ActionChains, Chrome, Keys
from selenium.webdriver.common.by import By
import time


class Twitter:
    def __init__(self, llm: LLM, chrome: Chrome, username: str, password: str) -> None:
        self.llm = llm
        self.chrome = chrome
        self.username = username
        self.password = password

    def type(self, text: str) -> None:
        self.chrome.switch_to.active_element.send_keys(text)

    def close(self) -> None:
        self.type(Keys.ESCAPE)

    def confirm(self) -> None:
        self.type(Keys.ENTER)

    def refresh(self) -> None:
        self.type(".")

    def open_focused_tweet(self) -> None:
        self.type("r")

    def focus_next_tweet(self) -> None:
        self.type("j")

    def send_tweet(self, text: str) -> None:
        send = (
            ActionChains(self.chrome)
            .key_down(Keys.CONTROL)
            .send_keys(Keys.ENTER)
            .key_up(Keys.CONTROL)
        )

        self.type(text)
        send.perform()

    def login(self) -> None:
        self.chrome.get("https://x.com/i/flow/login")
        time.sleep(Amount.URL_LOAD)

        self.chrome.find_element(By.CSS_SELECTOR, "input").send_keys(self.username)
        self.confirm()
        time.sleep(Amount.USER_TO_PASS)

        self.type(self.password)
        self.confirm()
        time.sleep(Amount.PASS_TO_HOME)

    def next(self) -> None:
        self.focus_next_tweet()
        self.open_focused_tweet()
        time.sleep(Amount.TWEET_OPEN)

        tweet = Tweet(self.chrome)
        valid, error_message = tweet.is_valid(self.username)
        if not valid:
            print(error_message)
            return self.close()

        text = tweet.get_text()
        valid, response = self.llm.query(text)
        if not valid:
            print(response)
            return self.close()

        self.send_tweet(response)
