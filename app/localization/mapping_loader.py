import json
from pathlib import Path


def load_mapping(path: str) -> dict:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Mapping file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Проверка старого слоя
    if "frames" not in data:
        raise ValueError("Invalid mapping.json: 'frames' field is missing")

    # 👇 НОВОЕ
    if "targets" not in data:
        raise ValueError("Invalid mapping.json: 'targets' field is missing")

    return data


def get_frames(mapping: dict) -> list:
    return mapping["frames"]


# 👇 НОВОЕ
def get_targets(mapping: dict) -> dict:
    return mapping["targets"]


# 👇 НОВОЕ
def get_target(mapping: dict, translation_key: str) -> dict:
    targets = get_targets(mapping)

    if translation_key not in targets:
        raise KeyError(
            f"Target not found for translation_key='{translation_key}'"
        )

    return targets[translation_key]

