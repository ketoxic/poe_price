# core/trade_client.py

import requests
import json
from core.rate_limit import rate_limited

BASE_URL = "https://www.pathofexile.com/api/trade"
LEAGUE = "Keepers"   # đổi khi cần

HEADERS = {
    "User-Agent": "Ket",
    "From":"phuket_92@gmail.com"
}



class TradeClient:
    def __init__(self, league: str = LEAGUE):
        self.league = league
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    @rate_limited()
    def _post(self, url, json):
        return self.session.post(url, json=json)

    @rate_limited()
    def _get(self, url, params):
        return self.session.get(url, params=params)
    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------
    def search(self, query: dict):
        url = f"{BASE_URL}/search/{self.league}"

        resp = self._post(url, json=query)

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
        print("DEBUG status:", resp.status_code)
        print("DEBUG text:", resp.text[:200])
    # --------------------------------------------------
    # FETCH
    # --------------------------------------------------
    def fetch(self, item_id: str, search_id: str):
        url = f"{BASE_URL}/fetch/{item_id}"
        params = {"query": search_id}

        resp = self._get(url, params=params)
        resp.raise_for_status()

        data = resp.json()
        result = data.get("result", [])

        if not result:
            return None

        price = result[0]["listing"].get("price")
        if not price:
            return None

        return {
            "amount": price["amount"],
            "currency": price["currency"]
        }
