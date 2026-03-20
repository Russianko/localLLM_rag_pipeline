from app.assistants.base import BaseAssistant
from app.assistants.factory import build_assistant
from app.storage import DocumentStorage
from app.config import DATA_DIR, ASSISTANT_TYPE


class PipelineService:
    def __init__(self, assistant: BaseAssistant | None = None):
        self.assistant = assistant or build_assistant(ASSISTANT_TYPE)
        self.storage = DocumentStorage(DATA_DIR / "processed")

    def health(self) -> dict:
        return self.assistant.health()

    def process_document(
        self,
        filename: str,
        summary_limit: int = 4000,
        chunk_size: int = 500,
        overlap: int = 100,
        force_rebuild: bool = False,
    ) -> dict:
        return self.assistant.process_document(
            filename=filename,
            summary_limit=summary_limit,
            chunk_size=chunk_size,
            overlap=overlap,
            force_rebuild=force_rebuild,
        )

    def ask_document(
            self,
            filename: str,
            question: str,
            top_k: int = 3,
            chunk_size: int = 500,
            overlap: int = 100,
            auto_process: bool = True,
            response_mode: str = "detailed",
    ) -> dict:
        return self.assistant.ask(
            filename=filename,
            question=question,
            top_k=top_k,
            chunk_size=chunk_size,
            overlap=overlap,
            auto_process=auto_process,
            response_mode=response_mode,
        )

    def list_documents(self) -> list[dict]:
        docs = self.storage.list_documents()
        result = []

        for doc_id in docs:
            result.append(
                {
                    "id": doc_id,
                    "has_embeddings": self.storage.get_embeddings_path(doc_id).exists(),
                    "has_chunks": self.storage.get_chunks_path(doc_id).exists(),
                    "has_summary": self.storage.get_summary_path(doc_id).exists(),
                }
            )

        return result

    def get_document(self, doc_id: str) -> dict:
        doc_dir = self.storage.base_dir / doc_id

        if not doc_dir.exists() or not doc_dir.is_dir():
            raise FileNotFoundError(f"Document not found: {doc_id}")

        summary = None
        chunks_count = 0
        has_embeddings = self.storage.get_embeddings_path(doc_id).exists()
        has_summary = self.storage.get_summary_path(doc_id).exists()
        has_chunks = self.storage.get_chunks_path(doc_id).exists()

        if has_summary:
            summary_data = self.storage.load_summary(doc_id)
            summary = summary_data.get("summary")

        if has_chunks:
            chunks = self.storage.load_chunks(doc_id)
            chunks_count = len(chunks)

        return {
            "id": doc_id,
            "summary": summary,
            "chunks_count": chunks_count,
            "has_embeddings": has_embeddings,
            "has_summary": has_summary,
            "has_chunks": has_chunks,
        }

    def delete_document(self, doc_id: str) -> dict:
        deleted = self.storage.delete_document(doc_id)

        if not deleted:
            raise FileNotFoundError(f"Document not found: {doc_id}")

        return {
            "id": doc_id,
            "deleted": True,
        }