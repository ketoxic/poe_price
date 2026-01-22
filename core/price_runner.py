# core/price_runner.py

import json
from pathlib import Path

from core.trade_client import TradeClient
from core.query_builder import build_query
from core.combo_builder import build_combos
from tools.export_to_excel import export_price_to_excel
from core.currency import load_currency_rate
from core.trade_client import TradeClient


BASE_DIR = Path(__file__).resolve().parent.parent
RESULT_DIR = BASE_DIR / "result"
RESULT_DIR.mkdir(exist_ok=True)



def save_results(result_map, out_file: Path):
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(list(result_map.values()), f, indent=2, ensure_ascii=False)

    print(f"💾 Saved {len(result_map)} results to {out_file.name}")


def run_price_check(item_file: Path, only_items=None):
    client = TradeClient()

    # load rate
    load_currency_rate(client.league)

    # load item list
    with open(item_file, "r", encoding="utf-8") as f:
        items = json.load(f)

    if only_items:
        items = [i for i in items if i in only_items]

    # prefix × suffix
    combos = build_combos()

    # output file name theo item file
    out_file = RESULT_DIR / f"{item_file.stem}_price.json"

    # --------------------------------------------------
    # LOAD OLD RESULTS (ghi đè combo cũ)
    # --------------------------------------------------
    if out_file.exists():
        with open(out_file, "r", encoding="utf-8") as f:
            old_results = json.load(f)
    else:
        old_results = []

    result_map = {
        (r["item"], r["prefix"], r["suffix"]): r
        for r in old_results
    }

    # --------------------------------------------------
    # RUN
    # --------------------------------------------------
    for item_name in items:
        print(f"\n=== CHECKING {item_name} ===")

        for prefix, suffix in combos:
            try:
                query = build_query(item_name, prefix, suffix)
                search_id, item_id = client.search(query)

                if not item_id:
                    continue

                price = client.fetch(item_id, search_id)
                if not price:
                    continue

                print(
                    f"[PRICE] {item_name} | "
                    f"{prefix['text']} + {suffix['text']} "
                    f"=> {price['amount']} {price['currency']}"
                )

                key = (item_name, prefix["text"], suffix["text"])
                result_map[key] = {
                    "item": item_name,
                    "prefix": prefix["text"],
                    "suffix": suffix["text"],
                    "price": price
                }

            except Exception as e:
                print("❌ ERROR combo:")
                print(item_name, "|", prefix["text"], "|", suffix["text"])
                print(e)

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------
    save_results(result_map, out_file)

