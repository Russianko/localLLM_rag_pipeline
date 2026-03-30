from pathlib import Path

import chromadb

from app.vectorstore.base import BaseVectorStore


class ChromaStore(BaseVectorStore):
    def __init__(self, persist_dir: str | Path, collection_name: str):
        self.persist_dir = str(persist_dir)
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def upsert_document_chunks(
        self,
        doc_id: str,
        chunks: list[str],
        embeddings: list[list[float]],
    ) -> None:
        ids = [f"{doc_id}:{i}" for i in range(len(chunks))]
        metadatas = [{"doc_id": doc_id, "chunk_id": i} for i in range(len(chunks))]

        self.collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int,
        doc_id: str | None = None,
    ) -> list[dict]:
        where = {"doc_id": doc_id} if doc_id else None

        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
        )

        ids = result.get("ids", [[]])[0]
        documents = result.get("documents", [[]])[0]
        distances = result.get("distances", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]

        items: list[dict] = []
        for idx, text in enumerate(documents):
            distance = distances[idx] if idx < len(distances) else None
            metadata = metadatas[idx] if idx < len(metadatas) else {}

            items.append(
                {
                    "id": ids[idx],
                    "chunk": text,
                    "score": self._distance_to_score(distance),
                    "distance": distance,
                    "metadata": metadata,
                }
            )

        return items

    def delete_document(self, doc_id: str) -> None:
        self.collection.delete(where={"doc_id": doc_id})

    @staticmethod
    def _distance_to_score(distance: float | None) -> float:
        if distance is None:
            return 0.0

        # Чем меньше distance, тем лучше. Преобразуем в "чем больше, тем лучше".
        return 1.0 / (1.0 + max(distance, 0.0))