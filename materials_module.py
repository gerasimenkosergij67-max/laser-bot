
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# ==========================
#   МАТЕРІАЛИ
# ==========================

MATERIAL_MAP = {
    "material_stainless": {"icon": "🟦", "ru": "Нержавеющая сталь"},
    "material_steel": {"icon": "⬛", "ru": "Углеродистая сталь"},
    "material_aluminum": {"icon": "⚪", "ru": "Алюминий"},
    "material_copper": {"icon": "🟧", "ru": "Медь"},
    "material_brass": {"icon": "🟨", "ru": "Латунь"},
    "material_galvanized": {"icon": "🟫", "ru": "Оцинкованная сталь"}
}

# ==========================
#   ТОВЩИНИ
# ==========================

THICKNESS_MAP = {
    "material_steel": [0.5,1,2,3,4,5,6,8,10,12,15,20,25],
    "material_stainless": [0.5,1,2,3,4,5,6,8,10,12,15,20],
    "material_aluminum": [0.5,1,2,3,4,6,8,10,12],
    "material_copper": [0.5,1,2,3,4,5,6,8,10],
    "material_brass": [0.5,1,2,3,4,5,6,8,10],
    "material_galvanized": [0.5,1,2,3,4,5]
}

# ==========================
#   МАПА ДЛЯ cut_params.py
# ==========================

MATERIAL_KEY_MAP = {
    "material_stainless": "stainless",
    "material_steel": "steel",
    "material_aluminum": "aluminum",
    "material_copper": "copper",
    "material_brass": "brass",
    "material_galvanized": "galvanized"
}

# ==========================
#   МЕНЮ МАТЕРІАЛІВ
# ==========================

def get_materials_menu(lang: str):
    keyboard = []
    for key, data in MATERIAL_MAP.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{data['icon']} {data['ru']}",
                callback_data=key
            )
        ])
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="choose_power")])
    return InlineKeyboardMarkup(keyboard)

# ==========================
#   МЕНЮ ТОВЩИН
# ==========================

def get_dynamic_thickness_menu(material_key: str):
    thicknesses = THICKNESS_MAP.get(material_key, [])
    keyboard = []

    for t in thicknesses:
        keyboard.append([
            InlineKeyboardButton(
                f"📏 {t} мм",
                callback_data=f"thickness|{material_key}|{t}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton("🔙 Назад", callback_data="choose_material")
    ])

    return InlineKeyboardMarkup(keyboard)