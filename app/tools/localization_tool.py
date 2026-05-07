from app.tools.base import BaseTool, ToolResult
from app.localization.plugin_action_exporter import (
    build_plugin_actions_summary,
    save_plugin_actions,
)

from app.localization.figma_payload_builder import build_figma_payload
from app.localization.fit_decision_engine import decide_payload_actions
from app.localization.layout_adjustment_planner import build_payload_adjustment_plan
from app.localization.figma_plugin_action_builder import (
    build_plugin_actions_from_layout_plan,
)

from app.localization.mapping_loader import load_mapping


DEFAULT_CHAR_LIMITS_BY_FORMAT = {
    "1080x1080": {
        "headline": 25,
        "subheadline": 45,
        "cta": 18,
    }
}


class LocalizationTool(BaseTool):
    name = "localization"

    description = (
        "Runs localization pipeline: xlsx → payload → fit decisions "
        "→ layout plan → Figma plugin actions."
    )

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        triggers = [
            "локализация",
            "localization",
            "переводы",
            "figma actions",
            "plugin actions",
        ]

        return any(trigger in text for trigger in triggers)

    def execute(
            self,
            text: str = "",
            *,
            xlsx_path: str,
            mapping_path: str,
            rules_path: str,
            output_path: str | None = None,
            char_limits_by_format: dict | None = None,
    ) -> ToolResult:
        try:
            payload = build_figma_payload(
                xlsx_path=xlsx_path,
                mapping_path=mapping_path,
                rules_path=rules_path,
            )

            decisions = decide_payload_actions(
                payload=payload,
                char_limits_by_format=char_limits_by_format
                or DEFAULT_CHAR_LIMITS_BY_FORMAT,
            )

            plans = build_payload_adjustment_plan(
                decisions=decisions,
                payload=payload,
            )

            mapping = load_mapping(mapping_path)

            actions = build_plugin_actions_from_layout_plan(
                plans,
                mapping,
            )

            summary = build_plugin_actions_summary(actions)
            if output_path:
                save_plugin_actions(actions, output_path)

            return ToolResult(
                success=True,
                tool_name=self.name,
                message="Localization pipeline completed.",
                data={
                    "summary": summary,
                    "actions": actions,
                    "output_path": output_path,
                },
            )

        except Exception as e:
            return ToolResult(
                success=False,
                tool_name=self.name,
                message=f"Localization pipeline failed: {e}",
                data={
                    "xlsx_path": xlsx_path,
                    "mapping_path": mapping_path,
                    "rules_path": rules_path,
                    "output_path": output_path,
                },
            )