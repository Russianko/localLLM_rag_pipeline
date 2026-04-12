from openai import OpenAI
from app.config import LM_STUDIO_BASE_URL, LM_STUDIO_API_KEY


DEFAULT_SYSTEM_PROMPT = "You are a helpful local AI assistant."


class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            base_url=LM_STUDIO_BASE_URL,
            api_key=LM_STUDIO_API_KEY,
            timeout=60.0,
        )

    def get_models(self):
        return self.client.models.list()

    def is_reachable(self) -> tuple[bool, str | None]:
        try:
            self.get_models()
            return True, None
        except Exception as e:
            return False, str(e)

    def ask(
        self,
        prompt: str,
        model: str,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        temperature: float = 0.3,
    ) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content