def extract_overflows(result: dict) -> list[dict]:
    overflows = []

    for key, langs in result.items():
        for lang, data in langs.items():
            if data["fit_status"] == "overflow":
                overflows.append({
                    "key": key,
                    "language": lang,
                    "text": data["text"],
                    "length": data["length"],
                    "max_chars": data["max_chars"],
                })

    return overflows