from app.assistants.base import BaseAssistant
from app.config import (
    BASE_URL,
    CHAT_MODEL,
    EMBEDDING_MODEL,
    DATA_DIR,
    OBSIDIAN_VAULT_DIR,
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


class RAGDocumentAssistant(BaseAssistant):
    def __init__(self):
        self.reader = PDFReader()
        self.cleaner = TextCleaner()
        self.summarizer = Summarizer()

        self.embedder = None
        self.rag = None

        self.vault = VaultManager(OBSIDIAN_VAULT_DIR)
        self.storage = DocumentStorage(DATA_DIR / "processed")

        self.document_pipeline = DocumentPipeline(
            reader=self.reader,
            cleaner=self.cleaner,
            summarizer=self.summarizer,
            vault=self.vault,
            storage=self.storage,
            embedder_provider=self._get_embedder,
        )

        self.query_pipeline = RAGQueryPipeline(
            storage=self.storage,
            vault=self.vault,
            rag_provider=self._get_rag,
            process_document_callback=self.process_document,
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
        return {
            "status": "ok",
            "base_url": BASE_URL,
            "chat_model": CHAT_MODEL,
            "embedding_model": EMBEDDING_MODEL,
            "vault_dir": str(OBSIDIAN_VAULT_DIR.resolve()),
            "processed_data_dir": str((DATA_DIR / "processed").resolve()),
            "assistant_type": "rag",
            "embedder_loaded": self.embedder is not None,
            "rag_loaded": self.rag is not None,
        }

    def process_document(
        self,
        filename: str,
        summary_limit: int = 4000,
        chunk_size: int = 500,
        overlap: int = 100,
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
            top_k: int = 3,
            chunk_size: int = 500,
            overlap: int = 100,
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