from dataclasses import dataclass
from typing import Dict, List, Tuple


# =========================================================
# ===================== CONFIG =============================
# =========================================================

CURRENCY_ALIAS = {
    "Vivid Lifeforce": "Vivid Crystallised Lifeforce",
    "Wild Lifeforce": "Wild Crystallised Lifeforce",
    "Primal Lifeforce": "Primal Crystallised Lifeforce",
    "alt": "Orb of Alteration",
    "aug": "Orb of Augmentation",
    "alc": "Orb of Alchemy",
    "scour": "Orb of Scouring"
}


# =========================================================
# ===================== DATA CLASS =========================
# =========================================================

@dataclass
class CraftMethod:
    name: str
    currency_usage: Dict[str, float]
    description: str = ""


# =========================================================
# ===================== CORE ===============================
# =========================================================

def resolve_currency_name(name: str) -> str:
    return CURRENCY_ALIAS.get(name, name)


def calculate_cost(method: CraftMethod, currency_rates: Dict[str, float]) -> float:
    if not currency_rates:
        raise ValueError("currency_rates is None or empty")

    total = 0.0

    for curr, amount in method.currency_usage.items():
        real_name = resolve_currency_name(curr)
        price = currency_rates.get(real_name)

        if price is None:
            print(f"[WARN] Missing price: {curr} ({real_name})")
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
    """
    Format cost into chaos + divine
    """
    chaos = round(cost, 2)

    divine_price = currency_rates.get("Divine Orb", 0)

    if divine_price > 0:
        divine = round(cost / divine_price, 2)
        return f"{chaos:.2f} chaos ({divine:.2f} div)"
    else:
        return f"{chaos:.2f} chaos"


# =========================================================
# ===================== PRINT ==============================
# =========================================================

def print_comparison(methods: List[CraftMethod], currency_rates: Dict[str, float]):
    results = compare_methods(methods, currency_rates)

    print("\n=== Craft Cost Comparison ===")

    for name, cost in results:
        formatted = format_cost(cost, currency_rates)
        print(f"{name:<20} : {formatted}")


def detailed_breakdown(method: CraftMethod, currency_rates: Dict[str, float]):
    print(f"\n=== {method.name} ===")

    total = 0.0

    for curr, amount in method.currency_usage.items():
        real_name = resolve_currency_name(curr)
        price = currency_rates.get(real_name, 0)

        cost = amount * price
        total += cost

        print(f"{real_name:<35} x {amount:<8} @ {price:<8.3f} = {cost:.2f}")

    print("-" * 60)
    print("TOTAL:", format_cost(total, currency_rates))