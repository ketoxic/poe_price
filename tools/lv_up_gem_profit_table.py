import requests

LEAGUE = "Mirage"
URL = f"https://poe.ninja/api/data/itemoverview?league={LEAGUE}&type=SkillGem"


def get_gem_group(data):
    groups = {}

    for g in data:
        if g.get("corrupted", False):
            continue

        name = g["name"]

        if name not in groups:
            groups[name] = []

        groups[name].append(g)

    return groups


def find_price(gems, level, quality):
    for g in gems:
        if g.get("gemLevel") == level and g.get("gemQuality", 0) == quality:
            return g["chaosValue"]
    return None


def get_max_level(gems):
    return max(g.get("gemLevel", 0) for g in gems)


def scan_all():
    data = requests.get(URL).json()["lines"]
    groups = get_gem_group(data)

    results = []

    for name, gems in groups.items():
        lv1 = find_price(gems, 1, 0)
        if lv1 is None:
            continue

        max_lv = get_max_level(gems)

        target_price = None
        label = ""

        # ===== logic theo max level =====
        if max_lv >= 20:
            target_price = find_price(gems, 20, 20)
            label = "Lv20(20q)"

        else:
            # gem kiểu 3 hoặc 4
            target_price = find_price(gems, max_lv, 0)
            label = f"Lv{max_lv}"

        if target_price is None:
            continue

        profit = target_price - lv1

        results.append({
            "name": name,
            "lv1": lv1,
            "target": target_price,
            "label": label,
            "profit": profit
        })

    results.sort(key=lambda x: x["profit"], reverse=True)

    return results[:10]


def print_table(results):
    print(f"{'Gem':35} {'Lv1':>10} {'Target':>12} {'Profit':>10}")
    print("-" * 75)

    for r in results:
        print(
            f"{r['name']:35} "
            f"{r['lv1']:10.1f} "
            f"{r['target']:10.1f} {r['label']:>6} "
            f"{r['profit']:10.1f}"
        )


# ===== MAIN =====
if __name__ == "__main__":
    print("Loading data...\n")

    top = scan_all()

    print("=== TOP 10 PROFIT GEM (AUTO MAX LEVEL) ===")
    print_table(top)
