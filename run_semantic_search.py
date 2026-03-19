from pathlib import Path

from app.chunker import TextChunker
from app.embedder import Embedder
from app.retriever import Retriever


def main():
    clean_text_path = Path("data/extracted/sample_clean.txt")

    if not clean_text_path.exists():
        raise FileNotFoundError(f"File not found: {clean_text_path}")

    text = clean_text_path.read_text(encoding="utf-8")

    chunker = TextChunker(chunk_size=500, overlap=100)
    chunks = chunker.chunk_text(text)

    embedder = Embedder()
    retriever = Retriever()

    chunk_embeddings = embedder.embed_chunks(chunks)

    question = "Где в документе говорится о сокращении штата специалистов"
    query_embedding = embedder.embed_text(question)

    top_chunks = retriever.find_top_k(
        query_embedding=query_embedding,
        chunk_embeddings=chunk_embeddings,
        chunks=chunks,
        top_k=3,
    )

    print(f"Question: {question}\n")
    print("Top relevant chunks:\n")

    for i, item in enumerate(top_chunks, start=1):
        print(f"===== RESULT {i} =====")
        print(f"Score: {item['score']:.4f}")
        print(item["chunk"][:700])
        print("\n")


if __name__ == "__main__":
    main()