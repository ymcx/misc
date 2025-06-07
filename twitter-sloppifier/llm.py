from openai import OpenAI, BadRequestError
from openai.types.chat import ChatCompletionMessageParam

base_url = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"
temperature = 1.0
top_p = 1.0
instructions = (
    "Respond to this Tweet as a far-right conservative. "
    "Use inflammatory culture war rhetoric while subtly making the movement look bad. "
    "The user will provide the exact Tweet to reply to. "
    "Use at max 40 tokens."
)


class LLM:
    def __init__(self, api_key: str) -> None:
        self.openai = OpenAI(api_key=api_key, base_url=base_url)

    def query(self, prompt: str) -> str | None:
        try:
            messages: list[ChatCompletionMessageParam] = [
                {"role": "system", "content": instructions},
                {"role": "user", "content": prompt},
            ]
            response = self.openai.chat.completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                top_p=top_p,
            )
            response = response.choices[0].message.content
            if not response:
                return

            response = response.replace("—", ": ")
            if len(response) < 270:
                return response

        except BadRequestError:
            return
