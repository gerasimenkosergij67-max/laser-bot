import json
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from PIL import Image
import pytesseract

logging.basicConfig(level=logging.INFO)

API_TOKEN = "8723535602:AAHM_9VBMBLu6mM_VfkvEgi885Sv_D4OhmE" 

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

LEARNED_FILE = "learned_params.json"

if not os.path.exists(LEARNED_FILE):
    with open(LEARNED_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=4)


def load_learned():
    with open(LEARNED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_learned(data):
    with open(LEARNED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# =========================
# LANG SYSTEM
# =========================
user_lang = {}  # user_id -> "ru" / "pl"

        "choose_lang": "Wybierz język:",
        "lang_ru": "Rosyjski",
        "lang_pl": "Polski",
        "main_menu": "Menu główne",
        "mode": "Wybierz materiał",
        "ocr": "OCR (zdjęcie → tekst)",
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

 TEXTS = {
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
}
# =========================
# MATERIALS / POWERS / THICKNESSES
# =========================
MATERIALS = {
    "ru": ["Оцинковка", "Нержавейка", "Медь", "Чёрная сталь", "Бронза", "Алюминий"],
    "pl": ["Ocynk", "Stal nierdzewna", "Miedź", "Stal czarna", "Brąz", "Aluminium"],
}
MATERIAL_KEYS = ["galvanized", "stainless", "copper", "mild_steel", "bronze", "aluminum"]

POWERS = [3, 4, 5, 6, 8, 10, 12]
THICKNESSES = [0.5, 1, 1.5, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20]

# =========================
# USER STATE
# =========================
user_state = {}  # user_id -> dict


def get_lang(user_id):
    return user_lang.get(user_id, "ru")


def set_lang(user_id, lang):
    user_lang[user_id] = lang


def get_state(user_id):
    return user_state.setdefault(user_id, {
        "step": None,
        "material_key": None,
        "power": None,
        "thickness": None,
        "edit_field": None,
    })# =========================
# NOZZLE LOGIC
# =========================
def get_nozzle(thickness):
    if thickness <= 2:
        return 1.2
    elif thickness <= 6:
        return 1.4
    elif thickness <= 12:
        return 1.6
    elif thickness <= 15:
        return 1.8
    else:
        return 2.0


# =========================
# GAS LOGIC
# =========================
def get_gas(material_key):
    if material_key == "mild_steel":
        return "O2"
    return "N2"


# =========================
# DEFAULT PARAMS LIBRARY
# =========================
def base_speed_for_material(material_key, power):
    base = {
        "galvanized": 25,
        "stainless": 20,
        "copper": 15,
        "mild_steel": 18,
        "bronze": 14,
        "aluminum": 28,
    }[material_key]

    factor = power / 4.0
    return base * factor


def focus_for_material(material_key, thickness):
    if thickness <= 1:
        base = -0.3
    elif thickness <= 2:
        base = -0.5
    elif thickness <= 4:
        base = -0.8
    elif thickness <= 6:
        base = -1.0
    elif thickness <= 8:
        base = -1.2
    elif thickness <= 10:
        base = -1.5
    elif thickness <= 12:
        base = -1.8
    elif thickness <= 15:
        base = -2.0
    else:
        base = -2.3

    if material_key in ["stainless", "aluminum"]:
        base -= 0.1
    if material_key == "mild_steel":
        base -= 0.2

    return round(base, 2)


def pressure_for(material_key, thickness):
    gas = get_gas(material_key)

    if gas == "N2":
        if thickness <= 1:
            return 18
        elif thickness <= 2:
            return 17
        elif thickness <= 4:
            return 16
        elif thickness <= 6:
            return 15
        elif thickness <= 8:
            return 14
        elif thickness <= 10:
            return 13
        elif thickness <= 12:
            return 12
        elif thickness <= 15:
            return 11
        else:
            return 10

    else:  # O2
        if thickness <= 1:
            return 6
        elif thickness <= 2:
            return 6
        elif thickness <= 4:
            return 7
        elif thickness <= 6:
            return 7
        elif thickness <= 8:
            return 8
        elif thickness <= 10:
            return 8
        elif thickness <= 12:
            return 9
        elif thickness <= 15:
            return 9
        else:
            return 10


def get_default_params(material_key, power, thickness):
    gas = get_gas(material_key)
    nozzle = get_nozzle(thickness)

    base_1mm = base_speed_for_material(material_key, power)
    speed = base_1mm / (0.6 + 0.15 * thickness)
    speed = max(0.4, speed)

    focus = focus_for_material(material_key, thickness)
    pressure = pressure_for(material_key, thickness)

    return {
        "speed": round(speed, 2),
        "focus": focus,
        "nozzle": nozzle,
        "pressure": pressure,
        "gas": gas,
    }


def get_key(material_key, power, thickness):
    return f"{material_key}|{power}|{thickness}"


def get_params(material_key, power, thickness):
    learned = load_learned()
    key = get_key(material_key, power, thickness)
    if key in learned:
        return learned[key]
    return get_default_params(material_key, power, thickness)


def save_param_field(material_key, power, thickness, field, value):
    learned = load_learned()
    key = get_key(material_key, power, thickness)
    if key not in learned:
        learned[key] = get_default_params(material_key, power, thickness)
    learned[key][field] = value
    save_learned(learned)


# =========================
# KEYBOARDS
# =========================
def lang_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Русский"), KeyboardButton("Polski"))
    return kb


def main_menu_kb(lang):
    t = TEXTS[lang]
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(t["mode"]))
    kb.add(KeyboardButton(t["ocr"]))
    return kb


def materials_kb(lang):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for name in MATERIALS[lang]:
        kb.add(KeyboardButton(name))
    kb.add(KeyboardButton(TEXTS[lang]["back"]))
    return kb


def powers_kb(lang):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for p in POWERS:
        kb.add(KeyboardButton(str(p)))
    kb.add(KeyboardButton(TEXTS[lang]["back"]))
    return kb


def thickness_kb(lang):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for th in THICKNESSES:
        kb.add(KeyboardButton(str(th)))
    kb.add(KeyboardButton(TEXTS[lang]["back"]))
    return kb


def edit_kb(lang):
    t = TEXTS[lang]
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(t["edit_speed"]), KeyboardButton(t["edit_focus"]))
    kb.add(KeyboardButton(t["edit_nozzle"]), KeyboardButton(t["edit_pressure"]))
    kb.add(KeyboardButton(t["edit_gas"]))
    kb.add(KeyboardButton(t["back"]))
    return kb
# =========================
# SHOW PARAMS
# =========================
async def show_params(message: types.Message, st):
    lang = get_lang(message.from_user.id)
    t = TEXTS[lang]

    material_key = st["material_key"]
    power = st["power"]
    thickness = st["thickness"]

    params = get_params(material_key, power, thickness)

    txt = (
        f"📌 {t['params']}:\n\n"
        f"Материал: {material_key}\n"
        f"Мощность: {power} кВт\n"
        f"Толщина: {thickness} мм\n\n"
        f"Скорость: {params['speed']} м/мин\n"
        f"Фокус: {params['focus']} мм\n"
        f"Сопло: {params['nozzle']} мм\n"
        f"Давление: {params['pressure']} бар\n"
        f"Газ: {params['gas']}\n"
    )

    await message.answer(txt, reply_markup=ReplyKeyboardMarkup(
        resize_keyboard=True
    ).add(TEXTS[lang]["edit"], TEXTS[lang]["back"]))


# =========================
# START
# =========================
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    uid = message.from_user.id
    set_lang(uid, "ru")
    st = get_state(uid)
    st["step"] = "choose_lang"

    await message.answer(TEXTS["ru"]["choose_lang"], reply_markup=lang_keyboard())


# =========================
# CHOOSE LANGUAGE
# =========================
@dp.message_handler(lambda m: m.text in ["Русский", "Polski"])
async def choose_lang(message: types.Message):
    uid = message.from_user.id

    if message.text == "Русский":
        set_lang(uid, "ru")
    else:
        set_lang(uid, "pl")

    lang = get_lang(uid)
    st = get_state(uid)
    st["step"] = "main_menu"

    await message.answer(TEXTS[lang]["main_menu"], reply_markup=main_menu_kb(lang))


# =========================
# MAIN ROUTER
# =========================
@dp.message_handler()
async def main_router(message: types.Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    st = get_state(uid)
    text = message.text
    t = TEXTS[lang]

    # Назад
    if text == t["back"]:
        st["step"] = "main_menu"
        await message.answer(t["main_menu"], reply_markup=main_menu_kb(lang))
        return

    # ГОЛОВНЕ МЕНЮ
    if st["step"] == "main_menu":
        if text == t["mode"]:
            st["step"] = "choose_material"
            await message.answer(t["choose_material"], reply_markup=materials_kb(lang))
            return

        if text == t["ocr"]:
            st["step"] = "ocr_wait_photo"
            await message.answer(t["send_photo"])
            return

        await message.answer(t["main_menu"], reply_markup=main_menu_kb(lang))
        return

    # Вибір матеріалу
    if st["step"] == "choose_material":
        if text in MATERIALS[lang]:
            idx = MATERIALS[lang].index(text)
            st["material_key"] = MATERIAL_KEYS[idx]
            st["step"] = "choose_power"
            await message.answer(t["choose_power"], reply_markup=powers_kb(lang))
            return
        else:
            await message.answer(t["choose_material"], reply_markup=materials_kb(lang))
            return

    # Вибір потужності
    if st["step"] == "choose_power":
        try:
            p = int(text)
            if p in POWERS:
                st["power"] = p
                st["step"] = "choose_thickness"
                await message.answer(t["choose_thickness"], reply_markup=thickness_kb(lang))
                return
        except:
            pass

        await message.answer(t["choose_power"], reply_markup=powers_kb(lang))
        return

    # Вибір товщини
    if st["step"] == "choose_thickness":
        try:
            th = float(text.replace(",", "."))
            if th in THICKNESSES:
                st["thickness"] = th
                st["step"] = "show_params"
                await show_params(message, st)
                return
        except:
            pass

        await message.answer(t["choose_thickness"], reply_markup=thickness_kb(lang))
        return

    # Показ параметрів
    if st["step"] == "show_params":
        if text == t["edit"]:
            st["step"] = "edit_menu"
            await message.answer(t["edit"], reply_markup=edit_kb(lang))
            return
        else:
            await show_params(message, st)
            return

    # Меню редагування
    if st["step"] == "edit_menu":
        mapping = {
            t["edit_speed"]: "speed",
            t["edit_focus"]: "focus",
            t["edit_nozzle"]: "nozzle",
            t["edit_pressure"]: "pressure",
            t["edit_gas"]: "gas",
        }

        if text in mapping:
            st["edit_field"] = mapping[text]
            st["step"] = "waiting_new_value"
            await message.answer(t["enter_value"])
            return

        await message.answer(t["edit"], reply_markup=edit_kb(lang))
        return

    # Очікування нового значення
    if st["step"] == "waiting_new_value":
        field = st.get("edit_field")
        material_key = st["material_key"]
        power = st["power"]
        thickness = st["thickness"]

        if field == "gas":
            val = text.strip().upper()
            if val not in ["N2", "O2"]:
                await message.answer(t["invalid_value"])
                return
            save_param_field(material_key, power, thickness, field, val)
        else:
            try:
                v = float(text.replace(",", "."))
            except ValueError:
                await message.answer(t["invalid_value"])
                return
            save_param_field(material_key, power, thickness, field, v)

        await message.answer(t["saved"])
        st["step"] = "show_params"
        await show_params(message, st)
        return

    # Якщо нічого не підійшло
    st["step"] = "main_menu"
    await message.answer(t["main_menu"], reply_markup=main_menu_kb(lang))
# =========================
# OCR HANDLER
# =========================
@dp.message_handler(content_types=["photo"])
async def handle_photo(message: types.Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    st = get_state(uid)

    # OCR активний тільки коли бот чекає фото
    if st["step"] != "ocr_wait_photo":
        return

    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path

    downloaded = await bot.download_file(file_path)
    img_path = f"ocr_{uid}.jpg"
    with open(img_path, "wb") as f:
        f.write(downloaded.read())

    import cv2, numpy as np, re

    img = cv2.imread(img_path)

    # Попередня обробка
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

    processed_path = f"ocr_proc_{uid}.png"
    cv2.imwrite(processed_path, thresh)

    # OCR
    text = pytesseract.image_to_string(processed_path, lang="eng+rus+ukr")

    os.remove(img_path)
    os.remove(processed_path)

    # Парсинг параметрів
    speed = re.findall(r"(?:speed|скорость|prędkość)[^\d]*(\d+\.?\d*)", text, re.I)
    focus = re.findall(r"(?:focus|фокус)[^\d\-]*(\-?\d+\.?\d*)", text, re.I)
    pressure = re.findall(r"(?:pressure|давление|ciśnienie)[^\d]*(\d+\.?\d*)", text, re.I)
    gas = re.findall(r"(N2|O2)", text, re.I)

    result = "📄 Результат OCR:\n\n" + text + "\n\n"
    params = {}

    if speed:
        params["speed"] = float(speed[0])
        result += f"🔹 Speed: {params['speed']}\n"
    if focus:
        params["focus"] = float(focus[0])
        result += f"🔹 Focus: {params['focus']}\n"
    if pressure:
        params["pressure"] = float(pressure[0])
        result += f"🔹 Pressure: {params['pressure']}\n"
    if gas:
        params["gas"] = gas[0].upper()
        result += f"🔹 Gas: {params['gas']}\n"

    await message.answer(result)

    # Якщо параметри знайдені — пропонуємо зберегти
    if params:
        st["ocr_params"] = params
        st["step"] = "ocr_save_offer"

        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton("💾 Зберегти"), KeyboardButton("❌ Не зберігати"))

        await message.answer("Зберегти ці параметри?", reply_markup=kb)
    else:
        st["step"] = "main_menu"
        await message.answer(TEXTS[lang]["main_menu"], reply_markup=main_menu_kb(lang))


# =========================
# OCR SAVE DECISION
# =========================
@dp.message_handler(lambda m: m.text in ["💾 Зберегти", "❌ Не зберігати"])
async def ocr_save_handler(message: types.Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    st = get_state(uid)

    if st["step"] != "ocr_save_offer":
        return

    if message.text == "💾 Зберегти":
        if "material_key" in st and st["material_key"] and st["power"] and st["thickness"]:
            params = st.get("ocr_params", {})
            for k, v in params.items():
                save_param_field(st["material_key"], st["power"], st["thickness"], k, v)

            await message.answer("Збережено!")
        else:
            await message.answer("Неможливо зберегти — спочатку виберіть матеріал, потужність і товщину.")
    else:
        await message.answer("Добре, не зберігаю.")

    st["step"] = "main_menu"
    await message.answer(TEXTS[lang]["main_menu"], reply_markup=main_menu_kb(lang))


# =========================
# BOT START
# =========================
if __name__ == "__main__":
    print("BOT STARTED")
    executor.start_polling(dp, skip_updates=False)

