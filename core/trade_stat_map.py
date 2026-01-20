import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MAP_FILE = os.path.join(BASE_DIR, "data", "trade_stat_map.json")

_trade_stat_map = None


def load_trade_stat_map():
    global _trade_stat_map
    if _trade_stat_map is None:
        with open(MAP_FILE, "r", encoding="utf-8") as f:
            _trade_stat_map = json.load(f)
    return _trade_stat_map




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


def get_trade_stat_id(mod_text: str) -> str:
    trade_map = load_trade_stat_map()
    key = normalize_text(mod_text)

    if key not in trade_map:
        raise KeyError(f"Trade stat id not found for: {mod_text}")

    return trade_map[key]
