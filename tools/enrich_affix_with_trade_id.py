# tools/enrich_affix_with_trade_id.py

import json
import os

# =========================
# PATHS
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

AFFIX_FILES = [
    os.path.join(BASE_DIR, "data", "prefixes.json"),
    os.path.join(BASE_DIR, "data", "suffixes.json"),
]

TRADE_STAT_MAP_FILE = os.path.join(
    BASE_DIR, "data", "trade_stat_map.json"
)

# =========================
# LOAD TRADE STAT MAP
# =========================

with open(TRADE_STAT_MAP_FILE, "r", encoding="utf-8") as f:
    TRADE_STAT_MAP = json.load(f)

# =========================
# ENRICH FUNCTION
# =========================

def enrich_affix_file(path: str):
    print(f"\n[PROCESS] {os.path.basename(path)}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for mod in data:
        text = mod.get("text")
        if not text:
            mod["trade_stat_id"] = None
            continue

        candidates = TRADE_STAT_MAP.get(text)

        if not candidates:
            mod["trade_stat_id"] = None
            print(f"[MISS] {text}")

        elif len(candidates) == 1:
            mod["trade_stat_id"] = candidates[0]["id"]
            print(f"[OK] {text} -> {mod['trade_stat_id']}")

        else:
            # nhiều trade stat cho cùng text → để user tự xử
            mod["trade_stat_id"] = None
            print(f"[AMBIGUOUS] {text} ({len(candidates)} candidates)")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[DONE] {os.path.basename(path)} written")


# =========================
# MAIN
# =========================

def main():
    for path in AFFIX_FILES:
        enrich_affix_file(path)


if __name__ == "__main__":
    main()
