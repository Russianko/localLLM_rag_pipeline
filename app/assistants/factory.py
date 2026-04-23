from app.assistants.rag_document_assistant import RAGDocumentAssistant
from app.assistants.dummy_assistant import DummyAssistant
from app.assistants.chat_assistant import ChatAssistant


ASSISTANT_REGISTRY = {
    "rag": {
        "name": "RAG Assistant",
        "description": "Отвечает по загруженным документам через retrieval.",
        "builder": RAGDocumentAssistant,
    },
    "chat": {
        "name": "Chat Assistant",
        "description": "Универсальный ассистент без привязки к документу.",
        "builder": ChatAssistant,
    },
    "dummy": {
        "name": "Dummy Assistant",
        "description": "Тестовый ассистент для проверки UI и маршрутизации.",
        "builder": DummyAssistant,
    },
}


def build_assistant(assistant_type: str = "rag"):
    config = ASSISTANT_REGISTRY.get(assistant_type)

    if not config:
        raise ValueError(f"Unknown assistant type: {assistant_type}")

    return config["builder"]()


def list_assistants() -> list[dict]:
    assistants = [
        {
            "type": "auto",
            "name": "Auto",
            "description": "Автоматический выбор агента по контексту.",
        }
    ]

    assistants.extend(
        {
            "type": key,
            "name": value["name"],
            "description": value["description"],
        }
        for key, value in ASSISTANT_REGISTRY.items()
    )

    return assistants