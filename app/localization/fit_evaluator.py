def get_fit_status(length: int, max_chars: int) -> str:
    if max_chars <= 0:
        raise ValueError("max_chars must be greater than 0")

    ratio = length / max_chars

    if ratio <= 0.85:
        return "fit"
    if ratio <= 1.0:
        return "borderline"
    return "overflow"


def evaluate_text(text: str, max_chars: int) -> dict:
    normalized_text = text.strip()
    length = len(normalized_text)

    return {
        "text": normalized_text,
        "length": length,
        "max_chars": max_chars,
        "fit_status": get_fit_status(length, max_chars),
    }