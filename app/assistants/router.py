from typing import Optional


DEFAULT_ASSISTANT = "chat"


def select_assistant(
    question: str,
    filename: Optional[str] = None,
    forced_assistant: str = "auto",
) -> str:
    if forced_assistant != "auto":
        return forced_assistant

    question_lower = (question or "").strip().lower()

    # Пока очень простой rule-based router.
    # Потом можно расширить или заменить на LLM-router.
    if filename:
        return "rag"

    if any(word in question_lower for word in ["документ", "договор", "pdf", "файл"]):
        return "rag"

    return DEFAULT_ASSISTANT