import re

def extract_value(patterns, text, cast_func=None):
    for p in patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            if cast_func:
                try:
                    return cast_func(value.replace(",", "."))
                except:
                    return value
            return value
    return None


def analyze_parameters(text: str) -> str:
    text = text.lower()

    # ==========================
    #   РАСПОЗНАВАНИЕ ПОЛЕЙ
    # ==========================

    material = extract_value(
        [
            r"материал[:\- ]+(.+)",
            r"матеріал[:\- ]+(.+)",
            r"material[:\- ]+(.+)",
            r"stal[:\- ]+(.+)",
        ],
        text
    )

    thickness = extract_value(
        [
            r"(?:толщина|товщина|grubość|grubosc)[:\- ]+([\d\.,]+)",
            r"(\d+[\.,]?\d*)\s*мм"
        ],
        text,
        float
    )

    speed = extract_value(
        [
            r"(?:скорость|швидкість|prędkość|predkosc)[:\- ]+([\d\.,]+)",
            r"([\d\.,]+)\s*м/мин"
        ],
        text,
        float
    )

    gas = extract_value(
        [
            r"(?:газ|gaz)[:\- ]+(.+)",
            r"(o2|n2|air)"
        ],
        text
    )

    pressure = extract_value(
        [
            r"(?:давление|тиск|ciśnienie|cisnienie)[:\- ]+([\d\.,]+)",
            r"([\d\.,]+)\s*мпа"
        ],
        text,
        float
    )

    nozzle = extract_value(
        [
            r"(?:сопло|dysza)[:\- ]+(.+)",
            r"(\d+[\.,]?\d*)\s*мм\s*сопло"
        ],
        text
    )

    power = extract_value(
        [
            r"(?:мощность|потужність|moc)[:\- ]+(\d+)",
            r"(\d+)\s*%"
        ],
        text,
        int
    )

    focus = extract_value(
        [
            r"(?:фокус|ognisko|focus)[:\- ]+([\d\.,]+)",
            r"([\-\d\.,]+)\s*мм\s*фокус"
        ],
        text,
        float
    )

    # ==========================
    #   ФОРМИРОВАНИЕ ОТЧЁТА
    # ==========================

    result = "📊 *Анализ параметров:*\n\n"

    result += f"• Материал: {material or '—'}\n"
    result += f"• Толщина: {thickness if thickness is not None else '—'} мм\n"
    result += f"• Скорость: {speed if speed is not None else '—'} м/мин\n"
    result += f"• Газ: {gas or '—'}\n"
    result += f"• Давление: {pressure if pressure is not None else '—'} МПа\n"
    result += f"• Сопло: {nozzle or '—'}\n"
    result += f"• Мощность: {power if power is not None else '—'} %\n"
    result += f"• Фокус: {focus if focus is not None else '—'} мм\n"

    return result