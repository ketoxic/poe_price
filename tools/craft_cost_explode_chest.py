from core.craft_cost import CraftMethod, print_comparison
from core.currency import load_currency_rate

rates = load_currency_rate("Keepers")

methods = [
    CraftMethod(
        "Reforge defense",
        {
            "vivid": 9300
        }
    ),
    CraftMethod(
        "Alt + Aug",
        {
            "alt": 2767,
            "aug": 679
        }
    ),
    CraftMethod(
        "Alch + Scour",
        {
            "alch": 963,
            "scour": 963
        }
    ),
    CraftMethod(
        "Chaos",
        {
            "chaos": 963
        }
    )
]

print_comparison(methods, rates)