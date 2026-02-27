# core/currency.py

import requests
from typing import Optional

POE_NINJA_URL = "https://poe.ninja/poe1/api/economy/exchange/current/overview"

_RATES = {}


def load_currency_rate(league: str):
    global _RATES

    params = {
        "league": league,
        "type": "Currency"
    }

    try:
        response = requests.get(POE_NINJA_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"[ERROR] Failed to fetch currency data: {e}")
        return {}

    rates = {}

    try:
        lines = data.get("lines", [])

        for item in lines:
            currency_id = item.get("id")              # e.g. "divine"
            chaos_price = item.get("primaryValue")   # giá chaos

            if currency_id and chaos_price is not None:
                rates[currency_id.lower()] = chaos_price

        _RATES = rates

    except Exception as e:
        print(f"[ERROR] Failed to parse currency data: {e}")
        return {}

    # Debug divine
    divine_rate = _RATES.get("divine")
    if divine_rate:
        print(f"[RATE] 1 Divine Orb = {divine_rate:.2f} chaos")

    return _RATES


def to_chaos(amount: float, currency: str) -> Optional[float]:
    if not _RATES:
        raise RuntimeError("Currency rate not loaded")

    currency = currency.lower()

    # chaos passthrough
    if currency == "chaos":
        return amount

    rate = _RATES.get(currency)

    if rate is None:
        return None

    return amount * rate