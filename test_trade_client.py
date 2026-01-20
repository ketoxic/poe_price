import json
from core.query_builder import build_query
from core.trade_client import TradeClient

def main():
    client = TradeClient()

    query = build_query(
        flask_name="Quicksilver Flask",
        prefix={
            "text": "#% increased Effect",
            "min": 25,
            "max": None
        },
        suffix={
            "text": "#% increased Movement Speed during Effect",
            "min": 14,
            "max": None
        }
    )

    print("=== QUERY SENT ===")
    print(json.dumps(query, indent=2))

    search_id, item_id = client.search(query)

    print("\nsearch_id:", search_id)
    print("item_id:", item_id)

    if not item_id:
        print("❌ No item found")
        return

    price = client.fetch(item_id, search_id)
    print("\nprice:", price)


if __name__ == "__main__":
    main()
