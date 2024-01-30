from src.taxpy.assets.tangible_asset import TangibleAsset


def reset_scenarios(scenario_table: dict[str:any]) -> None:
    """
    Resets all test cases in a given table.
    :return: Nothing.
    """
    for j, w in scenario_table.items():
        w.reset()


# Define test cases here.
scenarios: dict[str:TangibleAsset] = {
    "scenario_01": TangibleAsset("Computer", (5 * 12), 1_000, 100),
    "scenario_02": TangibleAsset("Furniture", (7 * 12), 50_000, 2_000),
    "scenario_03": TangibleAsset("Truck", (10 * 12), 100_000, 0)
}

conditions: dict[str:any] = {
    "test_periods": 12,
    "db_decline": 1.5,
    "units_prod": 5_000
}


# Straight-line depreciation test.
for i, v in scenarios.items():
    v.depreciate(0, conditions["test_periods"])

    assert v.depr_value == v.value - v.slvg_value
    assert v.amt_depr == ((v.def_value - v.slvg_value) / v.life) * conditions["test_periods"]

reset_scenarios(scenarios)

# Declining balance depreciation test.
for i, v in scenarios.items():
    v.depreciate(1, conditions["test_periods"], decline=conditions["db_decline"])

    # Write assertions here.

reset_scenarios(scenarios)

# Sum of the years' digits depreciation test.
for i, v in scenarios.items():
    v.depreciate(2, conditions["test_periods"])

    # Write assertions here.

reset_scenarios(scenarios)

# Units of production depreciation test.
for i, v in scenarios.items():
    v.depreciate(3, conditions["test_periods"], units_prod=conditions["units_prod"])

    # Write assertions here.

reset_scenarios(scenarios)
