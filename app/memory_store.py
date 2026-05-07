from collections import defaultdict
from datetime import datetime, timezone
from typing import Literal


Role = Literal["user", "assistant", "system"]


class InMemoryChatHistory:
    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.sessions: dict[str, list[dict[str, str]]] = defaultdict(list)

    def get(self, session_id: str) -> list[dict[str, str]]:
        return self.sessions[session_id][-self.max_messages:]

    def add_user_message(self, session_id: str, content: str) -> None:
        self._add(session_id, "user", content)

    def add_assistant_message(self, session_id: str, content: str) -> None:
        self._add(session_id, "assistant", content)

    def add_system_message(self, session_id: str, content: str) -> None:
        self._add(session_id, "system", content)

    def reset(self, session_id: str) -> None:
        self.sessions.pop(session_id, None)

    def get_status(self, session_id: str) -> dict:
        messages = self.sessions.get(session_id, [])

        return {
            "session_id": session_id,
            "messages_count": len(messages),
            "max_messages": self.max_messages,
            "has_memory": len(messages) > 0,
        }

    def _add(self, session_id: str, role: Role, content: str) -> None:
        if not content:
            return

        self.sessions[session_id].append(
            {
                "role": role,
                "content": content,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )

        self.sessions[session_id] = self.sessions[session_id][-self.max_messages:]

    def to_llm_messages(self, session_id: str) -> list[dict[str, str]]:
        messages = self.get(session_id)

        return [
            {
                "role": item["role"],
                "content": item["content"],
            }
            for item in messages
            if item["role"] in {"user", "assistant", "system"}
        ]


chat_history = InMemoryChatHistory(max_messages=20)