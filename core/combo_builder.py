# core/combo_builder.py

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

PREFIX_FILE = DATA_DIR / "prefixes.json"
SUFFIX_FILE = DATA_DIR / "suffixes.json"


def load_affix(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_combos():
    prefixes = load_affix(PREFIX_FILE)
    suffixes = load_affix(SUFFIX_FILE)

    combos = []

    for p in prefixes:
        for s in suffixes:
            combos.append((p, s))

    return combos
