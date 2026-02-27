# core/currency.py

import requests
from typing import Optional

POE_NINJA_URL = "https://poe.ninja/api/data/currencyoverview"

_DIVINE_TO_CHAOS = None


def load_currency_rate(league: str):
    url = "https://poe.ninja/api/data/currencyoverview"
    params = {
        "league": league,
        "type": "Currency"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"[ERROR] Failed to fetch currency data: {e}")
        return {}

    rates = {}

    try:
        lines = data.get("lines", [])

        for item in lines:
            name = item.get("currencyTypeName")
            chaos = item.get("chaosEquivalent")

            if name and chaos is not None:
                rates[name] = chaos

    except Exception as e:
        print(f"[ERROR] Failed to parse currency data: {e}")
        return {}

    # debug info
    divine = rates.get("Divine Orb")
    if divine:
        print(f"[RATE] 1 Divine Orb = {divine:.2f} chaos")

    return rates

def to_chaos(amount: float, currency: str) -> Optional[float]:
    if currency == "chaos":
        return amount

    if currency == "divine":
        if _DIVINE_TO_CHAOS is None:
            raise RuntimeError("Currency rate not loaded")
        return amount * _DIVINE_TO_CHAOS

    return None
