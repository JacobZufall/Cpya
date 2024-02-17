"""
test_TangibleAsset.py
"""
from src.taxpy.assets.TangibleAsset import TangibleAsset

# Define test scenarios here.
scenarios: dict[str:TangibleAsset] = {
    "scenario_01": TangibleAsset("Draw", (5 * 12), 1_000, 100, 1_000),
    "scenario_02": TangibleAsset("Apple", (7 * 12), 50_000, 2_000, 1_000),
    "scenario_03": TangibleAsset("Irbing", (10 * 12), 100_000, 0, 1_000),
    "scenario_04": TangibleAsset("Colith", (25 * 12), 5_000_000, 1_000_000, 5_000),
    "scenario_05": TangibleAsset("TheFireEnder", (1 * 12), 100_000, 0, 1_000)
}


def reset_scenarios(scenario_table: dict[str:any]) -> None:
    """
    Resets all scenarios in a given table.
    :return: Nothing.
    """
    for _, asset in scenario_table.items():
        asset.reset()


def depreciate_scenarios(method: int, scenario_table: dict[str:any], cond_table: dict[str:any]) -> None:
    for _, asset in scenario_table.items():
        asset.depreciate(method, cond_table["test_periods"], cond_table["db_decline"], cond_table["units_prod"])


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

    # Straight-line depreciation test
    depreciate_scenarios(0, scenarios, conditions)
    for _, asset in scenarios.items():
        assert asset.depreciable_value[-1] == asset.value - asset.SLVG_VALUE
        assert asset.last_depr[-1] == ((asset.DEF_VALUE - asset.SLVG_VALUE) / asset.LIFE) * conditions[
            "test_periods"]

    reset_scenarios(scenarios)

    # Declining balance depreciation test
    depreciate_scenarios(1, scenarios, conditions)
    for _, asset in scenarios.items():
        assert asset.depreciable_value[-1] == asset.value - asset.SLVG_VALUE
        # asset.total_depr[-2] retrieves the total depreciation prior to asset.depreciate() being called on the first
        # line of this loop.
        assert (asset.last_depr[-1] == (((asset.DEF_VALUE - asset.total_depr[-2]) / asset.LIFE) *
                                        conditions["db_decline"]) * conditions["test_periods"])

    reset_scenarios(scenarios)

    # Sum of the years' digits depreciation test
    depreciate_scenarios(2, scenarios, conditions)
    for _, asset in scenarios.items():
        assert asset.depreciable_value[-1] == asset.value - asset.SLVG_VALUE
        assert asset.last_depr[-1] == asset.DEF_VALUE * (asset.rem_life + conditions["test_periods"]) / asset.syd

    reset_scenarios(scenarios)

    # Units of production depreciation test
    depreciate_scenarios(3, scenarios, conditions)
    for _, asset in scenarios.items():
        assert asset.depreciable_value[-1] == asset.value - asset.SLVG_VALUE
        assert asset.last_depr[-1] == (asset.depreciable_value[-2] / asset.prod_cap) * conditions["units_prod"]

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

    assert scenarios["scenario_01"].last_depr[-1] == 180
    assert scenarios["scenario_02"].last_depr[-1] == 6_857.142857142857
    assert scenarios["scenario_03"].last_depr[-1] == 10_000
    assert scenarios["scenario_04"].last_depr[-1] == 160_000
    assert scenarios["scenario_05"].last_depr[-1] == 100_000

    reset_scenarios(scenarios)

    # Declining balance depreciation test
    # 150% test
    conditions["db_decline"] = 1.5
    depreciate_scenarios(1, scenarios, conditions)

    assert scenarios["scenario_01"].last_depr[-1] == 0
    assert scenarios["scenario_02"].last_depr[-1] == 0
    assert scenarios["scenario_03"].last_depr[-1] == 0
    assert scenarios["scenario_04"].last_depr[-1] == 0
    assert scenarios["scenario_05"].last_depr[-1] == 0

    reset_scenarios(scenarios)

    # 200% test
    conditions["db_decline"] = 2.0
    depreciate_scenarios(1, scenarios, conditions)

    assert scenarios["scenario_01"].last_depr[-1] == 0
    assert scenarios["scenario_02"].last_depr[-1] == 0
    assert scenarios["scenario_03"].last_depr[-1] == 0
    assert scenarios["scenario_04"].last_depr[-1] == 0
    assert scenarios["scenario_05"].last_depr[-1] == 0

    reset_scenarios(scenarios)

    # Sum of the years' digits depreciation test
    depreciate_scenarios(2, scenarios, conditions)

    assert scenarios["scenario_01"].last_depr[-1] == 0
    assert scenarios["scenario_02"].last_depr[-1] == 0
    assert scenarios["scenario_03"].last_depr[-1] == 0
    assert scenarios["scenario_04"].last_depr[-1] == 0
    assert scenarios["scenario_05"].last_depr[-1] == 0

    reset_scenarios(scenarios)

    # Units of production depreciation test
    depreciate_scenarios(3, scenarios, conditions)

    assert scenarios["scenario_01"].last_depr[-1] == 0
    assert scenarios["scenario_02"].last_depr[-1] == 0
    assert scenarios["scenario_03"].last_depr[-1] == 0
    assert scenarios["scenario_04"].last_depr[-1] == 0
    assert scenarios["scenario_05"].last_depr[-1] == 0

    reset_scenarios(scenarios)


if __name__ == "__main__":
    calc_assertions()
    result_assertions()
