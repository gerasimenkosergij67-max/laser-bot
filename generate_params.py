import json

# Матеріали, газ і базова логіка
materials = {
    "steel":     {"gas": "O2"},
    "stainless": {"gas": "N2"},
    "aluminum":  {"gas": "N2"},
    "copper":    {"gas": "N2"},
    "brass":     {"gas": "N2"},
    "bronze":    {"gas": "N2"},
}

powers = ["1.5", "3", "6"]

thicknesses = [
    "0.5", "0.8",
    "1", "1.2", "1.5",
    "2", "2.5",
    "3", "4", "5", "6",
    "8", "10", "12", "15", "20"
]

data = {}

for m, m_info in materials.items():
    gas = m_info["gas"]
    for p in powers:
        for t in thicknesses:
            th = float(t)
            pw = float(p)

            # Примірна швидкість: чим більше потужність і менша товщина — тим швидше
            base = 4500 if m == "steel" else 3500
            speed = int(base * (pw / 3.0) * (1.0 / (1.0 + (th - 1) * 0.25)))
            if speed < 200:
                speed = 200

            # Фокус: для сталі 0, для нерж/кольорових -1
            if m == "steel":
                focus = "0"
            else:
                focus = "-1"

            # Сопло: росте з товщиною
            if th <= 1:
                nozzle = "1.0"
            elif th <= 3:
                nozzle = "1.2"
            elif th <= 6:
                nozzle = "1.5"
            elif th <= 10:
                nozzle = "2.0"
            else:
                nozzle = "2.5"

            # Тиск: для O2 менший, для N2 більший
            if gas == "O2":
                if th <= 2:
                    pressure = "1.0"
                elif th <= 5:
                    pressure = "1.5"
                elif th <= 10:
                    pressure = "2.5"
                else:
                    pressure = "4.0"
            else:  # N2
                if th <= 2:
                    pressure = "10"
                elif th <= 5:
                    pressure = "14"
                elif th <= 10:
                    pressure = "18"
                else:
                    pressure = "22"

            key = f"{m}_{p}_{t}"
            data[key] = {
                "speed": str(speed),
                "focus": focus,
                "nozzle": nozzle,
                "pressure": pressure,
                "gas": gas
            }

with open("params.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Готово: створено params.json з приблизними параметрами.")