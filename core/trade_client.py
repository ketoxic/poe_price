# core/trade_client.py

import requests
import json

BASE_URL = "https://www.pathofexile.com/api/trade"
LEAGUE = "Settlers"   # đổi khi cần

HEADERS = {
    "User-Agent": "poe-price-checker/1.0",
    "Accept": "application/json",
    "Content-Type": "application/json"
}



class TradeClient:
    def __init__(self, league: str = LEAGUE):
        self.league = league
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------
    def search(self, query: dict):
        """
        POST /api/trade/search/{league}

        Returns:
            (search_id, first_item_id) or (None, None)
        """
        url = f"{BASE_URL}/search/{self.league}"

        resp = self.session.post(url, json=query)

        if resp.status_code != 200:
            print("=== QUERY SENT ===")
            print(json.dumps(query, indent=2, ensure_ascii=False))
            print("=== RESPONSE FROM TRADE ===")
            print(resp.text)
            resp.raise_for_status()

        data = resp.json()

        result_ids = data.get("result", [])
        if not result_ids:
            return data["id"], None

        return data["id"], result_ids[0]

    # --------------------------------------------------
    # FETCH
    # --------------------------------------------------
    def fetch(self, item_id: str, search_id: str):
        """
        GET /api/trade/fetch/{item_id}?query={search_id}

        Returns:
            {
              price: float,
              currency: str
            }
            or None
        """
        url = f"{BASE_URL}/fetch/{item_id}"
        params = {
            "query": search_id
        }

        resp = self.session.get(url, params=params)
        resp.raise_for_status()

        data = resp.json()
        result = data.get("result", [])

        if not result:
            return None

        listing = result[0]["listing"]
        price = listing.get("price")

        if not price:
            return None

        return {
            "amount": price["amount"],
            "currency": price["currency"]
        }
