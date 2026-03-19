from datetime import datetime
from pathlib import Path


class NoteWriter:
    def build_note_content(
        self,
        title: str,
        source: str,
        summary: str,
        key_points: str,
        action_items: str,
    ) -> str:
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        note_content = f"""# {title}

Source: {source}
Date: {current_date}

## Summary

{summary}

## Key Points

{key_points}

## Action Items

{action_items}
"""

        return note_content

    def save_note(
        self,
        output_path: str,
        title: str,
        source: str,
        summary: str,
        key_points: str,
        action_items: str,
    ) -> str:
        note_content = self.build_note_content(
            title=title,
            source=source,
            summary=summary,
            key_points=key_points,
            action_items=action_items,
        )

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(note_content, encoding="utf-8")

        return note_content