from app.tools.base import BaseTool
from app.tools.localization_tool import LocalizationTool


class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        self.tools[tool.name] = tool

    def list_tools(self) -> list[dict]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
            }
            for tool in self.tools.values()
        ]

    def get(self, name: str) -> BaseTool | None:
        return self.tools.get(name)

    def find_tool(self, text: str) -> BaseTool | None:
        for tool in self.tools.values():
            if tool.can_handle(text):
                return tool

        return None


def build_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(LocalizationTool())
    return registry