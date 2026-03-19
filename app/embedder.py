from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

    def embed_text(self, text: str) -> list[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()

    def embed_chunks(self, chunks: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(chunks)
        return [e.tolist() for e in embeddings]