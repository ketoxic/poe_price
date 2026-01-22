import json
from pathlib import Path
from openpyxl import Workbook


def export_price_to_excel(json_file: Path):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    wb = Workbook()
    ws = wb.active
    ws.title = "Prices"

    # header
    ws.append([
        "Item",
        "Prefix",
        "Suffix",
        "Price",
        "Currency"
    ])

    for row in data:
        price = row.get("price", {})
        ws.append([
            row.get("item"),
            row.get("prefix"),
            row.get("suffix"),
            price.get("amount"),
            price.get("currency")
        ])

    out_file = json_file.with_suffix(".xlsx")
    wb.save(out_file)

    print(f"📊 Exported Excel: {out_file.name}")
