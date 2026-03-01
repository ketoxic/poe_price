from dataclasses import dataclass
from typing import Dict, List, Tuple
from pathlib import Path
import json


# =========================================================
# ===================== LOAD MAPPING ======================
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]
MAP_PATH = BASE_DIR / "data" / "currency_map_auto.json"

if MAP_PATH.exists():
    with open(MAP_PATH, "r", encoding="utf-8") as f:
        FULLNAME_TO_ID = json.load(f)
else:
    FULLNAME_TO_ID = {}
    print("[WARN] currency_map_auto.json not found")


# =========================================================
# ===================== DATA CLASS =========================
# =========================================================

@dataclass
class CraftMethod:
    name: str
    currency_usage: Dict[str, float]
    description: str = ""


# =========================================================
# ===================== UTIL ===============================
# =========================================================

def resolve_currency_name(name: str, currency_rates: Dict[str, float]) -> str:
    """
    Try auto-detect:
    1) Exact exchange id
    2) Full name mapping
    3) Case-insensitive match
    4) Fuzzy partial match
    """

    name_lower = name.lower()

    # 1️⃣ Already exchange id
    if name_lower in currency_rates:
        return name_lower

    # 2️⃣ Full name mapping
    if name in FULLNAME_TO_ID:
        return FULLNAME_TO_ID[name]

    # 3️⃣ Case-insensitive full name
    for full_name, cid in FULLNAME_TO_ID.items():
        if full_name.lower() == name_lower:
            return cid

    # 4️⃣ Partial match (for Lifeforce etc)
    for full_name, cid in FULLNAME_TO_ID.items():
        if name_lower in full_name.lower():
            return cid

    print(f"[WARN] Could not resolve currency: {name}")
    return name_lower


# =========================================================
# ===================== CORE ===============================
# =========================================================

def calculate_cost(method: CraftMethod, currency_rates: Dict[str, float]) -> float:
    total = 0.0

    for curr, amount in method.currency_usage.items():
        currency_id = resolve_currency_name(curr, currency_rates)
        price = currency_rates.get(currency_id)

        if price is None:
            print(f"[WARN] Missing price: {curr} -> {currency_id}")
            continue

        total += amount * price

    return total


def compare_methods(
    methods: List[CraftMethod],
    currency_rates: Dict[str, float]
) -> List[Tuple[str, float]]:
    results = []

    for m in methods:
        cost = calculate_cost(m, currency_rates)
        results.append((m.name, cost))

    return sorted(results, key=lambda x: x[1])


# =========================================================
# ===================== FORMAT =============================
# =========================================================

def format_cost(cost: float, currency_rates: Dict[str, float]) -> str:
    chaos = round(cost, 2)

    divine_price = currency_rates.get("divine", 0)

    if divine_price > 0:
        divine = round(cost / divine_price, 2)
        return f"{chaos:.2f} chaos ({divine:.2f} div)"
    else:
        return f"{chaos:.2f} chaos"


# =========================================================
# ===================== PRINT ==============================
# =========================================================

def print_comparison(methods, currency_rates):
    divine_rate = currency_rates.get("divine")

    # ---- Thu thập currency đang dùng ----
    used_ids = set()
    for method in methods:
        for curr in method.currency_usage:
            cid = resolve_currency_name(curr, currency_rates)
            used_ids.add(cid)

    # ---- In rate các currency liên quan (có reverse) ----
    print("\n=== Currency Rates ===")

    for cid in sorted(used_ids):
        if cid not in currency_rates or cid == "chaos":
            continue

        rate = currency_rates[cid]

        if rate > 0:
            reverse = 1 / rate
            print(
                f"[RATE] 1 {cid:<15} = {rate:>10.4f} chaos | "
                f"1 chaos = {reverse:>10.4f} {cid}"
            )

    # ---- Tính cost trước để sort ----
    results = []
    for method in methods:
        total = calculate_cost(method, currency_rates)
        results.append((method, total))

    results.sort(key=lambda x: x[1])  # thấp → cao

    print("\n=== Craft Cost Comparison ===")

    for method, total in results:
        divine = total / divine_rate if divine_rate else 0

        print(
            f"{method.name:<20}: "
            f"{total:>10.2f} chaos "
            f"({divine:>6.2f} div)"
        )

def detailed_breakdown(method: CraftMethod, currency_rates: Dict[str, float]):
    print(f"\n=== {method.name} ===")

    total = 0.0

    for curr, amount in method.currency_usage.items():
        currency_id = resolve_currency_name(curr)
        price = currency_rates.get(currency_id, 0)

        cost = amount * price
        total += cost

        print(f"{currency_id:<30} x {amount:<8} @ {price:<8.3f} = {cost:.2f}")

    print("-" * 60)
    print("TOTAL:", format_cost(total, currency_rates))