from app.assistants.base import BaseAssistant
from app.config import (
    LM_STUDIO_BASE_URL,
    CHAT_MODEL,
    EMBEDDING_MODEL,
    DATA_DIR,
    OBSIDIAN_VAULT_DIR,
    DEV_FAST_MODE,
    DEFAULT_SUMMARY_LIMIT,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_OVERLAP,
    DEFAULT_TOP_K,
    DEFAULT_RESPONSE_MODE,
)
from app.llm_client import LLMClient


class ChatAssistant(BaseAssistant):
    def __init__(self):
        self.llm = None

    def _get_llm(self) -> LLMClient:
        if self.llm is None:
            self.llm = LLMClient()
        return self.llm

    def health(self) -> dict:
        processed_dir = DATA_DIR / "processed"
        vault_dir = OBSIDIAN_VAULT_DIR

        processed_documents_count = 0
        if processed_dir.exists() and processed_dir.is_dir():
            processed_documents_count = len(
                [p for p in processed_dir.iterdir() if p.is_dir()]
            )

        client = self._get_llm()
        llm_reachable, llm_error = client.is_reachable()

        status = "ok" if llm_reachable else "degraded"

        return {
            "status": status,
            "service": "local-chat-assistant",
            "assistant_type": "chat",
            "dev_fast_mode": DEV_FAST_MODE,
            "base_url": LM_STUDIO_BASE_URL,
            "chat_model": CHAT_MODEL,
            "embedding_model": EMBEDDING_MODEL,
            "defaults": {
                "summary_limit": DEFAULT_SUMMARY_LIMIT,
                "chunk_size": DEFAULT_CHUNK_SIZE,
                "overlap": DEFAULT_OVERLAP,
                "top_k": DEFAULT_TOP_K,
                "response_mode": DEFAULT_RESPONSE_MODE,
            },
            "storage": {
                "vault_dir": str(vault_dir.resolve()),
                "vault_dir_exists": vault_dir.exists(),
                "processed_data_dir": str(processed_dir.resolve()),
                "processed_data_dir_exists": processed_dir.exists(),
                "processed_documents_count": processed_documents_count,
            },
            "runtime": {
                "embedder_loaded": False,
                "rag_loaded": False,
            },
            "llm_connection": {
                "reachable": llm_reachable,
                "error": llm_error,
            },
        }

    def process_document(
        self,
        filename: str,
        summary_limit: int = 4000,
        chunk_size: int = 500,
        overlap: int = 100,
        force_rebuild: bool = False,
    ) -> dict:
        return {
            "status": "skipped",
            "assistant_type": "chat",
            "filename": filename,
            "message": "ChatAssistant does not process documents.",
        }

    def ask(
        self,
        question: str,
        filename: str | None = None,
        top_k: int = 3,
        chunk_size: int = 500,
        overlap: int = 100,
        auto_process: bool = True,
        response_mode: str = "detailed",
    ) -> dict:
        system_prompt = (
            "You are a helpful local AI coding and general-purpose assistant. "
            "Answer clearly, practically, and with good structure. "
            "If the user asks for code, provide usable code."
        )

        if response_mode == "short":
            system_prompt += " Keep answers concise."
        else:
            system_prompt += " Give a reasonably detailed answer."

        answer = self._get_llm().ask(
            prompt=question,
            model=CHAT_MODEL,
            system_prompt=system_prompt,
            temperature=0.3,
        )

        return {
            "source_document": filename or "",
            "question": question,
            "answer": answer,
            "rag_note_path": "",
            "top_chunks": [],
        }