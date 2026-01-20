import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LANG_FILE = DATA_DIR / "poec_lang.us.json"

TARGET_FILES = [
    DATA_DIR / "prefixes.json",
    DATA_DIR / "suffixes.json"
]


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def enrich_file(path, mod_dict):
    mods = load_json(path)
    updated = False

    for mod in mods:
        mod_id = str(mod["id"])
        text = mod_dict.get(mod_id)

        if text:
            mod["text"] = text
            updated = True
        else:
            mod["text"] = None
            print(f"[WARN] Missing mod text for id {mod_id}")

    if updated:
        save_json(path, mods)
        print(f"[OK] Overwritten {path.name}")
    else:
        print(f"[SKIP] No updates for {path.name}")


def main():
    lang_data = load_json(LANG_FILE)

    if "mod" not in lang_data:
        raise KeyError("poec_lang.us.json missing 'mod' section")

    mod_dict = lang_data["mod"]
    print(f"[INFO] Loaded {len(mod_dict)} mod texts")

    for file_path in TARGET_FILES:
        if file_path.exists():
            enrich_file(file_path, mod_dict)
        else:
            print(f"[SKIP] {file_path.name} not found")


if __name__ == "__main__":
    main()
