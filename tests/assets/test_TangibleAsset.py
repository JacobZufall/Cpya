"""
test_TangibleAsset.py

First time using unittest. I'm not 100% sure how to structure the file.
"""

import unittest as ut

from src.pyacty.assets.TangibleAsset import TangibleAsset


class TestTangibleAsset(ut.TestCase):
    def test_straight_line(self) -> None:
        asset_one: TangibleAsset = TangibleAsset("Test Asset", 10 * 12, 100_000)

        # Ensures that the properties were set and can be retrieved properly.
        self.assertEqual(asset_one.depreciable_allocation, 100_000)
        self.assertEqual(asset_one.depreciable_value, 100_000)
        self.assertEqual(asset_one.net_value, 100_000)
        self.assertEqual(asset_one.slvg_value, 0)
        self.assertEqual(asset_one.syd, 55)
        self.assertEqual(asset_one.total_depr, 0)
        self.assertEqual(asset_one.prod_cap, 0)

        # Ensures that depreciate depreciates the correct amount.
        self.assertEqual(asset_one.depreciate(0), 10_000)

        # Ensures that the properties were updated (or not updated) accordingly.
        self.assertEqual(asset_one.depreciable_allocation, 100_000)
        self.assertEqual(asset_one.depreciable_value, 90_000)
        self.assertEqual(asset_one.net_value, 90_000)
        self.assertEqual(asset_one.slvg_value, 0)
        self.assertEqual(asset_one.syd, 55)
        self.assertEqual(asset_one.total_depr, 10_000)
        self.assertEqual(asset_one.prod_cap, 0)

        # Testing depreciation for two periods just to ensure it doesn't change.
        self.assertEqual(asset_one.depreciate(0), 10_000)

        self.assertEqual(asset_one.depreciable_allocation, 100_000)
        self.assertEqual(asset_one.depreciable_value, 80_000)
        self.assertEqual(asset_one.net_value, 80_000)
        self.assertEqual(asset_one.slvg_value, 0)
        self.assertEqual(asset_one.syd, 55)
        self.assertEqual(asset_one.total_depr, 20_000)
        self.assertEqual(asset_one.prod_cap, 0)

        # Same tests, this time with a salvage value.
        asset_two: TangibleAsset = TangibleAsset("Test Asset", 10 * 12, 100_000, 10_000)

        self.assertEqual(asset_two.depreciable_allocation, 90_000)
        self.assertEqual(asset_two.depreciable_value, 90_000)
        self.assertEqual(asset_two.net_value, 100_000)
        self.assertEqual(asset_two.slvg_value, 10_000)
        self.assertEqual(asset_two.syd, 55)
        self.assertEqual(asset_two.total_depr, 0)
        self.assertEqual(asset_two.prod_cap, 0)

        self.assertEqual(asset_two.depreciate(0), 9_000)

        self.assertEqual(asset_two.depreciable_allocation, 90_000)
        self.assertEqual(asset_two.depreciable_value, 81_000)
        self.assertEqual(asset_two.net_value, 91_000)
        self.assertEqual(asset_two.slvg_value, 10_000)
        self.assertEqual(asset_two.syd, 55)
        self.assertEqual(asset_two.total_depr, 9_000)
        self.assertEqual(asset_two.prod_cap, 0)

        self.assertEqual(asset_two.depreciate(0), 9_000)

        self.assertEqual(asset_two.depreciable_allocation, 90_000)
        self.assertEqual(asset_two.depreciable_value, 72_000)
        self.assertEqual(asset_two.net_value, 82_000)
        self.assertEqual(asset_two.slvg_value, 10_000)
        self.assertEqual(asset_two.syd, 55)
        self.assertEqual(asset_two.total_depr, 18_000)
        self.assertEqual(asset_two.prod_cap, 0)

    def test_declining_balance(self) -> None:
        # Declining balance ignores salvage value, so testing asset_two ensures it ignores it in calculations.
        asset_two: TangibleAsset = TangibleAsset("Test Asset", 10 * 12, 100_000, 10_000)

        self.assertEqual(asset_two.depreciable_allocation, 90_000)
        self.assertEqual(asset_two.depreciable_value, 90_000)
        self.assertEqual(asset_two.net_value, 100_000)
        self.assertEqual(asset_two.slvg_value, 10_000)
        self.assertEqual(asset_two.syd, 55)
        self.assertEqual(asset_two.total_depr, 0)
        self.assertEqual(asset_two.prod_cap, 0)

        self.assertEqual(asset_two.depreciate(1, decline=2.0).value, 20_000)

        self.assertEqual(asset_two.depreciable_allocation, 90_000)
        self.assertEqual(asset_two.depreciable_value, 70_000)
        self.assertEqual(asset_two.net_value, 80_000)
        self.assertEqual(asset_two.slvg_value, 10_000)
        self.assertEqual(asset_two.syd, 55)
        self.assertEqual(asset_two.total_depr, 20_000)
        self.assertEqual(asset_two.prod_cap, 0)

        self.assertEqual(asset_two.depreciate(1, decline=2.0), 16_000)

        self.assertEqual(asset_two.depreciable_allocation, 90_000)
        self.assertEqual(asset_two.depreciable_value, 54_000)
        self.assertEqual(asset_two.net_value, 64_000)
        self.assertEqual(asset_two.slvg_value, 10_000)
        self.assertEqual(asset_two.syd, 55)
        self.assertEqual(asset_two.total_depr, 36_000)
        self.assertEqual(asset_two.prod_cap, 0)

    def test_sum_years(self) -> None:
        asset_one: TangibleAsset = TangibleAsset("Test Asset", 10 * 12, 100_000)

        self.assertEqual(asset_one.depreciable_allocation, 100_000)
        self.assertEqual(asset_one.depreciable_value, 100_000)
        self.assertEqual(asset_one.net_value, 100_000)
        self.assertEqual(asset_one.slvg_value, 0)
        self.assertEqual(asset_one.syd, 55)
        self.assertEqual(asset_one.total_depr, 0)
        self.assertEqual(asset_one.prod_cap, 0)

        self.assertEqual(asset_one.depreciate(2), 18_181.82)

        self.assertEqual(asset_one.depreciable_allocation, 100_000)
        self.assertEqual(asset_one.depreciable_value, 81_818.18)
        self.assertEqual(asset_one.net_value, 81_818.18)
        self.assertEqual(asset_one.slvg_value, 0)
        self.assertEqual(asset_one.syd, 55)
        self.assertEqual(asset_one.total_depr, 18_181.82)
        self.assertEqual(asset_one.prod_cap, 0)

        self.assertEqual(asset_one.depreciate(2), 16_363.64)

        self.assertEqual(asset_one.depreciable_allocation, 100_000)
        self.assertEqual(asset_one.depreciable_value.rounded_value, 65_454.55)
        self.assertEqual(asset_one.net_value, 65_454.55)
        self.assertEqual(asset_one.slvg_value, 0)
        self.assertEqual(asset_one.syd, 55)
        self.assertEqual(asset_one.total_depr, 34_545.45)
        self.assertEqual(asset_one.prod_cap, 0)

        asset_two: TangibleAsset = TangibleAsset("Test Asset", 10 * 12, 100_000, 10_000)

        self.assertEqual(asset_two.depreciable_allocation, 90_000)
        self.assertEqual(asset_two.depreciable_value, 90_000)
        self.assertEqual(asset_two.net_value, 100_000)
        self.assertEqual(asset_two.slvg_value, 10_000)
        self.assertEqual(asset_two.syd, 55)
        self.assertEqual(asset_two.total_depr, 0)
        self.assertEqual(asset_two.prod_cap, 0)

        self.assertEqual(asset_two.depreciate(2), 16_363.64)

        self.assertEqual(asset_two.depreciable_allocation, 90_000)
        self.assertEqual(asset_two.depreciable_value, 73_636.36)
        self.assertEqual(asset_two.net_value, 83_636.36)
        self.assertEqual(asset_two.slvg_value, 10_000)
        self.assertEqual(asset_two.syd, 55)
        self.assertEqual(asset_two.total_depr, 16_363.64)
        self.assertEqual(asset_two.prod_cap, 0)

        self.assertEqual(asset_two.depreciate(2), 14_727.27)

        self.assertEqual(asset_two.depreciable_allocation, 90_000)
        self.assertEqual(asset_two.depreciable_value, 58_909.09)
        self.assertEqual(asset_two.net_value, 68_909.09)
        self.assertEqual(asset_two.slvg_value, 10_000)
        self.assertEqual(asset_two.syd, 55)
        self.assertEqual(asset_two.total_depr, 31_090.91)
        self.assertEqual(asset_two.prod_cap, 0)

    def test_units_prod(self) -> None:
        # Just to test what happens if someone forgets to specify the amount of units produced or a production cap.
        asset_one: TangibleAsset = TangibleAsset("Test Asset", 10 * 12, 100_000)

        self.assertEqual(asset_one.depreciable_allocation, 100_000)
        self.assertEqual(asset_one.depreciable_value, 100_000)
        self.assertEqual(asset_one.net_value, 100_000)
        self.assertEqual(asset_one.slvg_value, 0)
        self.assertEqual(asset_one.syd, 55)
        self.assertEqual(asset_one.total_depr, 0)
        self.assertEqual(asset_one.prod_cap, 0)

        # It's expected that this results in a ZeroDivisionError, since the formula for the Units of Production method
        # involves dividing by the prod_cap of the asset. Therefore, if this doesn't result in an error, then we have a
        # problem.
        try:
            self.assertEqual(asset_one.depreciate(3), 0)

        except ZeroDivisionError:
            pass

        else:
            raise ArithmeticError("A production capacity of 0 should result in a ZeroDivisionError. Either "
                                  "prod_cap != 0 for this test case, or the formula is wrong!")

        asset_three: TangibleAsset = TangibleAsset("Test Asset", 10 * 12, 100_000, prod_cap=1_000)

        self.assertEqual(asset_three.depreciable_allocation, 100_000)
        self.assertEqual(asset_three.depreciable_value, 100_000)
        self.assertEqual(asset_three.net_value, 100_000)
        self.assertEqual(asset_three.slvg_value, 0)
        self.assertEqual(asset_one.syd, 55)
        self.assertEqual(asset_one.total_depr, 0)
        self.assertEqual(asset_three.prod_cap, 1_000)

        self.assertEqual(asset_three.depreciate(3, units_prod=100), 10_000)

        self.assertEqual(asset_three.depreciable_allocation, 100_000)
        self.assertEqual(asset_three.depreciable_value, 90_000)
        self.assertEqual(asset_three.net_value, 90_000)
        self.assertEqual(asset_three.slvg_value, 0)
        self.assertEqual(asset_three.syd, 55)
        self.assertEqual(asset_three.total_depr, 10_000)
        self.assertEqual(asset_three.prod_cap, 1_000)

        asset_four: TangibleAsset = TangibleAsset("Test Asset", 10 * 12, 100_000, 10_000, 1_000)

        self.assertEqual(asset_four.depreciable_allocation, 90_000)
        self.assertEqual(asset_four.depreciable_value, 90_000)
        self.assertEqual(asset_four.net_value, 100_000)
        self.assertEqual(asset_four.slvg_value, 10_000)
        self.assertEqual(asset_four.syd, 55)
        self.assertEqual(asset_four.total_depr, 0)
        self.assertEqual(asset_four.prod_cap, 1_000)

        self.assertEqual(asset_four.depreciate(3, units_prod=100), 9_000)

        self.assertEqual(asset_four.depreciable_allocation, 90_000)
        self.assertEqual(asset_four.depreciable_value.value, 81_000)
        self.assertEqual(asset_four.net_value, 91_000)
        self.assertEqual(asset_four.slvg_value, 10_000)
        self.assertEqual(asset_four.syd, 55)
        self.assertEqual(asset_four.total_depr, 9_000)
        self.assertEqual(asset_four.prod_cap, 1_000)

        # This asset is just to test behavior when an asset is depreciated all the way.
        asset_five: TangibleAsset = TangibleAsset("Test Asset", 10 * 12, 100_000, prod_cap=100)

        self.assertEqual(asset_five.depreciable_allocation, 100_000)
        self.assertEqual(asset_five.depreciable_value, 100_000)
        self.assertEqual(asset_five.net_value, 100_000)
        self.assertEqual(asset_five.slvg_value, 0)
        self.assertEqual(asset_five.syd, 55)
        self.assertEqual(asset_five.total_depr, 0)
        self.assertEqual(asset_five.prod_cap, 100)

        self.assertEqual(asset_five.depreciate(3, units_prod=100), 100_000)

        self.assertEqual(asset_five.depreciable_allocation, 100_000)
        self.assertEqual(asset_five.depreciable_value, 0)
        self.assertEqual(asset_five.net_value, 0)
        self.assertEqual(asset_five.slvg_value, 0)
        self.assertEqual(asset_five.syd, 55)
        self.assertEqual(asset_five.total_depr, 100_000)
        self.assertEqual(asset_five.prod_cap, 100)

        self.assertEqual(asset_five.depreciate(3, units_prod=100), 0)

        # These are all exactly the same as above, as they should be. Since you can't depreciate a fully depreciated
        # asset anymore, none of these should change.
        self.assertEqual(asset_five.depreciable_allocation, 100_000)
        self.assertEqual(asset_five.depreciable_value, 0)
        self.assertEqual(asset_five.net_value, 0)
        self.assertEqual(asset_five.slvg_value, 0)
        self.assertEqual(asset_five.syd, 55)
        self.assertEqual(asset_five.total_depr, 100_000)
        self.assertEqual(asset_five.prod_cap, 100)


if __name__ == "__main__":
    ut.main()
