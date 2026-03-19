from app.config import CHAT_MODEL
from app.embedder import Embedder
from app.llm_client import LLMClient
from app.retriever import Retriever


class RAGAnswerer:
    def __init__(self):
        self.embedder = Embedder()
        self.retriever = Retriever()
        self.llm = LLMClient()

    def build_context(self, top_chunks: list[dict]) -> str:
        context_parts = []

        for i, item in enumerate(top_chunks, start=1):
            context_parts.append(f"Источник {i} (score={item['score']:.4f}):")
            context_parts.append(item["chunk"])
            context_parts.append("")

        return "\n".join(context_parts)

    def answer_question(
        self,
        question: str,
        chunks: list[str],
        chunk_embeddings: list[list[float]],
        top_k: int = 3,
    ) -> dict:
        query_embedding = self.embedder.embed_text(question)

        top_chunks = self.retriever.find_top_k(
            query_embedding=query_embedding,
            chunk_embeddings=chunk_embeddings,
            chunks=chunks,
            top_k=top_k,
        )

        context = self.build_context(top_chunks)

        prompt = f"""
        Ты анализируешь русский деловой документ.

        Ответь на вопрос пользователя, опираясь только на предоставленные фрагменты документа.
        Не выдумывай факты и не добавляй ничего от себя.
        Если точного ответа нет, так и напиши.

        Сначала дай краткий ответ в 2–4 предложениях.
        Потом, если возможно, укажи, в каких фрагментах это подтверждается.

        Вопрос:
        {question}

        Фрагменты документа:
        {context}

        Формат ответа:
        1. Краткий ответ
        2. Подтверждение по фрагментам
        """
        answer = self.llm.ask(prompt=prompt, model=CHAT_MODEL)

        return {
            "answer": answer,
            "top_chunks": top_chunks,
        }