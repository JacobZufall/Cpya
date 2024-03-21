"""
test_TangibleAsset.py
"""

from src.pyacty.assets.TangibleAsset import TangibleAsset

# Define test scenarios here.
scenarios: dict[str:TangibleAsset] = {
    "scenario_01": TangibleAsset("Draw", (5 * 12), 1_000, 100, 2_500),
    "scenario_02": TangibleAsset("Apple", (7 * 12), 50_000, 2_000, 3_000),
    "scenario_03": TangibleAsset("Irbing", (10 * 12), 100_000, 0, 9_000),
    "scenario_04": TangibleAsset("Colith", (25 * 12), 5_000_000, 1_000_000, 5_000),
    "scenario_05": TangibleAsset("TheFireEnder", (1 * 12), 100_000, 0, 4_750)
}


def reset_scenarios(scenario_dict: dict[str:any]) -> None:
    """
    Resets all scenarios in a given array.
    :param scenario_dict: The dictionary containing the scenario(s).
    :return: Nothing.
    """
    for _, asset in scenario_dict.items():
        asset.reset()


def depreciate_scenarios(method: int, scenario_dict: dict[str:any], cond_dict: dict[str:any]) -> None:
    """
    Depreciates all scenarios in an array by a given method.\n
    [Supported Depreciation Methods] \n
    0: Straight Line Method \n
    1: Declining Balance Method \n
    2: Sum of the Years' Digits Method \n
    3: Units of Production Method \n
    :param method: The depreciation method.
    :param scenario_dict: The dictionary containing the scenario(s).
    :param cond_dict: The dictionary containing parameters for # of periods, declining %, and units produced.
    :return: Nothing
    """
    for _, asset in scenario_dict.items():
        asset.depreciate(method, cond_dict["test_periods"], cond_dict["db_decline"], cond_dict["units_prod"])
        # Rounded to two decimal places, or pennies.
        asset.last_depr[-1] = round(asset.last_depr.get_value(), 2)


def calc_assertions() -> None:
    """
    These assertions just re-do what was already done and aren't static. However, these are good for making sure you
    don't accidentally change how depreciation is calculated.
    :return: Nothing.
    """
    conditions: dict[str:any] = {
        "test_periods": 12,
        "db_decline": 1.5,
        "units_prod": 500
    }

    # In the event that an asset is 100% depreciated, the regular expression will return false and raise an assertion
    # error. In this case, it'll check if it equals asset.depreciable_value[-2]. If an asset is fully depreciated,
    # asset.depreciable_value[-1] will be 0, so asset.depreciable_value[-2] will be how much was last depreciated,
    # since it was the max amount that could be depreciated.

    # Straight-line depreciation test
    depreciate_scenarios(0, scenarios, conditions)
    for _, asset in scenarios.items():
        assert asset.depreciable_value[-1] == asset.value - asset.slvg_value
        assert asset.last_depr[-1] == ((asset.def_value - asset.slvg_value) / asset.life) * conditions[
            "test_periods"] or asset.depreciable_value[-2]

    reset_scenarios(scenarios)

    # Declining balance depreciation test
    depreciate_scenarios(1, scenarios, conditions)
    for _, asset in scenarios.items():
        assert asset.depreciable_value[-1] == asset.value - asset.slvg_value
        # asset.total_depr[-2] retrieves the total depreciation prior to asset.depreciate() being called on the first
        # line of this loop.
        # Also, I have no idea why PyCharm wants to format it this way, but I'll leave it for now.
        assert (asset.last_depr[-1] == (((asset.def_value - (asset.total_depr[-2] or 0)) / asset.life) *
                                        conditions["db_decline"]) * conditions["test_periods"] or
                asset.depreciable_value[-2])

    reset_scenarios(scenarios)

    # Sum of the years' digits depreciation test
    depreciate_scenarios(2, scenarios, conditions)
    for _, asset in scenarios.items():
        assert asset.depreciable_value[-1] == asset.value - asset.slvg_value
        assert (asset.last_depr[-1] == asset.def_value * (asset.rem_life + conditions["test_periods"]) / asset.syd or
                asset.depreciable_value[-2])

    reset_scenarios(scenarios)

    # Units of production depreciation test
    depreciate_scenarios(3, scenarios, conditions)
    for _, asset in scenarios.items():
        assert asset.depreciable_value[-1] == asset.value - asset.slvg_value
        assert (asset.last_depr[-1] == (asset.depreciable_value[-2] / asset.prod_cap) * conditions["units_prod"] or
                asset.depreciable_value[-2])

    reset_scenarios(scenarios)


def result_assertions() -> None:
    """
    These assertions make sure we're getting the expected value, or the same value we get calculating it by hand or with
    another program that's reliable. I think the only thing that needs to be asserted is self.last_depr[-1]
    :return: Nothing.
    """
    conditions: dict[str:any] = {
        "test_periods": 12,
        "db_decline": 1.0,
        "units_prod": 500
    }

    # Straight-line depreciation test
    depreciate_scenarios(0, scenarios, conditions)

    assert scenarios["scenario_01"].last_depr[-1] == 180.0
    assert scenarios["scenario_02"].last_depr[-1] == 6_857.14
    assert scenarios["scenario_03"].last_depr[-1] == 10_000.0
    assert scenarios["scenario_04"].last_depr[-1] == 160_000.0
    assert scenarios["scenario_05"].last_depr[-1] == 100_000.0

    reset_scenarios(scenarios)

    # Declining balance depreciation test
    # 150% test
    conditions["db_decline"] = 1.5
    depreciate_scenarios(1, scenarios, conditions)

    assert scenarios["scenario_01"].last_depr[-1] == 300.0
    assert scenarios["scenario_02"].last_depr[-1] == 10_714.29
    assert scenarios["scenario_03"].last_depr[-1] == 15_000.0
    assert scenarios["scenario_04"].last_depr[-1] == 300_000.0
    # scenario_05 is unique because it should depreciate $150,000, but the asset is only worth $100,000.
    assert scenarios["scenario_05"].last_depr[-1] == 100_000.0

    reset_scenarios(scenarios)

    # 200% test
    conditions["db_decline"] = 2.0
    depreciate_scenarios(1, scenarios, conditions)

    assert scenarios["scenario_01"].last_depr[-1] == 400.0
    assert scenarios["scenario_02"].last_depr[-1] == 14_285.71
    assert scenarios["scenario_03"].last_depr[-1] == 20_000.0
    assert scenarios["scenario_04"].last_depr[-1] == 400_000.0
    assert scenarios["scenario_05"].last_depr[-1] == 100_000.0

    reset_scenarios(scenarios)

    # Sum of the years' digits depreciation test
    depreciate_scenarios(2, scenarios, conditions)

    assert scenarios["scenario_01"].last_depr[-1] == 300.0
    assert scenarios["scenario_02"].last_depr[-1] == 12_000.0
    assert scenarios["scenario_03"].last_depr[-1] == 18_181.82
    assert scenarios["scenario_04"].last_depr[-1] == 307_692.31
    assert scenarios["scenario_05"].last_depr[-1] == 100_000.0

    reset_scenarios(scenarios)

    # Units of production depreciation test
    depreciate_scenarios(3, scenarios, conditions)

    assert scenarios["scenario_01"].last_depr[-1] == 180.0
    assert scenarios["scenario_02"].last_depr[-1] == 8_000.0
    assert scenarios["scenario_03"].last_depr[-1] == 5_555.56
    assert scenarios["scenario_04"].last_depr[-1] == 400_000.0
    assert scenarios["scenario_05"].last_depr[-1] == 10_526.32

    reset_scenarios(scenarios)


if __name__ == "__main__":
    calc_assertions()
    result_assertions()
