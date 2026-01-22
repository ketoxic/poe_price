# core/currency.py

import requests
from typing import Optional

POE_NINJA_URL = "https://poe.ninja/api/data/currencyoverview"

_DIVINE_TO_CHAOS = None


def load_currency_rate(league: str):
    global _DIVINE_TO_CHAOS

    params = {
        "league": league,
        "type": "Currency"
    }

    resp = requests.get(POE_NINJA_URL, params=params, timeout=10)
    resp.raise_for_status()

    data = resp.json()

    for line in data.get("lines", []):
        if line.get("currencyTypeName") == "Divine Orb":
            _DIVINE_TO_CHAOS = line["chaosEquivalent"]
            print(f"[RATE] 1 Divine = {_DIVINE_TO_CHAOS} chaos")
            return

    raise RuntimeError("Divine Orb rate not found from poe.ninja")


def to_chaos(amount: float, currency: str) -> Optional[float]:
    if currency == "chaos":
        return amount

    if currency == "divine":
        if _DIVINE_TO_CHAOS is None:
            raise RuntimeError("Currency rate not loaded")
        return amount * _DIVINE_TO_CHAOS

    return None
