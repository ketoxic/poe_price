import requests
import json

LEAGUE = "Keepers"

API = "https://poe.ninja/poe1/api/economy/exchange/current/overview"


def main():
    print("=== TEST EXCHANGE CURRENT API ===\n")

    r = requests.get(API, params={
        "league": LEAGUE,
        "type": "Currency"
    }, timeout=10)

    r.raise_for_status()
    data = r.json()

    print("TOP LEVEL KEYS:", data.keys())

    lines = data.get("lines", [])
    print("TOTAL CURRENCIES RETURNED:", len(lines))

    print("\n=== ALL IDS RETURNED ===\n")
    ids = sorted([item.get("id") for item in lines if item.get("id")])
    for cid in ids:
        print(cid)

    print("\n=== CHECK SPECIFIC CURRENCIES ===\n")
    targets = [
        "divine",
        "chaos",
        "alteration",
        "augmentation",
        "alchemy",
        "scouring"
    ]

    id_set = set(ids)

    for t in targets:
        print(f"{t:<15} ->", "FOUND" if t in id_set else "MISSING")

    print("\n=== SAMPLE ENTRY (DIVINE IF EXISTS) ===\n")
    for item in lines:
        if item.get("id") == "divine":
            print(json.dumps(item, indent=2))
            break


if __name__ == "__main__":
    main()