from materials_module import MATERIAL_MAP
from cut_params import CUT_PARAMS

print("=== Перевірка відповідності назв матеріалів ===\n")

map_names = set(MATERIAL_MAP.values())
cut_names = set(CUT_PARAMS.keys())

print("Назви в MATERIAL_MAP:")
for n in map_names:
    print(" -", n)

print("\nНазви в CUT_PARAMS:")
for n in cut_names:
    print(" -", n)

print("\n=== Результат ===")

missing_in_cut = map_names - cut_names
missing_in_map = cut_names - map_names

if not missing_in_cut and not missing_in_map:
    print("✔ Усі назви співпадають! Проблем немає.")
else:
    if missing_in_cut:
        print("\n❌ Є назви, які є в MATERIAL_MAP, але немає в CUT_PARAMS:")
        for n in missing_in_cut:
            print(" -", n)

    if missing_in_map:
        print("\n❌ Є назви, які є в CUT_PARAMS, але немає в MATERIAL_MAP:")
        for n in missing_in_map:
            print(" -", n)