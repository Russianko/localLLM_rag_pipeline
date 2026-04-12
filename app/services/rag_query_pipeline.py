from pathlib import Path
import logging

from app.config import build_pdf_path, RAG_SCORE_THRESHOLD
from app.storage import DocumentStorage
from app.vault_manager import VaultManager
from app.errors import DocumentNotFoundError, DocumentNotProcessedError


logger = logging.getLogger(__name__)


class RAGQueryPipeline:
    def __init__(
        self,
        storage: DocumentStorage,
        vault: VaultManager,
        rag_provider,
        process_document_callback,
        vector_store_provider,
    ):
        self.storage = storage
        self.vault = vault
        self.rag_provider = rag_provider
        self.process_document_callback = process_document_callback
        self.vector_store_provider = vector_store_provider

    def answer(
        self,
        filename: str,
        question: str,
        top_k: int = 3,
        chunk_size: int = 500,
        overlap: int = 100,
        auto_process: bool = True,
        response_mode: str = "detailed",
    ) -> dict:
        pdf_path = build_pdf_path(filename)

        if not pdf_path.exists():
            raise DocumentNotFoundError(f"PDF file not found: {pdf_path}")

        if not self.storage.has_processed_data(filename):
            if not auto_process:
                raise DocumentNotProcessedError(
                    "Документ ещё не обработан. Сначала вызови /process или включи auto_process."
                )

            self.process_document_callback(
                filename=filename,
                summary_limit=None,
                chunk_size=chunk_size,
                overlap=overlap,
                force_rebuild=False,
            )

        logger.info("ASK STEP 1: pdf exists / processed check passed")

        doc_id = Path(filename).stem
        rag = self.rag_provider()
        vector_store = self.vector_store_provider()

        logger.info("ASK STEP 2: rag provider and vector store ready")

        query_embedding = rag.embedder.embed_text(question)
        logger.info("ASK STEP 3: query embedding built")

        top_chunks = vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            doc_id=doc_id,
        )
        logger.info("ASK STEP 4: vector search done")

        if not top_chunks:
            result = {
                "answer": "В предоставленных фрагментах нет данных для ответа.",
                "top_chunks": [],
            }
        else:
            best_score = float(top_chunks[0]["score"])

            if best_score < RAG_SCORE_THRESHOLD:
                result = {
                    "answer": (
                        "В предоставленных фрагментах нет достаточно релевантных данных "
                        "для уверенного ответа. Попробуйте задать более конкретный вопрос."
                    ),
                    "top_chunks": top_chunks,
                }
            else:
                result = rag.answer_from_top_chunks(
                    question=question,
                    top_chunks=top_chunks,
                    response_mode=response_mode,
                )
                logger.info("ASK STEP 5: llm answer received")

        normalized_chunks = self._normalize_chunks(result.get("top_chunks", []))

        rag_note_path = self.vault.save_rag_answer(
            question=question,
            answer=result["answer"],
            used_chunks=normalized_chunks,
            source_document=filename,
        )

        return {
            "source_document": filename,
            "question": question,
            "answer": result["answer"],
            "rag_note_path": str(Path(rag_note_path).resolve()),
            "top_chunks": normalized_chunks,
        }

    @staticmethod
    def _normalize_chunks(top_chunks: list[dict]) -> list[dict]:
        normalized = []

        for i, item in enumerate(top_chunks):
            metadata = item.get("metadata", {}) or {}
            chunk_id = metadata.get("chunk_id", i)

            normalized.append(
                {
                    "chunk_id": int(chunk_id),
                    "text": item["chunk"],
                    "score": float(item["score"]),
                }
            )

        return normalized