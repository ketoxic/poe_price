from core.craft_cost import CraftMethod, print_comparison
from core.currency import load_currency_rate

rates = load_currency_rate("Keepers")

methods = [
    CraftMethod(
        "Harvest",
        {"Vivid Lifeforce": 9300}
    ),
    CraftMethod(
        "Alt+Aug",
        {
            "alt": 2767,
            "aug": 679
        }
    ),
    CraftMethod(
        "Alch + Scour",
        {
            "alc": 959,
            "scour": 958
        }
    )
]

print_comparison(methods, rates)