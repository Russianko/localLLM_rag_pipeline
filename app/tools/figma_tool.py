import json
import urllib.request
from app.config import FIGMA_TOOL_BASE_URL
from app.tools.base import BaseTool, ToolResult


class FigmaTool(BaseTool):
    name = "figma"
    description = "Выполняет действия в Figma через локальный HTTP API."

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        figma_words = [
            "figma",
            "фигма",
            "создай текст",
            "создай прямоугольник",
            "нарисуй прямоугольник",
            "измени цвет",
        ]

        return any(word in text for word in figma_words)

    def execute(self, text: str) -> ToolResult:
        payload = self._build_payload(text)

        try:
            response = self._post("/action", payload)

            return ToolResult(
                success=True,
                tool_name=self.name,
                message="Figma action executed.",
                data=response,
            )

        except Exception as e:
            return ToolResult(
                success=False,
                tool_name=self.name,
                message=f"Figma tool failed: {e}",
                data={"payload": payload},
            )

    def _build_payload(self, text: str) -> dict:
        text_lower = text.lower()

        if "создай текст" in text_lower:
            content = text_lower.split("создай текст", 1)[-1].strip() or "New text"

            return {
                "action": "create_text",
                "params": {
                    "text": content,
                    "x": 100,
                    "y": 100,
                    "font_size": 32,
                },
            }

        if "прямоугольник" in text_lower:
            return {
                "action": "create_rectangle",
                "params": {
                    "x": 100,
                    "y": 100,
                    "width": 300,
                    "height": 160,
                    "fill": "#2F80ED",
                },
            }

        return {
            "action": "unknown",
            "params": {
                "raw_text": text,
            },
        }

    def _post(self, path: str, payload: dict) -> dict:
        url = f"{FIGMA_TOOL_BASE_URL}{path}"

        body = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            url=url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=5) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}