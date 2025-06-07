from llm import LLM
from selenium.webdriver import ActionChains, Chrome, Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import time


class Twitter:
    def __init__(self, llm: LLM, chrome: Chrome, username: str, password: str) -> None:
        self.llm = llm
        self.chrome = chrome
        self.username = username
        self.password = password

    def __type(self, text: str) -> None:
        self.chrome.switch_to.active_element.send_keys(text)

    def __close(self) -> None:
        self.__type(Keys.ESCAPE)

    def __confirm(self) -> None:
        self.__type(Keys.ENTER)

    def __open_tweet(self) -> None:
        self.__type("r")

    def __focus_next(self) -> None:
        self.__type("j")

    def __get_input_field(self) -> WebElement:
        return self.chrome.find_element(By.XPATH, "//input")

    def __get_tweet_text(self) -> str:
        popup = "//div[@aria-labelledby='modal-header']"
        body = "//div[@data-testid='tweetText']"
        element = self.chrome.find_element(By.XPATH, popup).find_element(By.XPATH, body)
        return element.text

    def __open_login_page(self) -> None:
        self.chrome.get("https://x.com/i/flow/login")

    def __send_tweet(self) -> None:
        action = (
            ActionChains(self.chrome)
            .key_down(Keys.CONTROL)
            .send_keys(Keys.ENTER)
            .key_up(Keys.CONTROL)
        )
        action.perform()

    def login(self) -> None:
        self.__open_login_page()
        time.sleep(3)

        self.__get_input_field().send_keys(self.username)
        self.__confirm()
        time.sleep(1)

        self.__type(self.password)
        self.__confirm()
        time.sleep(6)

    def next(self) -> None:
        self.__focus_next()
        self.__open_tweet()

        tweet = self.__get_tweet_text()
        reply = self.llm.query(tweet)
        if not reply:
            print("Err")
            return self.__close()

        self.__type(reply)
        self.__send_tweet()
        time.sleep(3)
