from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import re

ELEMENT_POPUP = "//div[@aria-labelledby='modal-header']"
ELEMENT_TEXT = "//div[@data-testid='tweetText']"
ELEMENT_NAME = "//button[text()='Replying to ']"


class Tweet:
    def __init__(self, chrome: Chrome) -> None:
        self.chrome = chrome
        self.popup: WebElement | None = None
        self.text: str | None = None
        self.username: str | None = None

    def get_popup(self) -> WebElement:
        if self.popup:
            return self.popup

        popup = self.chrome.find_element(By.XPATH, ELEMENT_POPUP)

        self.popup = popup
        return self.popup

    def get_text(self) -> str:
        if self.text:
            return self.text

        self.popup = self.get_popup()

        text = self.popup.find_element(By.XPATH, ELEMENT_TEXT).text
        text = re.sub(r"\bhttp\S*", "", text)
        text = text.strip()

        self.text = text
        return self.text

    def get_username(self) -> str:
        if self.username:
            return self.username

        self.popup = self.get_popup()

        username = self.popup.find_element(By.XPATH, ELEMENT_NAME).text

        self.username = username
        return self.username

    def is_valid(self, username: str) -> tuple[bool, str | None]:
        self.text = self.get_text()
        self.username = self.get_username()

        text_cur_len, text_min_len = len(self.text), 60
        if text_cur_len < text_min_len:
            return (False, f"Tweet:\tInvalid length ({text_cur_len} < {text_min_len})")

        if self.username.__contains__(username):
            return (False, "Tweet:\tCan't reply to yourself")

        return (True, None)
