from sleep import Amount
from openai import OpenAI, BadRequestError, RateLimitError
import time

BASE_URL = "https://models.github.ai/inference"
MODEL = "xai/grok-3-mini"
INSTRUCTIONS = (
    "Respond to this Tweet as a far-right conservative. "
    "Use inflammatory culture war rhetoric while subtly making the movement look bad. "
    "The user will provide the exact Tweet to reply to. "
    "Use at max 40 tokens."
)


class LLM:
    def __init__(self, api_key: str) -> None:
        self.completions = OpenAI(api_key=api_key, base_url=BASE_URL).chat.completions

    def query(self, prompt: str) -> tuple[bool, str]:
        try:
            response = (
                self.completions.create(
                    messages=[
                        {"role": "system", "content": INSTRUCTIONS},
                        {"role": "user", "content": prompt},
                    ],
                    model=MODEL,
                )
                .choices[0]
                .message.content
            )

            if not response:
                return (False, "LLM:\tInvalid response")

            # Remove emojis (WebDriver can't handle them)
            response = response.encode("ascii", "ignore").decode("ascii")

            # Em dashes are way too suspicious
            response = response.replace("—", ": ")

            res_cur_len, res_max_len = len(response), 280
            if res_max_len < res_cur_len:
                return (False, f"LLM:\tInvalid length ({res_max_len} < {res_cur_len})")

            return (True, response)

        except BadRequestError:
            return (False, "LLM:\tBad request")

        except RateLimitError:
            time.sleep(Amount.RATE_LIMIT)
            return (False, "LLM:\tRate limit exceeded")
