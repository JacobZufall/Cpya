"""
test_IntangibleAsset
"""

import unittest as ut

from src.pyacty.assets.IntangibleAsset import IntangibleAsset


class TestIntangibleAsset(ut.TestCase):
    def test_straight_line(self) -> None:
        asset_one: IntangibleAsset = IntangibleAsset("Test Asset", 10 * 12, 100_000)

        # Ensures that the properties were set and can be retrieved properly.
        self.assertEqual(asset_one.net_value, 100_000)
        self.assertEqual(asset_one.total_amort, 0)

        # Ensures that depreciate depreciates the correct amount.
        self.assertEqual(asset_one.amortize(0), 10_000)

        # Ensures that the properties were updated accordingly.
        self.assertEqual(asset_one.net_value, 90_000)
        self.assertEqual(asset_one.total_amort, 10_000)

        # Testing depreciation for two periods just to ensure it doesn't change.
        self.assertEqual(asset_one.amortize(0), 10_000)

        # Ensures that the properties were updated accordingly.
        self.assertEqual(asset_one.net_value, 80_000)
        self.assertEqual(asset_one.total_amort, 20_000)

    def test_declining_balance(self) -> None:
        asset_one: IntangibleAsset = IntangibleAsset("Test Asset", 10 * 12, 100_000)

        self.assertEqual(asset_one.net_value, 100_000)
        self.assertEqual(asset_one.total_amort, 0)

        self.assertEqual(asset_one.amortize(1, decline=2.0), 20_000)

        self.assertEqual(asset_one.net_value, 80_000)
        self.assertEqual(asset_one.total_amort, 20_000)

        self.assertEqual(asset_one.amortize(1, decline=2.0), 16_000)

        self.assertEqual(asset_one.net_value, 64_000)
        self.assertEqual(asset_one.total_amort, 36_000)


if __name__ == "__main__":
    ut.main()