from pathlib import Path
from app.repositories import ProcessedDocumentRepository
from app.chunker import TextChunker
from app.config import build_note_title, build_pdf_path, build_raw_text_path
from app.pdf_reader import PDFReader
from app.storage import DocumentStorage
from app.summarizer import Summarizer
from app.text_cleaner import TextCleaner
from app.vault_manager import VaultManager
from app.errors import DocumentNotFoundError, InvalidRequestError


class DocumentPipeline:
    def __init__(
            self,
            reader: PDFReader,
            cleaner: TextCleaner,
            summarizer: Summarizer,
            vault: VaultManager,
            storage: DocumentStorage,
            embedder_provider,
            repository: ProcessedDocumentRepository,
    ):
        self.reader = reader
        self.cleaner = cleaner
        self.summarizer = summarizer
        self.vault = vault
        self.storage = storage
        self.embedder_provider = embedder_provider
        self.repository = repository

    def process(
            self,
            filename: str,
            summary_limit: int = 4000,
            chunk_size: int = 500,
            overlap: int = 100,
            force_rebuild: bool = False,
    ) -> dict:
        try:
            pdf_path = build_pdf_path(filename)
            raw_output_path = build_raw_text_path(filename)

            if not pdf_path.exists():
                raise DocumentNotFoundError(f"PDF file not found: {pdf_path}")

            raw_output_path.parent.mkdir(parents=True, exist_ok=True)

            raw_text = self.reader.extract_text(pdf_path)
            if not raw_text or not raw_text.strip():
                raise InvalidRequestError("Не удалось извлечь текст из PDF.")

            raw_output_path.write_text(raw_text, encoding="utf-8")

            clean_text = self.cleaner.clean(raw_text)
            if not clean_text or not clean_text.strip():
                raise InvalidRequestError("После очистки текст пустой.")

            summary_data = self._build_summary(clean_text, summary_limit)
            vector_data = self._build_vectors(
                filename=filename,
                clean_text=clean_text,
                chunk_size=chunk_size,
                overlap=overlap,
                force_rebuild=force_rebuild,
            )

            processed_doc = self.repository.save(
                doc_id=filename,
                clean_text=clean_text,
                summary=summary_data["summary"],
                key_points=summary_data["key_points"],
                action_items=summary_data["action_items"],
                chunks=vector_data["chunks"],
                embeddings=vector_data["embeddings"],
            )

            self.storage.delete_error(filename)

            document_note_path = self.vault.save_document_note(
                title=build_note_title(filename),
                source=filename,
                summary=summary_data["summary"],
                key_points=summary_data["key_points"],
                action_items=summary_data["action_items"],
            )

            return {
                "status": "processed",
                "source_document": filename,
                "summary": processed_doc.summary,
                "key_points": processed_doc.key_points,
                "action_items": processed_doc.action_items,
                "document_note_path": str(Path(document_note_path).resolve()),
                "raw_text_path": str(raw_output_path.resolve()),
                "clean_text_path": processed_doc.clean_text_path,
                "summary_path": processed_doc.summary_path,
                "chunks_path": processed_doc.chunks_path,
                "embeddings_path": processed_doc.embeddings_path,
                "chunks_count": processed_doc.chunks_count,
            }

        except Exception as e:
            self.storage.save_error(filename, str(e))
            raise

    def _build_summary(self, clean_text: str, summary_limit: int) -> dict:
        text = clean_text[:summary_limit]

        summary = self.summarizer.generate_summary(text)
        key_points = self._normalize_list(self.summarizer.extract_key_points(text))
        action_items = self._normalize_list(self.summarizer.extract_action_items(text))

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

        should_rebuild = (
                force_rebuild
                or not chunks_path.exists()
                or not embeddings_path.exists()
        )

        if should_rebuild:
            chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)
            chunks = chunker.chunk_text(clean_text)

            if not chunks:
                raise InvalidRequestError("Не удалось создать чанки.")

            embedder = self.embedder_provider()
            embeddings = embedder.embed_chunks(chunks)
        else:
            chunks = self.storage.load_chunks(filename)
            embeddings = self.storage.load_embeddings(filename)

        return {
            "chunks": chunks,
            "embeddings": embeddings,
        }

    @staticmethod
    def _normalize_list(value) -> list[str]:
        if isinstance(value, list):
            return [str(x).strip() for x in value if str(x).strip()]
        if value is None:
            return []
        text = str(value).strip()
        return [text] if text else []