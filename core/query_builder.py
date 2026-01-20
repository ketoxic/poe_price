import json
from pathlib import Path
from core.trade_stat_map import get_trade_stat_id

# --------------------------------------------------
# LOAD TRADE STAT MAP
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

TRADE_STAT_MAP_FILE = DATA_DIR / "trade_stat_map.json"

with open(TRADE_STAT_MAP_FILE, "r", encoding="utf-8") as f:
    TRADE_STAT_MAP = json.load(f)


def normalize_text(text: str) -> str:
    return (
        text.lower()
        .replace("  ", " ")
        .strip()
    )



# --------------------------------------------------
# BUILD STAT FILTER
# --------------------------------------------------

def stat_filter(mod: dict) -> dict:
    trade_id = get_trade_stat_id(mod["text"])

    return {
        "id": trade_id,
        "disabled": False,
        "value": {
            "min": mod["min"]
        }
    }



# --------------------------------------------------
# BUILD QUERY (FLASK)
# --------------------------------------------------

def build_query(flask_name: str, prefix: dict, suffix: dict) -> dict:
    filters = []

    if prefix:
        filters.append(stat_filter(prefix))
    if suffix:
        filters.append(stat_filter(suffix))

    return {
        "query": {
            "status": {"option": "securable"},   # 🔴 BẮT BUỘC
            "type": flask_name,
            "stats": [
                {
                    "type": "and",
                    "filters": filters,
                    "disabled": False
                }
            ]
        },
        "sort": {"price": "asc"}
    }
