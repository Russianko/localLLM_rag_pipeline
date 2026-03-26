from app.assistants.base import BaseAssistant
from app.config import (
    BASE_URL,
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
from app.embedder import Embedder
from app.pdf_reader import PDFReader
from app.rag_answerer import RAGAnswerer
from app.services.document_pipeline import DocumentPipeline
from app.services.rag_query_pipeline import RAGQueryPipeline
from app.storage import DocumentStorage
from app.summarizer import Summarizer
from app.text_cleaner import TextCleaner
from app.vault_manager import VaultManager
from app.repositories import ProcessedDocumentRepository
from app.llm_client import LLMClient

from pathlib import Path


class RAGDocumentAssistant(BaseAssistant):
    def __init__(self):
        self.reader = PDFReader()
        self.cleaner = TextCleaner()
        self.summarizer = Summarizer()

        self.embedder = None
        self.rag = None

        self.vault = VaultManager(OBSIDIAN_VAULT_DIR)
        self.storage = DocumentStorage(DATA_DIR / "processed")
        self.repository = ProcessedDocumentRepository(self.storage)

        self.document_pipeline = DocumentPipeline(
            reader=self.reader,
            cleaner=self.cleaner,
            summarizer=self.summarizer,
            vault=self.vault,
            storage=self.storage,
            embedder_provider=self._get_embedder,
            repository=self.repository,
        )

        self.query_pipeline = RAGQueryPipeline(
            storage=self.storage,
            vault=self.vault,
            rag_provider=self._get_rag,
            process_document_callback=self.process_document,
            repository=self.repository,
        )

    def _get_embedder(self) -> Embedder:
        if self.embedder is None:
            self.embedder = Embedder()
        return self.embedder

    def _get_rag(self) -> RAGAnswerer:
        if self.rag is None:
            self.rag = RAGAnswerer(embedder=self._get_embedder())
        return self.rag

    def health(self) -> dict:
        processed_dir = DATA_DIR / "processed"
        vault_dir = OBSIDIAN_VAULT_DIR

        processed_documents_count = 0
        if processed_dir.exists() and processed_dir.is_dir():
            processed_documents_count = len(
                [p for p in processed_dir.iterdir() if p.is_dir()]
            )

        llm_reachable = False
        llm_error = None

        try:
            client = LLMClient()
            client.get_models()
            llm_reachable = True
        except Exception as e:
            llm_error = str(e)

        status = "ok" if llm_reachable else "degraded"

        return {
            "status": status,
            "service": "local-rag-assistant",
            "assistant_type": "rag",
            "dev_fast_mode": DEV_FAST_MODE,
            "base_url": BASE_URL,
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
                "embedder_loaded": self.embedder is not None,
                "rag_loaded": self.rag is not None,
            },
            "llm_connection": {
                "reachable": llm_reachable,
                "error": llm_error,
            },
        }

    def process_document(
            self,
            filename: str,
            summary_limit: int,
            chunk_size: int,
            overlap: int,
            force_rebuild: bool = False,
    ) -> dict:
        return self.document_pipeline.process(
            filename=filename,
            summary_limit=summary_limit,
            chunk_size=chunk_size,
            overlap=overlap,
            force_rebuild=force_rebuild,
        )

    def ask(
            self,
            filename: str,
            question: str,
            top_k: int,
            chunk_size: int,
            overlap: int,
            auto_process: bool = True,
            response_mode: str = "detailed",
    ) -> dict:
        return self.query_pipeline.answer(
            filename=filename,
            question=question,
            top_k=top_k,
            chunk_size=chunk_size,
            overlap=overlap,
            auto_process=auto_process,
            response_mode=response_mode,
        )   