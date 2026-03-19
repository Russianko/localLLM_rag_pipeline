from openai import OpenAI
from app.config import BASE_URL, API_KEY


class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            base_url=BASE_URL,
            api_key=API_KEY,
        )

    def get_models(self):
        return self.client.models.list()

    def ask(self, prompt: str, model: str):
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful local AI assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content

