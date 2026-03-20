import json
import shutil
from pathlib import Path
from typing import Any


class DocumentStorage:
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def delete_document(self, doc_id: str) -> bool:
        doc_dir = self.base_dir / doc_id

        if not doc_dir.exists() or not doc_dir.is_dir():
            return False

        shutil.rmtree(doc_dir)
        return True

    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def get_doc_dir(self, filename: str) -> Path:
        doc_name = Path(filename).stem
        return self.base_dir / doc_name

    def ensure_doc_dir(self, filename: str) -> Path:
        doc_dir = self.get_doc_dir(filename)
        doc_dir.mkdir(parents=True, exist_ok=True)
        return doc_dir

    def get_clean_text_path(self, filename: str) -> Path:
        return self.get_doc_dir(filename) / "clean.txt"

    def get_chunks_path(self, filename: str) -> Path:
        return self.get_doc_dir(filename) / "chunks.json"

    def get_embeddings_path(self, filename: str) -> Path:
        return self.get_doc_dir(filename) / "embeddings.json"

    def get_summary_path(self, filename: str) -> Path:
        return self.get_doc_dir(filename) / "summary.json"

    def has_processed_data(self, filename: str) -> bool:
        return (
            self.get_clean_text_path(filename).exists()
            and self.get_chunks_path(filename).exists()
            and self.get_embeddings_path(filename).exists()
        )

    def save_clean_text(self, filename: str, clean_text: str) -> str:
        self.ensure_doc_dir(filename)
        path = self.get_clean_text_path(filename)
        path.write_text(clean_text, encoding="utf-8")
        return str(path.resolve())

    def load_clean_text(self, filename: str) -> str:
        path = self.get_clean_text_path(filename)
        return path.read_text(encoding="utf-8")

    def save_chunks(self, filename: str, chunks: list[str]) -> str:
        self.ensure_doc_dir(filename)
        path = self.get_chunks_path(filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)
        return str(path.resolve())

    def load_chunks(self, filename: str) -> list[str]:
        path = self.get_chunks_path(filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_embeddings(self, filename: str, embeddings: Any) -> str:
        self.ensure_doc_dir(filename)
        path = self.get_embeddings_path(filename)

        if hasattr(embeddings, "tolist"):
            serializable = embeddings.tolist()
        else:
            serializable = embeddings

        with open(path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, ensure_ascii=False)

        return str(path.resolve())

    def load_embeddings(self, filename: str) -> list[list[float]]:
        path = self.get_embeddings_path(filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_summary(
            self,
            filename: str,
            summary: str,
            key_points: list[str],
            action_items: list[str],
    ) -> str:
        self.ensure_doc_dir(filename)
        path = self.get_summary_path(filename)
        payload = {
            "summary": summary,
            "key_points": key_points,
            "action_items": action_items,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return str(path.resolve())

    def load_summary(self, filename: str) -> dict:
        path = self.get_summary_path(filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_documents(self) -> list[str]:
        if not self.base_dir.exists():
            return []

        return [
            d.name
            for d in self.base_dir.iterdir()
            if d.is_dir()
        ]