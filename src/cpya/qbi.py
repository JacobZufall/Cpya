"""
Versioning for this file is formatted by date.
YYYY.MM.DD.v
The last number is for if there are multiple versions in a single day.
For example, a release on May 15th, 2023 would be "2023.05.15.1", assuming it's the first release of the day.

These numbers are based on the numbers issued by the IRS yearly, and are expected to change. When these numbers
change, they will be updated as soon as possible. Currently planning on providing a way to manually override
these numbers easily, in case the update isn't quick enough for some people. Ideally, we should be able to
automatically pull these numbers from the web, but that's not even planned yet.
"""
import math

tax_limits: dict = {
    "single": {
        "lower": 170_050,
        "upper": 220_050,
        "phase_in": 50_000
    },

    "married": {
        "lower": 340_100,
        "upper": 440_100,
        "phase_in": 100_000
    }
}


def calc_w2_limit(wages: float, ubia: float = 0.0) -> float:
    # Will always get returned if there's no argument for UBIA.
    num_one: float = wages * 0.5
    num_two: float = (wages * 0.25) + (ubia * 0.025)

    return max(num_one, num_two)


def calc_excess(qbi_amt: float, w2_limit: float) -> float:
    return (0.2 * qbi_amt) - w2_limit


def calc_tn_qbi(qbi_amt: float) -> float:
    return qbi_amt * 0.2


def calc_phase_in_per(tax_inc: float, f_status: str) -> float | None:
    if f_status.upper() == "S" or f_status.upper() == "HOH" or f_status.upper() == "MFS":
        return (tax_inc - tax_limits["single"]["lower"]) / tax_limits["single"]["phase_in"]
    elif f_status.upper() == "MFJ":
        return (tax_inc - tax_limits["married"]["lower"]) / tax_limits["married"]["phase_in"]


def calc_cat_one(tax_inc: float, qbi_amt: float, net_cap_gain: float, b_type: str) -> float | None:
    tn_qbi: float = calc_tn_qbi(qbi_amt)
    if b_type.upper() == "QTB":
        return tn_qbi
    elif b_type.upper() == "SSTB":
        limit: float = (tax_inc - net_cap_gain) * 0.2
        if limit < tn_qbi:
            return limit
        else:
            return tn_qbi


def calc_cat_three(tax_inc: float, qbi_amt: float, w2_wages: float, f_status: str, b_type: str) -> float | None:
    if b_type.upper() == "QTB":
        tn_qbi: float = calc_tn_qbi(qbi_amt)
        w2_limit: float = calc_w2_limit(w2_wages)
        overall_limit: float = calc_tn_qbi(tax_inc)

        phase_in_per: float = calc_phase_in_per(tax_inc, f_status)
        excess: float = calc_excess(qbi_amt, w2_limit)

        red_amt: float = excess * phase_in_per
        red_qbi: float = tn_qbi - red_amt

        return min(red_qbi, w2_limit, overall_limit)

    elif b_type.upper() == "SSTB":
        phase_in_per: float = calc_phase_in_per(tax_inc, f_status)
        applied_per: float = 1.0 - phase_in_per

        tn_qbi: float = calc_tn_qbi(qbi_amt * applied_per)
        w2_limit: float = calc_w2_limit(w2_wages * applied_per)
        overall_limit: float = calc_tn_qbi(tax_inc)

        excess: float = calc_excess(tn_qbi, w2_limit)
        red_amt: float = excess * phase_in_per
        red_qbi: float = tn_qbi - red_amt

        return min(red_qbi, w2_limit, overall_limit)


def calc_cat_two(tax_inc: float, qbi_amt: float, w2_wages: float, ubia: float, b_type: str) -> float | None:
    if b_type.upper() == "QTB":
        tn_qbi: float = calc_tn_qbi(qbi_amt)
        w2_limit: float = calc_w2_limit(w2_wages, ubia)
        overall_limit: float = calc_tn_qbi(tax_inc)

        return min(tn_qbi, w2_limit, overall_limit)

    elif b_type.upper() == "SSTB":
        # There is no QBI deduction allowed for an SSTB for Category 2.
        return 0.0


# Filing status needs to be changed to a boolean applicable to if the filing status is MFJ.
# MFJ is the only filing status that is different, so it'd be a lot easier to use if it were a boolean.
def qbi(filing_status: str,
        b_type: str,
        taxable_income: float,
        net_capital_gains: float,
        w2_wages: float,
        qbi_amt: float = 0.0,
        ubia: float = 0.0) -> float:

    if math.floor(qbi_amt) == 0:
        qbi_amt = taxable_income

    # For taxpayers with a filing status of Single or Head of Household.
    # Married Filing Single is included in here, since it's treated the same as filing single.
    if filing_status.upper() == "S" or filing_status.upper() == "HOH" or filing_status.upper() == "MFS":
        if taxable_income <= tax_limits["single"]["lower"]:
            # Category 1
            return calc_cat_one(taxable_income, qbi_amt, net_capital_gains, b_type)
        elif tax_limits["single"]["lower"] < taxable_income < tax_limits["single"]["upper"]:
            # Category 3
            return calc_cat_three(taxable_income, qbi_amt, w2_wages, filing_status, b_type)
        elif taxable_income >= tax_limits["single"]["upper"]:
            # Category 2
            return calc_cat_two(taxable_income, qbi_amt, w2_wages, ubia, b_type)
        else:
            return 0.0  # Returns 0 if they enter an invalid filing status.

    # For taxpayers with a filing status of Married Filing Jointly.
    elif filing_status.upper() == "MFJ":
        if taxable_income <= tax_limits["married"]["lower"]:
            return calc_cat_one(taxable_income, qbi_amt, net_capital_gains, b_type)
        elif tax_limits["married"]["lower"] < taxable_income < tax_limits["married"]["upper"]:
            return calc_cat_three(taxable_income, qbi_amt, w2_wages, filing_status, b_type)
        elif taxable_income >= tax_limits["married"]["upper"]:
            return calc_cat_two(taxable_income, qbi_amt, w2_wages, ubia, b_type)
        else:
            return 0.0

    else:
        return 0.0


if __name__ == "__main__":
    print(qbi("S", "SSTB", 135_050, 7_500, 135_050, 50_000, 30_000))
    print(qbi("S", "SSTB", 194_050, 11_250, 194_050, 70_000, 45_000))
    print(qbi("S", "SSTB", 135_050, 7_500, 135_050, 50_000, 30_000))
