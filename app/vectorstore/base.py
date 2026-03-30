from abc import ABC, abstractmethod


class BaseVectorStore(ABC):
    @abstractmethod
    def upsert_document_chunks(
        self,
        doc_id: str,
        chunks: list[str],
        embeddings: list[list[float]],
    ) -> None:
        pass

    @abstractmethod
    def search(
        self,
        query_embedding: list[float],
        top_k: int,
        doc_id: str | None = None,
    ) -> list[dict]:
        pass

    @abstractmethod
    def delete_document(self, doc_id: str) -> None:
        pass