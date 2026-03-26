from pathlib import Path
from app.repositories import ProcessedDocumentRepository
from app.config import build_pdf_path
from app.storage import DocumentStorage
from app.vault_manager import VaultManager
from app.errors import DocumentNotFoundError, DocumentNotProcessedError



class RAGQueryPipeline:
    def __init__(
            self,
            storage: DocumentStorage,
            vault: VaultManager,
            rag_provider,
            process_document_callback,
            repository: ProcessedDocumentRepository,
    ):
        self.storage = storage
        self.vault = vault
        self.rag_provider = rag_provider
        self.process_document_callback = process_document_callback
        self.repository = repository

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

        if self.repository.exists(filename):
            processed_doc = self.repository.load(filename)
            chunks = processed_doc.chunks
            chunk_embeddings = processed_doc.embeddings
        else:
            if not auto_process:
                raise DocumentNotProcessedError(
                    "Документ ещё не обработан. Сначала вызови /process или включи auto_process."
                )

            self.process_document_callback(
                filename=filename,
                chunk_size=chunk_size,
                overlap=overlap,
            )

            processed_doc = self.repository.load(filename)
            chunks = processed_doc.chunks
            chunk_embeddings = processed_doc.embeddings

            if not chunks:
                raise DocumentNotProcessedError(
                    "После обработки не удалось загрузить чанки документа."
                )

        rag = self.rag_provider()
        result = rag.answer_question(
            question=question,
            chunks=chunks,
            chunk_embeddings=chunk_embeddings,
            top_k=top_k,
            response_mode=response_mode,
        )

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
            normalized.append(
                {
                    "chunk_id": i,
                    "text": item["chunk"],
                    "score": float(item["score"]),
                }
            )

        return normalized