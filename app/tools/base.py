from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult:
    success: bool
    tool_name: str
    message: str
    data: dict[str, Any] | None = None


class BaseTool(ABC):
    name: str
    description: str

    @abstractmethod
    def can_handle(self, text: str) -> bool:
        pass

    @abstractmethod
    def execute(self, text: str) -> ToolResult:
        pass