from app.assistants.base import BaseAssistant
from app.config import DATA_DIR, OBSIDIAN_VAULT_DIR


class DummyAssistant(BaseAssistant):
    def health(self) -> dict:
        return {
            "status": "ok",
            "base_url": "dummy://local",
            "chat_model": "dummy-model",
            "embedding_model": "dummy-embedding",
            "vault_dir": str(OBSIDIAN_VAULT_DIR.resolve()),
            "processed_data_dir": str((DATA_DIR / "processed").resolve()),
            "assistant_type": "dummy",
            "embedder_loaded": False,
            "rag_loaded": False,
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
            "status": "processed",
            "source_document": filename,
            "summary": f"Dummy summary for {filename}",
            "key_points": [
                "Это тестовый ассистент.",
                "Он нужен для проверки переключаемой архитектуры.",
            ],
            "action_items": [
                "Проверить /health",
                "Проверить /process",
                "Проверить /ask",
            ],
            "document_note_path": "dummy://document_note",
            "raw_text_path": "dummy://raw_text",
            "clean_text_path": "dummy://clean_text",
            "summary_path": "dummy://summary",
            "chunks_path": "dummy://chunks",
            "embeddings_path": "dummy://embeddings",
            "chunks_count": 0,
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
        return {
            "source_document": filename or "",
            "question": question,
            "answer": f"[DummyAssistant] Тестовый ответ на вопрос: {question}",
            "rag_note_path": "",
            "top_chunks": [],
        }

