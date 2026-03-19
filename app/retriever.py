import math


class Retriever:
    def cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vec1, vec2))

        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def find_top_k(
        self,
        query_embedding: list[float],
        chunk_embeddings: list[list[float]],
        chunks: list[str],
        top_k: int = 3,
    ) -> list[dict]:
        scored_chunks = []

        for chunk, embedding in zip(chunks, chunk_embeddings):
            score = self.cosine_similarity(query_embedding, embedding)
            scored_chunks.append(
                {
                    "chunk": chunk,
                    "score": score,
                }
            )

        scored_chunks.sort(key=lambda x: x["score"], reverse=True)

        return scored_chunks[:top_k]