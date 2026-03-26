from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.storage import DocumentStorage


@dataclass
class ProcessedDocument:
    doc_id: str
    summary: str | None
    key_points: list[str]
    action_items: list[str]
    chunks: list[str]
    embeddings: list[Any]
    clean_text_path: str | None
    summary_path: str | None
    chunks_path: str | None
    embeddings_path: str | None

    @property
    def chunks_count(self) -> int:
        return len(self.chunks)


class ProcessedDocumentRepository:
    def __init__(self, storage: DocumentStorage):
        self.storage = storage

    def exists(self, doc_id: str) -> bool:
        return self.storage.has_processed_data(doc_id)

    def load(self, doc_id: str) -> ProcessedDocument:
        summary = None
        key_points: list[str] = []
        action_items: list[str] = []
        chunks: list[str] = []
        embeddings: list[Any] = []

        summary_path = self.storage.get_summary_path(doc_id)
        chunks_path = self.storage.get_chunks_path(doc_id)
        embeddings_path = self.storage.get_embeddings_path(doc_id)
        clean_text_path = self.storage.get_clean_text_path(doc_id)

        if summary_path.exists():
            summary_data = self.storage.load_summary(doc_id)
            summary = summary_data.get("summary")
            key_points = summary_data.get("key_points", []) or []
            action_items = summary_data.get("action_items", []) or []

        if chunks_path.exists():
            chunks = self.storage.load_chunks(doc_id)

        if embeddings_path.exists():
            embeddings = self.storage.load_embeddings(doc_id)

        return ProcessedDocument(
            doc_id=doc_id,
            summary=summary,
            key_points=key_points,
            action_items=action_items,
            chunks=chunks,
            embeddings=embeddings,
            clean_text_path=str(clean_text_path.resolve()) if clean_text_path.exists() else None,
            summary_path=str(summary_path.resolve()) if summary_path.exists() else None,
            chunks_path=str(chunks_path.resolve()) if chunks_path.exists() else None,
            embeddings_path=str(embeddings_path.resolve()) if embeddings_path.exists() else None,
        )

    def save(
        self,
        doc_id: str,
        clean_text: str,
        summary: str,
        key_points: list[str],
        action_items: list[str],
        chunks: list[str],
        embeddings: list[Any],
    ) -> ProcessedDocument:
        self.storage.save_clean_text(doc_id, clean_text)
        self.storage.save_summary(
            filename=doc_id,
            summary=summary,
            key_points=key_points,
            action_items=action_items,
        )
        self.storage.save_chunks(doc_id, chunks)
        self.storage.save_embeddings(doc_id, embeddings)

        return self.load(doc_id)

    def get_status(self, doc_id: str) -> dict:
        summary_path = self.storage.get_summary_path(doc_id)
        chunks_path = self.storage.get_chunks_path(doc_id)
        embeddings_path = self.storage.get_embeddings_path(doc_id)
        clean_text_path = self.storage.get_clean_text_path(doc_id)
        error_path = self.storage.base_dir / doc_id / "error.json"

        has_clean = clean_text_path.exists()
        has_summary = summary_path.exists()
        has_chunks = chunks_path.exists()
        has_embeddings = embeddings_path.exists()
        has_error = error_path.exists()

        if has_error:
            status = DocumentStatus.FAILED
        elif has_chunks and has_embeddings:
            status = DocumentStatus.PROCESSED
        elif has_clean or has_summary:
            status = DocumentStatus.PARTIAL
        else:
            status = DocumentStatus.NOT_PROCESSED

        return {
            "id": doc_id,
            "status": status.value,
            "has_clean_text": has_clean,
            "has_summary": has_summary,
            "has_chunks": has_chunks,
            "has_embeddings": has_embeddings,
            "is_processed": status == DocumentStatus.PROCESSED,
            "has_error": has_error,
        }

    def delete(self, doc_id: str) -> bool:
        return self.storage.delete_document(doc_id)

    def list_statuses(self) -> list[dict]:
        result = []
        for doc_id in self.storage.list_documents():
            result.append(self.get_status(doc_id))
        return result