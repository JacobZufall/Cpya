from src.taxpy.assets.TangibleAsset import TangibleAsset


def reset_scenarios(scenario_table: dict[str:any]) -> None:
    """
    Resets all test cases in a given table.
    :return: Nothing.
    """
    for j, w in scenario_table.items():
        w.reset()


# Define test cases here.
scenarios: dict[str:TangibleAsset] = {
    "scenario_01": TangibleAsset("Draw", (5 * 12), 1_000, 100, 1_000),
    "scenario_02": TangibleAsset("Apple", (7 * 12), 50_000, 2_000, 1_000),
    "scenario_03": TangibleAsset("Irbing", (10 * 12), 100_000, 0, 1_000)
}

# CALCULATION ASSERTIONS #
# These assertions just re-do what was already done and aren't static. However, these are good for making sure you
# don't accidentally change how depreciation is calculated.

calc_conditions: dict[str:any] = {
    "test_periods": 12,
    "db_decline": 1.5,
    "units_prod": 5_000
}

# Straight-line depreciation test.
for i, v in scenarios.items():
    v.depreciate(0, calc_conditions["test_periods"])

    assert v.depr_value == v.value - v.slvg_value
    assert v.last_depr == ((v.def_value - v.slvg_value) / v.life) * calc_conditions["test_periods"]

reset_scenarios(scenarios)

# Declining balance depreciation test.
for i, v in scenarios.items():
    py_total_depr: float = v.total_depr
    v.depreciate(1, periods=calc_conditions["test_periods"], decline=calc_conditions["db_decline"])

    assert (v.last_depr == (((v.def_value - py_total_depr) / v.life) * calc_conditions["db_decline"]) *
            calc_conditions["test_periods"])
    # Need another assertion right here.

reset_scenarios(scenarios)

# Sum of the years' digits depreciation test.
for i, v in scenarios.items():
    v.depreciate(2, calc_conditions["test_periods"])

    # Write assertions here.

reset_scenarios(scenarios)

# Units of production depreciation test.
for i, v in scenarios.items():
    v.depreciate(3, calc_conditions["test_periods"], units_prod=calc_conditions["units_prod"])

    # Write assertions here.

reset_scenarios(scenarios)

# RESULT ASSERTIONS #
# These assertions make sure we're getting the expected value, or the same value we get calculating it by hand or with
# another program that's reliable. I think the only thing that needs to be asserted is self.amt_depr.

result_conditions: dict[str:any] = {
    "test_periods": 12,
    "db_decline": 1.5,
    "units_prod": 5_000
}

for i, v in scenarios.items():
    v.depreciate(0, result_conditions["test_periods"])

assert scenarios["scenario_01"].last_depr == 180
