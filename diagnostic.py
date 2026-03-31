import sys
import os

print("=== DIAGNOSTIC STARTED ===")

# --------------------------
# 1. Перевірка Python
# --------------------------
print(f"Python version: {sys.version}")

# --------------------------
# 2. Перевірка токена
# --------------------------
TOKEN = "8723535602:AAHM_9VBMBLu6mM_VfkvEgi885Sv_D4OhmE"

if not TOKEN or len(TOKEN) < 20:
    print("❌ TOKEN ERROR: Token is empty or invalid format")
else:
    print("✔ TOKEN OK (format valid)")

# --------------------------
# 3. Перевірка імпортів
# --------------------------
print("\nChecking imports...")

modules = [
    "telegram",
    "telegram.ext",
    "pytesseract",
    "PIL",
]

for m in modules:
    try:
        __import__(m)
        print(f"✔ {m} OK")
    except Exception as e:
        print(f"❌ {m} ERROR:", e)

# --------------------------
# 4. Перевірка Tesseract
# --------------------------
print("\nChecking Tesseract...")

import shutil
tess = shutil.which("tesseract")

if tess:
    print(f"✔ Tesseract found at: {tess}")
else:
    print("❌ Tesseract NOT FOUND")
    print("Install from: https://github.com/UB-Mannheim/tesseract/wiki")

# --------------------------
# 5. Перевірка запуску Telegram Application
# --------------------------
print("\nChecking Telegram bot startup...")

try:
    from telegram.ext import ApplicationBuilder
    app = ApplicationBuilder().token(TOKEN).build()
    print("✔ Telegram Application created successfully")
except Exception as e:
    print("❌ ERROR creating Telegram Application:")
    print(e)
    sys.exit()

print("\n=== DIAGNOSTIC FINISHED ===")