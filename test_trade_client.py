import json
from core.trade_client import TradeClient


def main():
    client = TradeClient()

    # build query thủ công, bám sát query mẫu chạy được trên web
    query = {
        "query": {
            "status": {"option": "securable"},
            "type": "Quicksilver Flask",
            "stats": [
                {
                    "type": "and",
                    "filters": [
                        {
                            "id": "explicit.stat_2448920197",  # increased effect
                            "value": {"min": 25},
                            "disabled": False
                        },
                        {
                            "id": "explicit.stat_3182498570",  # movement speed
                            "value": {"min": 14},
                            "disabled": False
                        },
                        {
                            "id": "explicit.stat_3529940209",  # reduced duration (stat còn lại)
                            "disabled": True
                        }
                    ],
                    "disabled": False
                }
            ]
        },
        "sort": {"price": "asc"},
        "size": 1
    }

    print("=== QUERY SENT ===")
    print(json.dumps(query, indent=2, ensure_ascii=False))

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
