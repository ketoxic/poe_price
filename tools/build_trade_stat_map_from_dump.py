import json
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DUMP_FILE = DATA_DIR / "trade_stats_dump.json"
OUT_FILE = DATA_DIR / "trade_stat_map.json"



def normalize_text(text: str) -> str:
    text = text.lower()

    # bỏ nội dung trong ngoặc (nếu có)
    text = re.sub(r"\([^)]*\)", "", text)

    # bỏ ký hiệu đặc biệt
    text = text.replace("+", "")
    text = text.replace("#", "")
    text = text.replace("%", "")
    text = text.replace(",", "")

    # chuẩn hóa khoảng trắng
    text = re.sub(r"\s+", " ", text)

    return text.strip()




def main():
    if not DUMP_FILE.exists():
        raise FileNotFoundError(f"Missing {DUMP_FILE}")

    with open(DUMP_FILE, "r", encoding="utf-8") as f:
        dump = json.load(f)

    trade_map = {}

    for group in dump.get("result", []):
        for entry in group.get("entries", []):
            if entry.get("type") != "explicit":
                continue  # ← CHỈ LẤY explicit

            stat_id = entry.get("id")
            text = entry.get("text")

            if not stat_id or not text:
                continue

            trade_map[normalize_text(text)] = stat_id

    OUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(trade_map, f, indent=2, ensure_ascii=False)

    print(f"[DONE] Saved {len(trade_map)} trade stat ids")
    print(f"→ {OUT_FILE}")


if __name__ == "__main__":
    main()
