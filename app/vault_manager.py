from pathlib import Path
from datetime import datetime
import re


class VaultManager:
    def __init__(self, vault_path: str | Path):
        self.vault_path = Path(vault_path)

        self.projects_path = self.vault_path / "Projects"
        self.areas_path = self.vault_path / "Areas"
        self.resources_path = self.vault_path / "Resources"
        self.archive_path = self.vault_path / "Archive"
        self.inbox_path = self.vault_path / "Inbox"

        self.documents_path = self.resources_path / "Documents"
        self.rag_answers_path = self.resources_path / "RAG Answers"

    def setup_vault_structure(self) -> None:
        folders = [
            self.projects_path,
            self.areas_path,
            self.resources_path,
            self.archive_path,
            self.inbox_path,
            self.documents_path,
            self.rag_answers_path,
        ]

        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)

    def save_document_note(
        self,
        title: str,
        source: str,
        summary: str,
        key_points: list[str],
        action_items: list[str],
    ) -> Path:
        self.setup_vault_structure()

        created_at = self._current_timestamp()
        safe_title = self._slugify(title)
        note_path = self.documents_path / f"{safe_title}.md"

        content = self._build_document_note_markdown(
            title=title,
            source=source,
            summary=summary,
            key_points=key_points,
            action_items=action_items,
            created_at=created_at,
        )

        note_path.write_text(content, encoding="utf-8")
        return note_path

    def save_rag_answer(
        self,
        question: str,
        answer: str,
        used_chunks: list[dict],
        source_document: str | None = None,
    ) -> Path:
        self.setup_vault_structure()

        created_at = self._current_timestamp()
        safe_question = self._slugify(question)[:80]
        filename = f"{created_at.replace(':', '-').replace(' ', '_')}__{safe_question}.md"
        note_path = self.rag_answers_path / filename

        content = self._build_rag_answer_markdown(
            question=question,
            answer=answer,
            used_chunks=used_chunks,
            created_at=created_at,
            source_document=source_document,
        )

        note_path.write_text(content, encoding="utf-8")

        self._append_rag_link_to_document_note(
            source_document=source_document,
            rag_note_path=note_path,
            question=question,
        )

        return note_path

    def _build_document_note_markdown(
        self,
        title: str,
        source: str,
        summary: str,
        key_points: list[str],
        action_items: list[str],
        created_at: str,
    ) -> str:
        key_points_md = self._format_bullet_list(key_points)
        action_items_md = self._format_bullet_list(action_items)
        formatted_summary = self._as_callout(summary, "summary", "Summary")

        return f"""---
type: document_note
title: "{self._escape_quotes(title)}"
source: "{self._escape_quotes(source)}"
created_at: "{created_at}"
tags:
  - document
  - knowledge
---

# {title}

## Context

- **Source:** {source}
- **Created:** {created_at}

{formatted_summary}

## Key Points

{key_points_md}

## Action Items

{action_items_md}

## Related Notes

_Add related RAG answers here._
"""

    def _build_rag_answer_markdown(
        self,
        question: str,
        answer: str,
        used_chunks: list[dict],
        created_at: str,
        source_document: str | None = None,
    ) -> str:
        chunks_md = self._format_chunks_as_details(used_chunks)

        source_lines = [f"- **Created:** {created_at}"]
        doc_note_name = ""

        if source_document:
            doc_note_name = self._document_note_name(source_document)
            source_lines.append(f"- **Source document:** {source_document}")
            source_lines.append(f"- **Linked note:** [[{doc_note_name}]]")

        context_block = "\n".join(source_lines)
        formatted_answer = self._as_callout(answer, "note", "Answer")

        return f"""---
type: rag_answer
question: "{self._escape_quotes(question)}"
created_at: "{created_at}"
source_document: "{self._escape_quotes(source_document or '')}"
document_note: "{doc_note_name}"
tags:
  - rag
  - answer
---

# RAG Answer

## Question

{question}

## Context

{context_block}

{formatted_answer}

## Evidence

{chunks_md}
"""

    def _format_bullet_list(self, items: list[str]) -> str:
        if not items:
            return "- No items found."

        return "\n".join(f"- {item}" for item in items)

    def _format_chunks_as_details(self, used_chunks: list[dict]) -> str:
        if not used_chunks:
            return "_No chunks were saved._"

        formatted = []

        for index, chunk in enumerate(used_chunks, start=1):
            chunk_id = chunk.get("chunk_id", "unknown")
            score = chunk.get("score", "n/a")
            text = str(chunk.get("text", "")).strip()

            formatted.append(
                f"""<details>
<summary>Chunk {index} | chunk_id={chunk_id} | score={score}</summary>

{text}

</details>"""
            )

        return "\n\n".join(formatted)

    def _as_callout(self, text: str, callout_type: str, title: str) -> str:
        cleaned = str(text).strip()
        lines = cleaned.splitlines() or [""]
        formatted_lines = "\n".join(f"> {line}" if line else ">" for line in lines)
        return f"> [!{callout_type}] {title}\n{formatted_lines}"

    def _slugify(self, text: str) -> str:
        text = text.strip().lower()
        text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
        text = re.sub(r"\s+", "_", text, flags=re.UNICODE)
        return text[:120] or "untitled"

    def _document_note_name(self, source_document: str) -> str:
        source_stem = Path(source_document).stem
        return self._slugify(source_stem)

    def _escape_quotes(self, text: str) -> str:
        return str(text).replace('"', '\\"')

    def _current_timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _append_rag_link_to_document_note(
            self,
            source_document: str | None,
            rag_note_path: Path,
            question: str,
    ) -> None:
        if not source_document:
            return

        doc_note_name = self._document_note_name(source_document)
        doc_note_path = self.documents_path / f"{doc_note_name}.md"

        if not doc_note_path.exists():
            return

        rag_note_name = rag_note_path.stem
        link_line = f"- [[{rag_note_name}]] — {question}"

        content = doc_note_path.read_text(encoding="utf-8")

        if link_line in content:
            return

        marker = "## Related Notes"

        if marker in content:
            if "_Add related RAG answers here._" in content:
                content = content.replace(
                    "_Add related RAG answers here._",
                    f"{link_line}"
                )
            else:
                content = content.replace(
                    marker,
                    f"{marker}\n\n{link_line}",
                    1
                )
        else:
            content += f"\n\n## Related Notes\n\n{link_line}\n"

        doc_note_path.write_text(content, encoding="utf-8")