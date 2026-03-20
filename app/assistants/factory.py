from app.assistants.rag_document_assistant import RAGDocumentAssistant
from app.assistants.dummy_assistant import DummyAssistant


def build_assistant(assistant_type: str = "rag"):
    normalized_type = assistant_type.strip().lower()

    if normalized_type == "rag":
        return RAGDocumentAssistant()

    if normalized_type == "dummy":
        return DummyAssistant()

    raise ValueError(f"Unknown assistant type: {assistant_type}")