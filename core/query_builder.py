# core/query_builder.py

import json
from pathlib import Path

# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# (giữ lại nếu chỗ khác còn dùng, builder này thì không cần)
TRADE_STAT_MAP_FILE = DATA_DIR / "trade_stat_map.json"


# --------------------------------------------------
# BUILD STAT FILTER
# --------------------------------------------------

def stat_filter(mod: dict) -> dict:
    """
    Build trade stat filter directly from enriched affix.
    Assumes mod already has trade_stat_id.
    """
    trade_id = mod.get("trade_stat_id")

    if not trade_id:
        raise ValueError(f"Missing trade_stat_id for mod: {mod}")

    value = {}
    if mod.get("min") is not None:
        value["min"] = mod["min"]
    if mod.get("max") is not None:
        value["max"] = mod["max"]

    return {
        "id": trade_id,
        "disabled": False,
        "value": value
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
            "status": {"option": "securable"},   # 🔴 giữ nguyên như bạn yêu cầu
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


