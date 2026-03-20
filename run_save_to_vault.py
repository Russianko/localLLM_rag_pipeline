from app.vault_manager import VaultManager

VAULT_PATH = "local_brain/obsidian_vault"


def main():
    vault = VaultManager(VAULT_PATH)
    vault.setup_vault_structure()

    question = "Какая основная цель проекта?"
    answer = (
        "Основная цель проекта - построить локальный RAG pipeline для работы с документами: "
        "извлекать текст, структурировать знания, выполнять semantic search, генерировать ответы "
        "и сохранять результаты в Obsidian vault."
    )

    used_chunks = [
        {
            "chunk_id": 1,
            "score": 0.91,
            "text": "Цель проекта: извлекать текст из документов, структурировать знания, выполнять semantic search, отвечать на вопросы через RAG и сохранять результаты в Obsidian vault."
        },
        {
            "chunk_id": 2,
            "score": 0.87,
            "text": "Проект используется как pet-project"
        },
    ]

    saved_path = vault.save_rag_answer(
        question=question,
        answer=answer,
        used_chunks=used_chunks,
        source_document="PROJECT_CONTEXT.md",
    )

    print(f"RAG answer saved to: {saved_path.resolve()}")


if __name__ == "__main__":
    main()