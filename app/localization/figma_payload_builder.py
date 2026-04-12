from app.localization.spreadsheet_reader import read_translations
from app.localization.mapping_loader import load_mapping, get_frames
from app.localization.rules_loader import load_rules, get_format_rules
from mapping_loader import get_target
from app.localization.mapping_loader import load_mapping, get_frames, get_target


def build_figma_payload(
    xlsx_path: str,
    mapping_path: str,
    rules_path: str,
) -> list[dict]:
    """
    Собирает payload для Figma на основе:
    - xlsx с переводами
    - mapping.json
    - layout_rules.json

    Что делает функция:
    1. Читает переводы из xlsx
    2. Читает список frame из mapping.json
    3. Для каждого frame определяет:
       - какой это формат
       - какой язык нужен
       - какие поля нужно вставить
    4. Подтягивает правила для каждого поля
    5. Формирует готовый payload для передачи в Figma plugin

    Возвращает:
    list[dict]
        Список frame payload-ов.
        Один элемент списка = один frame в Figma.
    """

    # 1. Загружаем все переводы из Excel.
    # Формат примерно такой:
    # {
    #   "promo.headline": {"ru": "...", "en": "..."},
    #   "promo.cta": {"ru": "...", "en": "..."}
    # }
    translations = read_translations(xlsx_path)

    # 2. Загружаем mapping.json
    # Там лежит список frame и связь между node_name и key из xlsx.
    mapping = load_mapping(mapping_path)

    # 3. Загружаем layout_rules.json
    # Там лежат правила по форматам и полям.
    rules = load_rules(rules_path)

    # Сюда будем складывать итоговый результат.
    payload = []

    # Получаем список описаний frame из mapping.json
    frames = get_frames(mapping)

    # Проходим по каждому frame, который надо подготовить для Figma
    for frame in frames:
        frame_name = frame["frame_name"]
        format_id = frame["format_id"]
        language = frame["language"]
        fields = frame["fields"]


        # Получаем правила для конкретного формата, например "1080x1080"
        format_rules = get_format_rules(rules, format_id)

        # Здесь будем собирать список текстовых узлов (headline, cta и т.д.)
        nodes = []

        # fields выглядит так:
        # {
        #   "headline": "promo.headline",
        #   "subheadline": "promo.subheadline",
        #   "cta": "promo.cta"
        # }
        #
        # Где:
        # - "headline" = имя node в Figma
        # - "promo.headline" = key_name из xlsx
        for node_name, translation_key in fields.items():
            # Проверяем, есть ли такой ключ вообще в переводах
            if translation_key not in translations:
                available_keys_preview = list(translations.keys())[:10]

                raise ValueError(
                    f"Translation key '{translation_key}' not found in xlsx. "
                    f"Example available keys: {available_keys_preview}"
                )

            # Берем словарь языков для этого ключа:
            # {"ru": "...", "en": "..."}
            language_map = translations[translation_key]

            # Проверяем, есть ли нужный язык для этого frame
            if language not in language_map:
                raise ValueError(
                    f"Language '{language}' not found for key '{translation_key}'"
                )

            # Достаём сам текст, который надо вставить в Figma
            text = language_map[language]


            # Проверяем, есть ли правила для этого поля
            # Например для headline / subheadline / cta
            if node_name not in format_rules:
                raise ValueError(
                    f"Rules for node '{node_name}' not found in format '{format_id}'"
                )

            node_rules = format_rules[node_name]

            target = get_target(mapping, translation_key)

            # Формируем описание одного текстового узла для Figma
            node_payload = {
                "node_name": node_name,  # пока оставь
                "translation_key": translation_key,
                "text": text,
                "rules": node_rules,
                "target": target  # 👈 ВАЖНО
            }

            nodes.append(node_payload)

        # Когда все узлы frame собраны, формируем payload для frame целиком
        frame_payload = {
            "frame_name": frame_name,
            "format_id": format_id,
            "language": language,
            "nodes": nodes,
        }

        payload.append(frame_payload)

    return payload