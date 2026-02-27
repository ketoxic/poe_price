import requests
import json
from pathlib import Path

LEAGUE = "Keepers"
API = "https://poe.ninja/poe1/api/economy/exchange/current/overview"


def main():
    print("Fetching exchange API...")

    r = requests.get(API, params={
        "league": LEAGUE,
        "type": "Currency"
    }, timeout=15)

    r.raise_for_status()
    data = r.json()

    lines = data.get("lines", [])
    items = data.get("items", [])

    print(f"Found {len(lines)} currencies")

    # =========================
    # Build id -> full name map
    # =========================
    id_to_name = {}

    for item in items:
        cid = item.get("id")
        name = item.get("name")

        if cid and name:
            id_to_name[cid] = name

    # =========================
    # Build fullname -> id map
    # =========================
    fullname_to_id = {}

    for line in lines:
        cid = line.get("id")
        if not cid:
            continue

        name = id_to_name.get(cid)

        if name:
            fullname_to_id[name] = cid

    print(f"Built mapping for {len(fullname_to_id)} entries")

    # =========================
    # Save to data folder
    # =========================
    base_dir = Path(__file__).resolve().parents[1]  # poe_price/
    data_dir = base_dir / "data"
    data_dir.mkdir(exist_ok=True)

    output_path = data_dir / "currency_map_auto.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(fullname_to_id, f, indent=2, ensure_ascii=False)

    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()