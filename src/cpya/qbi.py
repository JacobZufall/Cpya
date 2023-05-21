"""
Tax note: QBI deductions are only allowed for a QTB or SSTB. If it is neither of those, then a QBI deduction is not
allowed. This module only asks IF your business is a QTB OR an SSTB, not if it's one of the two. It is assumed that
you, as the user, know not to take a QBI deduction if your business is not a QTB or an SSTB.

DO NOT INCLUDE NET CAPITAL GAINS IN INCOME.
"""

# These variables let me easily assign duplicate values to tax_limits.
# My reasoning for this is it makes the code look cleaner inside of functions later on.
# Main point being, it reduces the amount of conditionals needed. :)
# Having two variables like this also makes it easier to change.
tl_s: dict[str:int] = {"lower": 170_050, "upper": 220_050, "phase_in": 50_000}
tl_m: dict[str:int] = {"lower": 340_100, "upper": 440_100, "phase_in": 100_000}

tax_limits: dict[str:dict[str:int]] = {"s": tl_s, "mfj": tl_m, "mfs": tl_s, "hoh": tl_s}

standard_deduction: dict[str:int] = {
    "s": 12_950,
    "mfj": 25_900,
    # Despite "mfs" == "s", there are individual to make other code easier to read.
    "mfs": 12_950,
    "hoh": 19_400
}


def calc_tax_inc(agi: float, f_status: str) -> float:
    return agi - standard_deduction[f_status]


def calc_ten_qbi(ord_inc: float, sstb_per: float) -> float:
    return ord_inc * sstb_per * 0.2


def calc_overall_limit(agi: float, net_cap_gain: float = 0) -> float:
    return (agi - net_cap_gain) * 0.2


def calc_199a_qbi(ten_qbi: float, overall_limit: float) -> float:
    return min(ten_qbi, overall_limit)


def calc_w2_limit(w2_wages: float, sstb_per: float, ubia: float) -> float:
    return max(w2_wages * sstb_per * 0.5, (w2_wages * sstb_per * 0.25) + (ubia * 0.025))


# Returns a table with [0] == phase in % and [1] == SSTB applicable %.
def calc_phase_in(f_status: str, tax_inc: float, sstb: bool) -> list[float]:
    percentages: list[float] = []

    percentages[0] = (tax_inc - standard_deduction[f_status]) / tax_limits[f_status]["phase_in"]

    # Using this conditional here means we don't have to use it in other functions.
    # percentages[1] is always multiplied with another value. Therefore, if it == 1, it has no effect.
    if sstb:
        percentages[1] = 1
    else:
        percentages[1] = 1 - percentages[0]

    return percentages


def calc_cat_one(ord_inc: float, agi: float, net_cap_gain: float) -> float:
    # SSTBs and QTBs are treated equally, which is why the second argument in calc_ten_qbi() is hard coded as 1.0.
    return calc_199a_qbi(calc_ten_qbi(ord_inc, 1.0), calc_overall_limit(agi, net_cap_gain))


def calc_cat_two(f_status: str, ord_inc: float, agi: float, w2_wages: float, ubia: float, net_cap_gain: float, sstb: bool = False):
    tax_inc: float = calc_tax_inc(agi, f_status)
    percentages: list[float] = calc_phase_in(f_status, tax_inc, sstb)

    ten_qbi: float = calc_ten_qbi(ord_inc, percentages[1])
    w2_limit = calc_w2_limit(w2_wages, percentages[1], ubia)

    return min()



if __name__ == "__main__":
    pass
