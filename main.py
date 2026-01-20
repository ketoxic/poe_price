# main.py

import json
from pathlib import Path
from core.query_generator import generate_queries


DATA_DIR = Path("data")
OUT_DIR = Path("out/queries")


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    flasks = load_json(DATA_DIR / "flasks.json")
    prefixes = load_json(DATA_DIR / "prefixes.json")
    suffixes = load_json(DATA_DIR / "suffixes.json")

    queries = generate_queries(flasks, prefixes, suffixes)

    print(f"Total queries: {len(queries)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for i, entry in enumerate(queries, start=1):
        out_file = OUT_DIR / f"query_{i:03}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
