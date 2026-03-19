class TextChunker:
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str) -> list[str]:
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += self.chunk_size - self.overlap

        return chunks