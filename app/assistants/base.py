from abc import ABC, abstractmethod


class BaseAssistant(ABC):
    @abstractmethod
    def health(self) -> dict:
        pass

    @abstractmethod
    def process_document(
        self,
        filename: str,
        summary_limit: int,
        chunk_size: int,
        overlap: int,
        force_rebuild: bool = False,
    ) -> dict:
        pass

    @abstractmethod
    def ask(
        self,
        filename: str,
        question: str,
        top_k: int,
        chunk_size: int,
        overlap: int,
        auto_process: bool = True,
        response_mode: str = "detailed",
    ) -> dict:
        pass