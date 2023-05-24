"""
Tax note: QBI deductions are only allowed for a QTB or SSTB. If it is neither of those, then a QBI deduction is not
allowed. This module only asks IF your business is a QTB OR an SSTB, not if it's one of the two. It is assumed that
you, as the user, know not to take a QBI deduction if your business is not a QTB or an SSTB.

DO NOT INCLUDE NET CAPITAL GAINS IN ORDINARY INCOME.
"""

# These variables let me easily assign duplicate values to tax_limits.
# My reasoning for this is it makes the code look cleaner inside of functions later on.
# Main point being, it reduces the amount of conditionals needed. :)
# Having two variables like this also makes it easier to change.
tl_s: dict[str:int] = {"lower": 170_050, "upper": 220_050, "phase_in": 50_000}
tl_m: dict[str:int] = {"lower": 340_100, "upper": 440_100, "phase_in": 100_000}

tax_limits: dict[str:any] = {"s": tl_s, "mfj": tl_m, "mfs": tl_s, "hoh": tl_s}

standard_deduction: dict[str:int] = {
    "s": 12_950,
    "mfj": 25_900,
    # Despite "mfs" == "s", there are individual to make other code easier to read.
    "mfs": 12_950,
    "hoh": 19_400
}


def calc_ten_qbi(ord_inc: float, sstb_per: float) -> float:
    return ord_inc * sstb_per * 0.2


def calc_tax_inc(agi: float, f_status: str) -> float:
    return agi - standard_deduction[f_status]


def calc_w2_limit(w2_wages: float, sstb_per: float, ubia: float) -> float:
    return max(w2_wages * sstb_per * 0.5, (w2_wages * sstb_per * 0.25) + (ubia * 0.025))


def calc_overall_limit(tax_inc: float, net_cap_gain: float = 0) -> float:
    return (tax_inc - net_cap_gain) * 0.2


# Returns a table with [0] == phase in % and [1] == SSTB applicable %.
def calc_phase_in(f_status: str, tax_inc: float, sstb: bool) -> list[float]:
    percentages: list[float] = [0, 0]

    percentages[0] = (tax_inc - tax_limits[f_status]["lower"]) / tax_limits[f_status]["phase_in"]

    # Using this conditional here means we don't have to use it in other functions.
    # percentages[1] is always multiplied with another value. Therefore, if it == 1, it has no effect.
    if sstb:
        percentages[1] = 1 - percentages[0]
    else:
        percentages[1] = 1

    return percentages


def qbi(filing_status: str, ord_inc: float, agi: float, w2_wages: float, ubia: float, net_cap_gain: float = 0.0, sstb: bool = False) -> float:

    tax_inc: float = calc_tax_inc(agi, filing_status)

    # Category 1
    if tax_inc <= tax_limits[filing_status]["lower"]:

        # SSTBs and QTBs are treated equally, which is why the second argument in calc_ten_qbi() is hard coded as 1.0.
        return min(calc_ten_qbi(ord_inc, 1.0), calc_overall_limit(calc_tax_inc(agi, filing_status), net_cap_gain))

    # Category 3
    elif tax_limits[filing_status]["lower"] < tax_inc < tax_limits[filing_status]["upper"]:

        print("Running calculation three.")  # Debug
        percentages: list[float] = calc_phase_in(filing_status, tax_inc, sstb)

        ten_qbi: float = calc_ten_qbi(ord_inc, percentages[1])
        w2_limit: float = calc_w2_limit(w2_wages, percentages[1], ubia)

        # If w2_limit > ten_qbi, then there is no reduction. The use of the min() function below makes it so that if
        # this is true, then red_amt == 0, which makes red_qbi == ten_qbi. This allows us to use one return statement.
        red_amt: float = (ten_qbi - min(ten_qbi, w2_limit)) * calc_phase_in(filing_status, tax_inc, sstb)[0]
        red_qbi = ten_qbi - red_amt
        overall_limit: float = calc_overall_limit(tax_inc, net_cap_gain)

        return min(red_qbi, overall_limit)

    # Category 2
    else:

        print("Running calculation two.")  # Debug
        percentages: list[float] = calc_phase_in(filing_status, tax_inc, sstb)

        ten_qbi: float = calc_ten_qbi(ord_inc, percentages[1])
        w2_limit: float = calc_w2_limit(w2_wages, percentages[1], ubia)
        overall_limit: float = calc_overall_limit(tax_inc, net_cap_gain)
        red_qbi: float = min(ten_qbi, w2_limit)

        # SSTBs do not qualify for a QBI deduction if they're category two.
        if sstb:
            percentages[1] = 0

        # If they're an SSTB, then it'll return 0 since percentages[1] == 0. However, if they're a QTB, it'll return the
        # result of the min function because percentages[1] == 1.
        return min(red_qbi, overall_limit) * percentages[1]


if __name__ == "__main__":
    print(qbi("s", 130_000, 148_000, 50_000, 30_000, 7_500))  # Cat 1
    print(qbi("s", 195_000, 207_000, 75_000, 45_000, 11_250))  # Cat 3
    print(qbi("s", 325_000, 345_000, 125_000, 75_000, 18_750))  # Cat 2
