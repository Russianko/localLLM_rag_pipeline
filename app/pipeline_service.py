from app.assistants.base import BaseAssistant
from app.assistants.factory import build_assistant
from app.storage import DocumentStorage
from app.config import DATA_DIR, get_default_pipeline_params, DEFAULT_RESPONSE_MODE
from app.repositories import ProcessedDocumentRepository
from app.errors import DocumentNotFoundError



class PipelineService:
    def __init__(self, assistant: BaseAssistant | None = None):
        self.assistant = assistant or build_assistant("rag")
        self.storage = DocumentStorage(DATA_DIR / "processed")
        self.repository = ProcessedDocumentRepository(self.storage)

    def health(self) -> dict:
        return self.assistant.health()

    def process_document(
        self,
        filename: str,
        summary_limit: int | None = None,
        chunk_size: int | None = None,
        overlap: int | None = None,
        force_rebuild: bool = False,
    ) -> dict:
        defaults = get_default_pipeline_params()

        summary_limit = defaults["summary_limit"] if summary_limit is None else summary_limit
        chunk_size = defaults["chunk_size"] if chunk_size is None else chunk_size
        overlap = defaults["overlap"] if overlap is None else overlap

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
        top_k: int | None = None,
        chunk_size: int | None = None,
        overlap: int | None = None,
        auto_process: bool = True,
        response_mode: str | None = None,
    ) -> dict:
        defaults = get_default_pipeline_params()

        top_k = defaults["top_k"] if top_k is None else top_k
        chunk_size = defaults["chunk_size"] if chunk_size is None else chunk_size
        overlap = defaults["overlap"] if overlap is None else overlap
        response_mode = DEFAULT_RESPONSE_MODE if response_mode is None else response_mode

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
        return self.repository.list_statuses()

    def get_document(self, doc_id: str) -> dict:
        doc_dir = self.storage.base_dir / doc_id

        if not doc_dir.exists() or not doc_dir.is_dir():
            raise DocumentNotFoundError(f"Document not found: {doc_id}")

        processed_doc = self.repository.load(doc_id)
        status = self.repository.get_status(doc_id)

        return {
            "id": doc_id,
            "summary": processed_doc.summary,
            "chunks_count": processed_doc.chunks_count,
            "has_embeddings": status["has_embeddings"],
            "has_summary": status["has_summary"],
            "has_chunks": status["has_chunks"],
            "has_clean_text": status["has_clean_text"],
            "is_processed": status["is_processed"],
            "has_error": status["has_error"],
        }

    def delete_document(self, doc_id: str) -> dict:
        deleted = self.storage.delete_document(doc_id)

        if not deleted:
            raise DocumentNotFoundError(f"Document not found: {doc_id}")

        return {
            "id": doc_id,
            "deleted": True,
        }