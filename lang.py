LANG = {
    # ==========================
    #   ГОЛОВНЕ МЕНЮ
    # ==========================
    "main_menu": {
        "ru": "🏠 Главное меню:",
        "pl": "🏠 Menu główne:"
    },

    "cut_modes": {
        "ru": "✂️ Режимы резки",
        "pl": "✂️ Tryby cięcia"
    },

    "library": {
        "ru": "📘 Библиотека параметров",
        "pl": "📘 Biblioteka parametrów"
    },

    "photo": {
        "ru": "📷 Фото-анализ",
        "pl": "📷 Analiza zdjęć"
    },

    # ==========================
    #   РЕЖИМЫ РЕЗКИ
    # ==========================
    "choose_mode": {
        "ru": "Выберите режим резки:",
        "pl": "Wybierz tryb cięcia:"
    },

    "mode_cut": {
        "ru": "Резка",
        "pl": "Cięcie"
    },

    "mode_engrave": {
        "ru": "Гравировка",
        "pl": "Grawerowanie"
    },

    "mode_pierce": {
        "ru": "Перфорация",
        "pl": "Przebijanie"
    },

    # ==========================
    #   ВЫБОР ПОТУЖНОСТИ
    # ==========================
    "choose_power": {
        "ru": "Выберите мощность лазера:",
        "pl": "Wybierz moc lasera:"
    },

    # ==========================
    #   МАТЕРИАЛЫ
    # ==========================
    "choose_material": {
        "ru": "Выберите материал:",
        "pl": "Wybierz materiał:"
    },

    "choose_thickness": {
        "ru": "Выберите толщину:",
        "pl": "Wybierz grubość:"
    },

    # ==========================
    #   БИБЛИОТЕКА
    # ==========================
    "learned_params": {
        "ru": "📘 Сохранённые параметры",
        "pl": "📘 Zapisane parametry"
    },

    "add_params": {
        "ru": "➕ Добавить параметры",
        "pl": "➕ Dodaj parametry"
    },

    "open_file": {
        "ru": "📂 Импорт из файла",
        "pl": "📂 Import z pliku"
    },

    "send_params": {
        "ru": "Отправьте параметры текстом:",
        "pl": "Wyślij parametry w formie tekstowej:"
    },

    "send_file": {
        "ru": "Отправьте файл с параметрами:",
        "pl": "Wyślij plik z parametrami:"
    },

    # ==========================
    #   ПРОЧЕЕ
    # ==========================
    "photo_not_ready": {
        "ru": "📷 Фото-анализ пока не готов.",
        "pl": "📷 Analiza zdjęć jeszcze nie jest gotowa."
    },

    "calculated_speed": {
        "ru": "Расчётная скорость",
        "pl": "Prędkość obliczona"
    },

    "home": {
        "ru": "🏠 В главное меню",
        "pl": "🏠 Do menu głównego"
    },

    "back": {
        "ru": "🔙 Назад",
        "pl": "🔙 Wstecz"
    }
}


def t(lang: str, key: str) -> str:
    """Возвращает перевод строки по ключу."""
    try:
        return LANG[key][lang]
    except:
        return f"[{key}]"