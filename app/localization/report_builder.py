import json
from pathlib import Path


def build_summary(items: dict) -> dict:
    summary = {
        "fit": 0,
        "borderline": 0,
        "overflow": 0,
        "total_checked": 0,
    }

    for key_data in items.values():
        for lang_data in key_data.values():
            status = lang_data["fit_status"]
            if status not in summary:
                continue

            summary[status] += 1
            summary["total_checked"] += 1

    return summary


def build_report(result: dict) -> dict:
    return {
        "summary": build_summary(result),
        "items": result,
    }


def save_report_to_json(result: dict, output_path: str) -> None:
    report = build_report(result)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)