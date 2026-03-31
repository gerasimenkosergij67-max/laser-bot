import os
import json

def save_user_photo(user_id, file_id):
    folder = "photo_library"
    os.makedirs(folder, exist_ok=True)

    filename = os.path.join(folder, f"{user_id}_photo.json")

    data = {"file_id": file_id}

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)