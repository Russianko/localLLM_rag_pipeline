from app.config import TOOLS_ENABLED
from app.tools.registry import build_tool_registry
from app.tools.base import ToolResult


class ToolRouter:
    def __init__(self):
        self.registry = build_tool_registry()

    def try_execute(self, text: str) -> ToolResult | None:
        if not TOOLS_ENABLED:
            return None

        tool = self.registry.find_tool(text)

        if tool is None:
            return None

        return tool.execute(text)