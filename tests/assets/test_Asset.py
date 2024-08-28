"""
test_Asset.py
"""

from src.pyacty.assets.Asset import Asset
from src.pyacty.fundamentals.Money import Money

if __name__ == "__main__":
    asset_one: Asset = Asset("Chapstick", 5, 50_000)
    asset_two: Asset = Asset("Water", 10, 100_000)
    print(asset_one._value)
    print(asset_two._value)

    Money.show_decimals = True

    print(asset_one._value)
    print(asset_two._value)
