from pathlib import Path
from app.errors import DocumentNotFoundError, InvalidRequestError
from app.chunker import TextChunker
from app.config import build_note_title, build_pdf_path, build_raw_text_path
from app.pdf_reader import PDFReader
from app.storage import DocumentStorage
from app.summarizer import Summarizer
from app.text_cleaner import TextCleaner
from app.vault_manager import VaultManager


class DocumentPipeline:
    def __init__(
        self,
        reader: PDFReader,
        cleaner: TextCleaner,
        summarizer: Summarizer,
        vault: VaultManager,
        storage: DocumentStorage,
        embedder_provider,
    ):
        self.reader = reader
        self.cleaner = cleaner
        self.summarizer = summarizer
        self.vault = vault
        self.storage = storage
        self.embedder_provider = embedder_provider

    def process(self, filename: str, summary_limit: int = 4000, chunk_size: int = 500, overlap: int = 100):
        try:
            # === 1. путь к PDF ===
            pdf_path = self.storage.get_pdf_path(filename)

            if not pdf_path.exists():
                raise DocumentNotFoundError(f"PDF file not found: {pdf_path}")

            # === 2. extract ===
            raw_text = self.pdf_reader.read(pdf_path)

            if not raw_text or not raw_text.strip():
                raise InvalidRequestError("Не удалось извлечь текст из PDF.")

            # === 3. clean ===
            clean_text = self.cleaner.clean(raw_text)

            if not clean_text or not clean_text.strip():
                raise InvalidRequestError("После очистки текст пустой.")

            # === 4. chunk ===
            chunks = self.chunker.chunk(clean_text, chunk_size=chunk_size, overlap=overlap)

            if not chunks:
                raise InvalidRequestError("Не удалось создать чанки.")

            # === 5. embeddings ===
            embeddings = self.embedder.embed(chunks)

            # === 6. summary ===
            summary = self.summarizer.summarize(clean_text[:summary_limit])

            # === 7. сохранить ===
            self.storage.save_chunks(filename, chunks)
            self.storage.save_embeddings(filename, embeddings)
            self.storage.save_summary(filename, summary)

            # ✅ УСПЕХ → удалить старую ошибку (если была)
            self.storage.delete_error(filename)

            return {
                "status": "processed",
                "chunks_count": len(chunks),
            }

        except Exception as e:
            # ❌ ОШИБКА → сохранить её
            self.storage.save_error(filename, str(e))
            raise



    def _build_summary(self, clean_text: str, summary_limit: int) -> dict:
        summary_input = clean_text[:summary_limit]

        summary = self.summarizer.generate_summary(summary_input)
        key_points = self._normalize_list(
            self.summarizer.extract_key_points(summary_input)
        )
        action_items = self._normalize_list(
            self.summarizer.extract_action_items(summary_input)
        )

        return {
            "summary": summary,
            "key_points": key_points,
            "action_items": action_items,
        }

    def _build_vectors(
        self,
        filename: str,
        clean_text: str,
        chunk_size: int,
        overlap: int,
        force_rebuild: bool,
    ) -> dict:
        chunks_path = self.storage.get_chunks_path(filename)
        embeddings_path = self.storage.get_embeddings_path(filename)

        should_rebuild_vectors = (
            force_rebuild
            or not chunks_path.exists()
            or not embeddings_path.exists()
        )

        if should_rebuild_vectors:
            chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)
            chunks = chunker.chunk_text(clean_text)

            if not chunks:
                raise InvalidRequestError("Не удалось создать чанки.")

            embedder = self.embedder_provider()
            chunk_embeddings = embedder.embed_chunks(chunks)

            chunks_path = self.storage.save_chunks(filename, chunks)
            embeddings_path = self.storage.save_embeddings(filename, chunk_embeddings)
            chunks_count = len(chunks)
        else:
            chunks = self.storage.load_chunks(filename)
            chunks_count = len(chunks)

        return {
            "chunks_path": chunks_path,
            "embeddings_path": embeddings_path,
            "chunks_count": chunks_count,
        }

    @staticmethod
    def _normalize_list(value) -> list[str]:
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if value is None:
            return []
        text = str(value).strip()
        return [text] if text else []