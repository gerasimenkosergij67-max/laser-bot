import re

# Читаємо bot.py
with open("bot.py", "r", encoding="utf-8") as f:
    code = f.read()

# Видаляємо ВСЕ, що йде після правильного закриття словника TEXTS
cleaned = re.sub(
    r'TEXTS\s*=\s*\{[\s\S]*?\}\s*\}',   # шукаємо повний словник TEXTS
    '''TEXTS = {
    "ru": {
        "choose_lang": "Выберите язык:",
        "lang_ru": "Русский",
        "lang_pl": "Polski",
        "main_menu": "Главное меню",
        "mode": "Выбрать материал",
        "ocr": "OCR (фото → текст)",
        "choose_material": "Выберите материал:",
        "choose_power": "Выберите мощность (кВт):",
        "choose_thickness": "Выберите толщину (мм):",
        "edit": "Редактировать параметры",
        "back": "⬅ Назад",
        "enter_value": "Введите новое значение:",
        "saved": "Сохранено!",
        "send_photo": "Отправьте фото для OCR",
        "invalid_value": "Некорректное значение. Попробуйте ещё раз.",
        "no_params": "Параметры не найдены.",
        "params": "Параметры резки",
        "edit_speed": "Скорость",
        "edit_focus": "Фокус",
        "edit_nozzle": "Сопло",
        "edit_pressure": "Давление",
        "edit_gas": "Газ"
    },
    "pl": {
        "choose_lang": "Wybierz język:",
        "lang_ru": "Rosyjski",
        "lang_pl": "Polski",
        "main_menu": "Menu główne",
        "mode": "Wybierz materiał",
        "ocr": "OCR (zdjęcie → текст)",
        "choose_material": "Wybierz materiał:",
        "choose_power": "Wybierz moc (kW):",
        "choose_thickness": "Wybierz grubość (mm):",
        "edit": "Edytuj parametry",
        "back": "⬅ Wstecz",
        "enter_value": "Wpisz nową wartość:",
        "saved": "Zapisano!",
        "send_photo": "Wyślij zdjęcie do OCR",
        "invalid_value": "Nieprawidłowa wartość. Spróbuj ponownie.",
        "no_params": "Brak parametrów.",
        "params": "Parametry cięcia",
        "edit_speed": "Prędkość",
        "edit_focus": "Ognisko",
        "edit_nozzle": "Dysza",
        "edit_pressure": "Ciśnienie",
        "edit_gas": "Gaz"
    }
}''',
    code,
    flags=re.MULTILINE
)

# Записуємо чистий файл
with open("bot_clean.py", "w", encoding="utf-8") as f:
    f.write(cleaned)

print("Готово! Файл bot_clean.py створено.")