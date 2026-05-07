from app.assistants.base import BaseAssistant
from app.config import (
    LM_STUDIO_BASE_URL,
    CHAT_MODEL,
    EMBEDDING_MODEL,
    DATA_DIR,
    OBSIDIAN_VAULT_DIR,
    DEV_FAST_MODE,
    DEFAULT_SUMMARY_LIMIT,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_OVERLAP,
    DEFAULT_TOP_K,
    DEFAULT_RESPONSE_MODE,
)
from app.llm_client import LLMClient
from app.memory_store import chat_history
from pathlib import Path
from app.tools.localization_tool import LocalizationTool


class ChatAssistant(BaseAssistant):
    def __init__(self):
        self.llm = None

    def _get_llm(self) -> LLMClient:
        if self.llm is None:
            self.llm = LLMClient()
        return self.llm

    def health(self) -> dict:
        processed_dir = DATA_DIR / "processed"
        vault_dir = OBSIDIAN_VAULT_DIR

        processed_documents_count = 0
        if processed_dir.exists() and processed_dir.is_dir():
            processed_documents_count = len(
                [p for p in processed_dir.iterdir() if p.is_dir()]
            )

        client = self._get_llm()
        llm_reachable, llm_error = client.is_reachable()

        status = "ok" if llm_reachable else "degraded"

        return {
            "status": status,
            "service": "local-chat-assistant",
            "assistant_type": "chat",
            "dev_fast_mode": DEV_FAST_MODE,
            "base_url": LM_STUDIO_BASE_URL,
            "chat_model": CHAT_MODEL,
            "embedding_model": EMBEDDING_MODEL,
            "defaults": {
                "summary_limit": DEFAULT_SUMMARY_LIMIT,
                "chunk_size": DEFAULT_CHUNK_SIZE,
                "overlap": DEFAULT_OVERLAP,
                "top_k": DEFAULT_TOP_K,
                "response_mode": DEFAULT_RESPONSE_MODE,
            },
            "storage": {
                "vault_dir": str(vault_dir.resolve()),
                "vault_dir_exists": vault_dir.exists(),
                "processed_data_dir": str(processed_dir.resolve()),
                "processed_data_dir_exists": processed_dir.exists(),
                "processed_documents_count": processed_documents_count,
            },
            "runtime": {
                "embedder_loaded": False,
                "rag_loaded": False,
            },
            "llm_connection": {
                "reachable": llm_reachable,
                "error": llm_error,
            },
        }

    def process_document(
        self,
        filename: str,
        summary_limit: int = 4000,
        chunk_size: int = 500,
        overlap: int = 100,
        force_rebuild: bool = False,
    ) -> dict:
        return {
            "status": "skipped",
            "assistant_type": "chat",
            "filename": filename,
            "message": "ChatAssistant does not process documents.",
        }

    def ask(
        self,
        question: str,
        filename: str | None = None,
        session_id: str = "default",
        top_k: int = 3,
        chunk_size: int = 500,
        overlap: int = 100,
        auto_process: bool = True,
        response_mode: str = "detailed",
    ) -> dict:
        system_prompt = (
            "You are a helpful local AI coding and general-purpose assistant. "
            "You MUST use the previous conversation messages as memory. "
            "If the user asks about information they told you earlier in this session, "
            "answer from the conversation history. "
            "Do not confuse your identity with the user's identity. "
            "Answer clearly, practically, and with good structure. "
            "If the user asks for code, provide usable code."
        )

        question_lower = question.lower()

        if any(word in question_lower for word in [
            "локализация",
            "локализуй",
            "figma",
            "фигма",
            "plugin actions",
            "figma actions",
        ]):
            tool = LocalizationTool()

            base_dir = Path(__file__).resolve().parents[2]

            xlsx_path = base_dir / "data" / "input" / "March 2026.xlsx"
            mapping_path = base_dir / "config" / "mapping.json"
            rules_path = base_dir / "config" / "layout_rules.json"
            output_path = base_dir / "data" / "output" / "figma_plugin_actions.json"

            result = tool.execute(
                xlsx_path=str(xlsx_path),
                mapping_path=str(mapping_path),
                rules_path=str(rules_path),
                output_path=str(output_path),
            )

            data = result.data or {}
            summary = data.get("summary", {})

            if result.success:
                answer = (
                    "Localization tool completed.\n\n"
                    f"Frames: {summary.get('total_frames')}\n"
                    f"Nodes: {summary.get('total_nodes')}\n"
                    f"Actions: {summary.get('total_actions')}\n"
                    f"Output: {data.get('output_path')}\n\n"
                    "Figma plugin can now fetch actions from /bridge/figma/actions."
                )
            else:
                answer = (
                    "Localization tool failed.\n\n"
                    f"Error: {result.message}\n"
                    f"Data: {data}"
                )

            return {
                "source_document": filename or "",
                "question": question,
                "answer": answer,
                "rag_note_path": "",
                "top_chunks": [],
            }

        if response_mode == "short":
            system_prompt += " Keep answers concise."
        else:
            system_prompt += " Give a reasonably detailed answer."

        history = chat_history.to_llm_messages(session_id)

        messages = [
            {"role": "system", "content": system_prompt},
            *history,
            {"role": "user", "content": question},
        ]

        answer = self._get_llm().ask_with_messages(
            messages=messages,
            model=CHAT_MODEL,
            temperature=0.3,
        )

        chat_history.add_user_message(session_id, question)
        chat_history.add_assistant_message(session_id, answer)

        return {
            "source_document": filename or "",
            "question": question,
            "answer": answer,
            "rag_note_path": "",
            "top_chunks": [],
        }