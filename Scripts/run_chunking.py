from pathlib import Path

from app.chunker import TextChunker


def main():
    clean_text_path = Path("data/extracted/sample_clean.txt")
    output_chunks_path = Path("data/extracted/sample_chunks.txt")

    if not clean_text_path.exists():
        raise FileNotFoundError(f"File not found: {clean_text_path}")

    text = clean_text_path.read_text(encoding="utf-8")

    chunker = TextChunker(chunk_size=500, overlap=100)
    chunks = chunker.chunk_text(text)

    output_chunks_path.parent.mkdir(parents=True, exist_ok=True)

    with output_chunks_path.open("w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks, start=1):
            f.write(f"===== CHUNK {i} =====\n")
            f.write(chunk)
            f.write("\n\n")

    print(f"Chunking completed successfully.")
    print(f"Total chunks: {len(chunks)}")
    print(f"Saved to: {output_chunks_path}")

    if chunks:
        print("\nFirst chunk preview:\n")
        print(chunks[0][:1000])


if __name__ == "__main__":
    main()