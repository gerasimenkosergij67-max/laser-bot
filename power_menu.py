from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from lang import t

# Список доступных мощностей (в ваттах)
POWER_LIST = [
    1000, 1500, 2000, 3000,
    4000, 6000, 8000, 10000, 12000
]

def get_power_menu(lang: str):
    keyboard = []
    row = []

    for p in POWER_LIST:
        label = f"⚡ {p // 1000} кВт"
        row.append(InlineKeyboardButton(label, callback_data=f"power_{p}"))

        if len(row) == 3:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton(t(lang, "back"), callback_data="cut_modes")])

    return InlineKeyboardMarkup(keyboard)