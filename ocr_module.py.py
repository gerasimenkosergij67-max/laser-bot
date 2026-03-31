import pytesseract
from PIL import Image
import re
import json
import os

# Якщо Tesseract не в PATH — вкажи шлях вручну:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_params_from_photo(photo_path):
    img = Image.open(photo_path)
    text = pytesseract.image_to_string(img)

    material = None
    thickness = None
    speed = None

    # Матеріал
    if "steel" in text.lower() or "thép" in text.lower():
        material = "steel"
    if "inox" in text.lower() or "stainless" in text.lower():
        material = "stainless"

    # Товщина
    th_match = re.search(r"(\d+)\s*mm", text.lower())
    if th_match:
        thickness = th_match.group(1)

    # Швидкість
    sp_match = re.search(r"(\d+\.?\d*)\s*m/?min", text.lower())
    if sp_match:
        speed = sp_match.group(1)

    return material, thickness, speed, text


def save_params(material, thickness, speed):
    param = {
        "material": material,
        "thickness": thickness,
        "speed": speed
    }

    if not os.path.exists("learned_params.json"):
        with open("learned_params.json", "w") as f:
            json.dump([], f)

    with open("learned_params.json", "r") as f:
        data = json.load(f)

    data.append(param)

    with open("learned_params.json", "w") as f:
        json.dump(data, f, indent=4)