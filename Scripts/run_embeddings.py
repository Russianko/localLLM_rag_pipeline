from pathlib import Path

from app.chunker import TextChunker
from app.embedder import Embedder


def main():
    clean_text_path = Path("data/extracted/sample_clean.txt")

    if not clean_text_path.exists():
        raise FileNotFoundError(f"File not found: {clean_text_path}")

    text = clean_text_path.read_text(encoding="utf-8")

    chunker = TextChunker(chunk_size=500, overlap=100)
    chunks = chunker.chunk_text(text)

    embedder = Embedder()
    embeddings = embedder.embed_chunks(chunks)

    print(f"Total chunks: {len(chunks)}")
    print(f"Embedding dimension: {len(embeddings[0])}")

    print("\nFirst chunk preview:")
    print(chunks[0][:300])

    print("\nFirst embedding (first 10 values):")
    print(embeddings[0][:10])


if __name__ == "__main__":
    main()