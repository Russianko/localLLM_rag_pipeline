from app.config import CHAT_MODEL
from app.llm_client import LLMClient
from app.retriever import Retriever
from app.prompts import build_general_rag_prompt, build_specific_rag_prompt


class RAGAnswerer:
    def __init__(self, embedder, retriever=None, llm=None):
        self.embedder = embedder
        self.retriever = retriever if retriever is not None else Retriever()
        self.llm = llm if llm is not None else LLMClient()

    def build_context(self, top_chunks: list[dict]) -> str:
        context_parts = []

        for i, item in enumerate(top_chunks, start=1):
            context_parts.append(f"Источник {i} (score={item['score']:.4f}):")
            context_parts.append(item["chunk"])
            context_parts.append("")

        return "\n".join(context_parts)

    def is_general_question(self, question: str) -> bool:
        question_lower = question.strip().lower()

        general_patterns = [
            "о чем",
            "что это за документ",
            "что это за договор",
            "кратко опиши",
            "кратко описать",
            "опиши документ",
            "опиши договор",
            "в чем суть",
            "какие главные тезисы",
            "основные тезисы",
            "краткое резюме",
            "сделай резюме",
        ]

        return any(pattern in question_lower for pattern in general_patterns)

    def build_general_prompt(
            self,
            question: str,
            context: str,
            response_mode: str = "detailed",
    ) -> str:
        return build_general_rag_prompt(
            question=question,
            context=context,
            response_mode=response_mode,
        )

    def build_specific_prompt(
            self,
            question: str,
            context: str,
            response_mode: str = "detailed",
    ) -> str:
        return build_specific_rag_prompt(
            question=question,
            context=context,
            response_mode=response_mode,
        )

    def answer_question(
            self,
            question: str,
            chunks: list[str],
            chunk_embeddings,
            top_k: int = 3,
            response_mode: str = "detailed",
    ) -> dict:
        query_embedding = self.embedder.embed_text(question)

        top_chunks = self.retriever.find_top_k(
            query_embedding=query_embedding,
            chunk_embeddings=chunk_embeddings,
            chunks=chunks,
            top_k=top_k,
        )

        if not top_chunks:
            return {
                "answer": "В предоставленных фрагментах нет данных для ответа.",
                "top_chunks": [],
            }

        best_score = top_chunks[0]["score"]
        if best_score < 0.45:
            return {
                "answer": (
                    "В предоставленных фрагментах нет достаточно релевантных данных "
                    "для уверенного ответа. Попробуйте задать более конкретный вопрос."
                ),
                "top_chunks": top_chunks,
            }

        context = self.build_context(top_chunks)

        if self.is_general_question(question):
            prompt = self.build_general_prompt(question, context, response_mode=response_mode)
        else:
            prompt = self.build_specific_prompt(question, context, response_mode=response_mode)

        answer = self.llm.ask(prompt=prompt, model=CHAT_MODEL)

        return {
            "answer": answer,
            "top_chunks": top_chunks,
        }

    def answer_from_top_chunks(
            self,
            question: str,
            top_chunks: list[dict],
    ) -> dict:
        if not top_chunks:
            return {
                "answer": "В предоставленных фрагментах нет данных для ответа.",
                "top_chunks": [],
            }

        context = "\n\n".join(item["chunk"] for item in top_chunks)

        if self.is_general_question(question):
            prompt = self.build_general_prompt(question, context)
        else:
            prompt = self.build_specific_prompt(question, context)

        answer = self.llm.ask(prompt, model=self.chat_model)

        return {
            "answer": answer,
            "top_chunks": top_chunks,
        }