from src.taxpy.assets.tangible_asset import TangibleAsset


def assert_depr_value(asset: TangibleAsset) -> None:
    """
    Asserts that self.depr_value is calculated correctly.
    :param asset: The asset to test.
    :return:Nothing.
    """
    assert asset.depr_value == asset.value - asset.slvg_value


def assert_sl_amt_depr(asset: TangibleAsset, periods: int) -> None:
    """
    Asserts that straight-line depreciation is calculated correctly.
    :param asset: The asset to test.
    :param periods: The amount of periods the asset was depreciated most recently.
    :return: Nothing.
    """
    assert asset.amt_depr == (asset.default_value / asset.life) * periods


# Define assets here.
asset_one: TangibleAsset = TangibleAsset("Computer", (5 * 12), 1_000, 100)
asset_two: TangibleAsset = TangibleAsset("Furniture", (7 * 12), 50_000, 2_000)
asset_three: TangibleAsset = TangibleAsset("Truck", (10 * 12), 100_000, 0)

# Straight-line depreciation.
sl_test_periods: int = 12

asset_one.depreciate(0, sl_test_periods)
asset_two.depreciate(0, sl_test_periods)
asset_three.depreciate(0, sl_test_periods)

assert_depr_value(asset_one)
assert_sl_amt_depr(asset_one, sl_test_periods)

assert_depr_value(asset_two)
assert_sl_amt_depr(asset_two, sl_test_periods)

assert_depr_value(asset_three)
assert_sl_amt_depr(asset_three, sl_test_periods)
