from pathlib import Path

from app.chunker import TextChunker
from app.embedder import Embedder
from app.rag_answerer import RAGAnswerer


def main():
    clean_text_path = Path("data/extracted/sample_clean.txt")

    if not clean_text_path.exists():
        raise FileNotFoundError(f"File not found: {clean_text_path}")

    text = clean_text_path.read_text(encoding="utf-8")

    chunker = TextChunker(chunk_size=500, overlap=100)
    chunks = chunker.chunk_text(text)

    embedder = Embedder()
    chunk_embeddings = embedder.embed_chunks(chunks)

    question = "Где в документе говорится о сокращении штата специалистов?"

    rag = RAGAnswerer()
    result = rag.answer_question(
        question=question,
        chunks=chunks,
        chunk_embeddings=chunk_embeddings,
        top_k=3,
    )

    print(f"\nQUESTION:\n{question}\n")
    print("ANSWER:\n")
    print(result["answer"])

    print("\nTOP CHUNKS USED:\n")
    for i, item in enumerate(result["top_chunks"], start=1):
        print(f"===== CHUNK {i} | score={item['score']:.4f} =====")
        print(item["chunk"][:700])
        print("\n")


if __name__ == "__main__":
    main()