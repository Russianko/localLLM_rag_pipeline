from app.config import EMBEDDING_MODEL


class Embedder:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or EMBEDDING_MODEL
        self.model = None

    def _get_model(self):
        if self.model is None:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(
                self.model_name,
                trust_remote_code=True,
            )
        return self.model

    def embed_text(self, text: str) -> list[float]:
        model = self._get_model()
        embedding = model.encode(text)
        return embedding.tolist()

    def embed_chunks(self, chunks: list[str]) -> list[list[float]]:
        model = self._get_model()
        embeddings = model.encode(chunks)
        return [e.tolist() for e in embeddings]