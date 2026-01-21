import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DUMP_FILE = os.path.join(BASE_DIR, "data", "trade_stats_dump.json")
OUT_FILE = os.path.join(BASE_DIR, "data", "trade_stat_map.json")


def main():
    with open(DUMP_FILE, "r", encoding="utf-8") as f:
        dump = json.load(f)

    trade_map = {}

    for group in dump.get("result", []):
        for entry in group.get("entries", []):
            # bạn chỉ muốn explicit
            if entry.get("type") != "explicit":
                continue

            text = entry.get("text")
            stat_id = entry.get("id")

            if not text or not stat_id:
                continue

            trade_map.setdefault(text, []).append({
                "id": stat_id,
                "type": entry.get("type")
            })

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(trade_map, f, indent=2, ensure_ascii=False)

    print(f"[OK] Written {OUT_FILE} ({len(trade_map)} texts)")


if __name__ == "__main__":
    main()
