import telebot
from telebot import types
import json
import os
import time

# ---------------- НАСТРОЙКИ ----------------

BOT_TOKEN = "8723535602:AAHM_9VBMBLu6mM_VfkvEgi885Sv_D4OhmE"    # ВСТАВ СВІЙ ТОКЕН
PARAM_FILE = "params.json"

bot = telebot.TeleBot(BOT_TOKEN)

# ---------------- ЗАВАНТАЖЕННЯ ПАРАМЕТРІВ ----------------

def load_params():
    if not os.path.exists(PARAM_FILE):
        return {}
    try:
        with open(PARAM_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_params(data):
    with open(PARAM_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

ALL_PARAMS = load_params()

# ---------------- СТАН КОРИСТУВАЧІВ ----------------

user_lang = {}
user_params = {}

# ---------------- ТЕКСТИ ----------------

TEXTS = {
    "ru": {
        "choose_lang": "Выберите язык:",
        "main_menu": "Главное меню",
        "mode": "Выбрать материал",
        "choose_material": "Выберите материал:",
        "choose_power": "Выберите мощность:",
        "choose_thickness": "Выберите толщину:",
        "params": "Параметры резки",
        "edit": "Редактировать параметры",
        "enter_value": "Введите новое значение:",
        "saved": "Сохранено!"
    },
    "pl": {
        "choose_lang": "Wybierz język:",
        "main_menu": "Menu główne",
        "mode": "Wybierz materiał",
        "choose_material": "Wybierz materiał:",
        "choose_power": "Wybierz moc:",
        "choose_thickness": "Wybierz grubość:",
        "params": "Parametry cięcia",
        "edit": "Edytuj parametry",
        "enter_value": "Wpisz nową wartość:",
        "saved": "Zapisano!"
    }
}

# ---------------- СТАРТ ----------------

@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Русский", callback_data="lang_ru"))
    kb.add(types.InlineKeyboardButton("Polski", callback_data="lang_pl"))
    bot.send_message(message.chat.id, "Выберите язык:", reply_markup=kb)

# ---------------- CALLBACK ----------------

@bot.callback_query_handler(func=lambda c: True)
def callbacks(call):
    chat = call.message.chat.id

    # вибір мови
    if call.data in ["lang_ru", "lang_pl"]:
        user_lang[chat] = "ru" if call.data == "lang_ru" else "pl"
        main_menu(chat)
        return

    # меню
    if call.data == "menu":
        main_menu(chat)
        return

    # вибір матеріалу
    if call.data == "mode":
        choose_material(chat)
        return

    if call.data.startswith("mat_"):
        user_params[chat] = {"material": call.data.replace("mat_", "")}
        choose_power(chat)
        return

    # вибір потужності
    if call.data.startswith("power_"):
        user_params[chat]["power"] = call.data.replace("power_", "")
        choose_thickness(chat)
        return

    # вибір товщини
    if call.data.startswith("th_"):
        user_params[chat]["thickness"] = call.data.replace("th_", "")
        show_params(chat)
        return

    # меню редагування
    if call.data == "edit_menu":
        edit_menu(chat)
        return

    # редагування конкретного параметра
    if call.data.startswith("edit_"):
        key = call.data.replace("edit_", "")
        lang = user_lang[chat]
        bot.send_message(chat, TEXTS[lang]["enter_value"])
        bot.register_next_step_handler(call.message, lambda msg: save_edit(msg, key))
        return

    # назад
    if call.data == "back_to_material":
        choose_material(chat)
        return

    if call.data == "back_to_power":
        choose_power(chat)
        return

    if call.data == "back_to_thickness":
        choose_thickness(chat)
        return

    if call.data == "back_to_params":
        show_params(chat)
        return

# ---------------- МЕНЮ ----------------

def main_menu(chat):
    lang = user_lang[chat]
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(TEXTS[lang]["mode"], callback_data="mode"))
    bot.send_message(chat, TEXTS[lang]["main_menu"], reply_markup=kb)

def choose_material(chat):
    lang = user_lang[chat]
    kb = types.InlineKeyboardMarkup()

    materials = [
        ("steel", "Чорна сталь" if lang == "ru" else "Stal czarna"),
        ("stainless", "Нержавейка" if lang == "ru" else "Stal nierdzewna"),
        ("aluminum", "Алюминий" if lang == "ru" else "Aluminium"),
        ("copper", "Мідь" if lang == "ru" else "Miedź"),
        ("brass", "Латунь" if lang == "ru" else "Mosiądz"),
        ("bronze", "Бронза" if lang == "ru" else "Brąz")
    ]

    for code, name in materials:
        kb.add(types.InlineKeyboardButton(name, callback_data=f"mat_{code}"))

    kb.add(types.InlineKeyboardButton("🏠 В меню", callback_data="menu"))
    bot.send_message(chat, TEXTS[lang]["choose_material"], reply_markup=kb)

def choose_power(chat):
    lang = user_lang[chat]
    kb = types.InlineKeyboardMarkup()

    for p in ["1.5", "3", "6"]:
        kb.add(types.InlineKeyboardButton(f"{p} kW", callback_data=f"power_{p}"))

    kb.add(types.InlineKeyboardButton("⬅ Назад", callback_data="back_to_material"))
    kb.add(types.InlineKeyboardButton("🏠 В меню", callback_data="menu"))

    bot.send_message(chat, TEXTS[lang]["choose_power"], reply_markup=kb)

def choose_thickness(chat):
    lang = user_lang[chat]
    kb = types.InlineKeyboardMarkup()

    thicknesses = [
        "0.5", "0.8",
        "1", "1.2", "1.5",
        "2", "2.5",
        "3", "4", "5", "6",
        "8", "10", "12", "15", "20"
    ]

    for t in thicknesses:
        kb.add(types.InlineKeyboardButton(f"{t} мм", callback_data=f"th_{t}"))

    kb.add(types.InlineKeyboardButton("⬅ Назад", callback_data="back_to_power"))
    kb.add(types.InlineKeyboardButton("🏠 В меню", callback_data="menu"))

    bot.send_message(chat, TEXTS[lang]["choose_thickness"], reply_markup=kb)

# ---------------- ПОКАЗ ПАРАМЕТРІВ ----------------

def show_params(chat):
    lang = user_lang[chat]
    p = user_params[chat]

    key = f"{p['material']}_{p['power']}_{p['thickness']}"

    if key not in ALL_PARAMS:
        ALL_PARAMS[key] = {
            "speed": "",
            "focus": "",
            "nozzle": "",
            "pressure": "",
            "gas": ""
        }
        save_params(ALL_PARAMS)

    params = ALL_PARAMS[key]

    text = f"{TEXTS[lang]['params']}:\n"
    text += f"Материал: {p['material']}\n"
    text += f"Мощность: {p['power']} kW\n"
    text += f"Толщина: {p['thickness']} мм\n\n"

    for k, v in params.items():
        text += f"{k}: {v}\n"

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(TEXTS[lang]["edit"], callback_data="edit_menu"))
    kb.add(types.InlineKeyboardButton("⬅ Назад", callback_data="back_to_thickness"))
    kb.add(types.InlineKeyboardButton("🏠 В меню", callback_data="menu"))

    bot.send_message(chat, text, reply_markup=kb)

# ---------------- РЕДАГУВАННЯ ----------------

def edit_menu(chat):
    lang = user_lang[chat]
    kb = types.InlineKeyboardMarkup()

    for key in ["speed", "focus", "nozzle", "pressure", "gas"]:
        kb.add(types.InlineKeyboardButton(key, callback_data=f"edit_{key}"))

    kb.add(types.InlineKeyboardButton("⬅ Назад", callback_data="back_to_params"))
    kb.add(types.InlineKeyboardButton("🏠 В меню", callback_data="menu"))

    bot.send_message(chat, TEXTS[lang]["edit"], reply_markup=kb)

def save_edit(message, key):
    chat = message.chat.id
    lang = user_lang[chat]
    p = user_params[chat]

    combo = f"{p['material']}_{p['power']}_{p['thickness']}"

    ALL_PARAMS[combo][key] = message.text
    save_params(ALL_PARAMS)

    bot.send_message(chat, TEXTS[lang]["saved"])
    show_params(chat)

# ---------------- АВТОНОМНИЙ ЗАПУСК ----------------

while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=30)
    except Exception as e:
        print("Ошибка:", e)
        time.sleep(3)