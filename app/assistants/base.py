from abc import ABC, abstractmethod


class BaseAssistant(ABC):
    @abstractmethod
    def health(self) -> dict:
        pass

    @abstractmethod
    def process_document(
        self,
        filename: str,
        summary_limit: int = 4000,
        chunk_size: int = 500,
        overlap: int = 100,
        force_rebuild: bool = False,
    ) -> dict:
        pass

    @abstractmethod
    def ask(
        self,
        filename: str,
        question: str,
        top_k: int = 3,
        chunk_size: int = 500,
        overlap: int = 100,
        auto_process: bool = True,
        response_mode: str = "detailed",
    ) -> dict:
        pass