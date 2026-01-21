# core/price_runner.py

import json
from pathlib import Path
from core.combo_builder import build_combos
from core.query_builder import build_query
from core.trade_client import TradeClient

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

OUTPUT_FILE = DATA_DIR / "price_result.json"


def run_price_check(flask_name: str):
    client = TradeClient()
    combos = build_combos()

    results = []

    for prefix, suffix in combos:
        try:
            query = build_query(flask_name, prefix, suffix)
            search_id, item_id = client.search(query)

            if not item_id:
                continue

            price = client.fetch(item_id, search_id)
            if not price:
                continue

            print(
                f"[PRICE] {flask_name} | "
                f"{prefix['text']} + {suffix['text']} "
                f"=> {price['amount']} {price['currency']}"
            )

            results.append({
                "flask": flask_name,
                "prefix": prefix["text"],
                "suffix": suffix["text"],
                "price": price
            })

        except Exception as e:
            print("❌ ERROR combo:")
            print(prefix["text"], "|", suffix["text"])
            print(e)

    # ghi đè mỗi lần chạy
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(results)} results to {OUTPUT_FILE}")
