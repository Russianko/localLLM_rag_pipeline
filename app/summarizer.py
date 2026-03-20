from app.config import CHAT_MODEL
from app.llm_client import LLMClient
from app.prompts import (
    SUMMARY_PROMPT,
    KEY_POINTS_PROMPT,
    ACTION_ITEMS_PROMPT,
)


class Summarizer:
    def __init__(self):
        self.llm = LLMClient()

    def generate_summary(self, text: str) -> str:
        prompt = SUMMARY_PROMPT.format(text=text)
        response = self.llm.ask(prompt=prompt, model=CHAT_MODEL)
        return (response or "").strip()

    def extract_key_points(self, text: str) -> list[str]:
        prompt = KEY_POINTS_PROMPT.format(text=text)
        response = self.llm.ask(prompt=prompt, model=CHAT_MODEL)
        return self._to_lines(response)

    def extract_action_items(self, text: str) -> list[str]:
        prompt = ACTION_ITEMS_PROMPT.format(text=text)
        response = self.llm.ask(prompt=prompt, model=CHAT_MODEL)
        return self._to_lines(response)

    @staticmethod
    def _to_lines(value: str) -> list[str]:
        if not value:
            return []

        lines = []
        for line in value.splitlines():
            cleaned = line.strip().lstrip("-•*").strip()
            if cleaned:
                lines.append(cleaned)

        return lines