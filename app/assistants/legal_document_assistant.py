from app.assistants.rag_document_assistant import RAGDocumentAssistant
from app.config import CHAT_MODEL


LEGAL_SYSTEM_PROMPT = """
Ты локальный ассистент для анализа юридических документов.

Правила:
1. Отвечай строго по предоставленному тексту документа.
2. Не выдумывай факты, даты, обязательства и штрафы.
3. Если информации нет в документе, прямо скажи: "В документе это не указано".
4. Не давай юридическую консультацию как юрист, а анализируй текст документа.
5. Структурируй ответ понятно и практично.

Фокус анализа:
- суть документа
- стороны
- обязательства
- сроки
- риски
- штрафы
- спорные формулировки
- что требует внимания
"""


class LegalDocumentAssistant(RAGDocumentAssistant):
    def health(self) -> dict:
        data = super().health()
        data["assistant_type"] = "legal"
        data["service"] = "local-legal-document-assistant"
        return data

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
        if not filename:
            raise ValueError("Legal assistant requires filename.")

        result = self.query_pipeline.answer(
            filename=filename,
            question=question,
            top_k=top_k,
            chunk_size=chunk_size,
            overlap=overlap,
            auto_process=auto_process,
            response_mode=response_mode,
        )

        return result