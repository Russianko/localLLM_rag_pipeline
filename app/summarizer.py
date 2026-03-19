from app.config import CHAT_MODEL
from app.llm_client import LLMClient
from app.prompts import SUMMARY_PROMPT, KEY_POINTS_PROMPT, ACTION_ITEMS_PROMPT


class Summarizer:
    def __init__(self):
        self.llm = LLMClient()

    def generate_summary(self, document_text: str) -> str:
        prompt = SUMMARY_PROMPT.format(document_text=document_text)
        return self.llm.ask(prompt=prompt, model=CHAT_MODEL)

    def extract_key_points(self, document_text: str) -> str:
        prompt = KEY_POINTS_PROMPT.format(document_text=document_text)
        return self.llm.ask(prompt=prompt, model=CHAT_MODEL)

    def extract_action_items(self, document_text: str) -> str:
        prompt = ACTION_ITEMS_PROMPT.format(document_text=document_text)
        return self.llm.ask(prompt=prompt, model=CHAT_MODEL)