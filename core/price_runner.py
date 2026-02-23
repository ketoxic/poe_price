import json
from pathlib import Path

from core.trade_client import TradeClient
from core.query_builder import build_query
from core.combo_builder import build_combos
from tools.export_to_excel import export_price_to_excel
from core.currency import load_currency_rate


BASE_DIR = Path(__file__).resolve().parent.parent
RESULT_DIR = BASE_DIR / "result"
RESULT_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# utils
# --------------------------------------------------
def save_results(result_map, out_file: Path, log_hook=None):
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(list(result_map.values()), f, indent=2, ensure_ascii=False)

    msg = f"💾 Saved {len(result_map)} results to {out_file.name}"

    if log_hook:
        log_hook(msg)
    else:
        print(msg)


# --------------------------------------------------
# main
# --------------------------------------------------
def run_price_check(
    item_file: Path = None,
    only_items=None,
    items=None,
    log_hook=None,
    should_stop=None
):
    client = TradeClient()

    def log(msg):
        if log_hook:
            log_hook(msg)
        else:
            print(msg)

    # load rate
    load_currency_rate(client.league)

    # --------------------------------------------------
    # load item list
    # --------------------------------------------------
    if items is not None:
        final_items = items
    else:
        with open(item_file, "r", encoding="utf-8") as f:
            final_items = json.load(f)

        if only_items:
            final_items = [i for i in final_items if i in only_items]

    combos = build_combos()

    if item_file:
        out_file = RESULT_DIR / f"{item_file.stem}_price.json"
    else:
        out_file = RESULT_DIR / "custom_price.json"

    # --------------------------------------------------
    # LOAD OLD RESULTS
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
    for item_name in final_items:
        if should_stop and should_stop():
            log("⛔ Stopped by user")
            return

        log(f"\n=== CHECKING {item_name} ===")

        for prefix, suffix in combos:
            if should_stop and should_stop():
                log("⛔ Stopped by user")
                return

            try:
                query = build_query(item_name, prefix, suffix)
                search_id, item_id = client.search(query)

                key = (item_name, prefix["text"], suffix["text"])

                # ❌ không có người bán → giá = 0
                if not item_id:
                    log(
                        f"[PRICE] {item_name} | "
                        f"{prefix['text']} + {suffix['text']} "
                        f"=> 0 chaos"
                    )

                    result_map[key] = {
                        "item": item_name,
                        "prefix": prefix["text"],
                        "suffix": suffix["text"],
                        "price": {
                            "amount": 0,
                            "currency": "chaos"
                        }
                    }
                    continue

                # -------------------------------
                # fetch price
                # -------------------------------
                price = client.fetch(item_id, search_id)

                if price is None:
                    continue

                msg = (
                    f"[PRICE] {item_name} | "
                    f"{prefix['text']} + {suffix['text']} "
                    f"=> {price['amount']} {price['currency']}"
                )

                log(msg)

                result_map[key] = {
                    "item": item_name,
                    "prefix": prefix["text"],
                    "suffix": suffix["text"],
                    "price": price
                }

            except Exception as e:
                log("❌ ERROR combo:")
                log(f"{item_name} | {prefix['text']} | {suffix['text']}")
                log(str(e))

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------
    save_results(result_map, out_file, log_hook=log_hook)

    # optional export excel
    try:
        export_price_to_excel(out_file)
        log("📊 Exported to Excel")
    except Exception as e:
        log(f"⚠️ Excel export failed: {e}")