"""
test_Asset.py
"""

import unittest as ut

from src.pyacty.assets.Asset import Asset

asset_one: Asset = Asset("Test Asset", 10 * 12, 100_000)


class TestAsset(ut.TestCase):
    def test_properties(self) -> None:
        asset_one.reset()

        self.assertEqual(asset_one.value, 100_000)
        self.assertEqual(asset_one.life, 120)
        self.assertEqual(asset_one.rem_life, 120)

        asset_one.value = 50_000
        asset_one.life = 5 * 12

        self.assertEqual(asset_one.value, 50_000)
        # life and rem_life aren't always equal, as rem_life is changed when the TangibleAsset and IntangibleAsset
        # classes depreciate or amortize, respectively. However, this test ensures that rem_life updates accordingly
        # when life is changed. Further tests on this property are done in both test_TangibleAsset.py and
        # test_IntangibleAsset.py.
        self.assertEqual(asset_one.life, 60)
        self.assertEqual(asset_one.rem_life, 60)

if __name__ == "__main__":
    ut.main()
