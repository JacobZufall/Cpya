# Versioning for this file is formatted by date.
# YYYY.MM.DD.v
# The last number is for if there are multiple versions in a single day.
# For example, a release on May 15th, 2023 would be "2023.05.15.1", assuming it's the first release of the day.

class TaxLimits:
    # These numbers are based on the numbers issued by the IRS yearly, and are expected to change. When these numbers
    # change, they will be updated as soon as possible. Currently planning on providing a way to manually override
    # these numbers easily, in case the update isn't quick enough for some people. Ideally, we should be able to
    # automatically pull these numbers from the web, but that's not even planned yet.
    class Single:
        lower: int = 170_050
        upper: int = 220_050
        phase_in_range: int = 50_000

    class MFJ:
        lower: int = 340_100
        upper: int = 440_100
        phase_in_range: int = 100_000


def calc_w2_limit(wages: float, ubia: float = 0) -> float:
    num_one: float = wages * 0.5  # Will always get returned if there's no argument for UBIA.
    num_two: float = (wages * 0.25) + (ubia * 0.025)

    return max(num_one, num_two)


def calc_excess(qbi_amt: float, w2_limit: float) -> float:
    return (0.2 * qbi_amt) - w2_limit


def calc_tn_qbi(qbi_amt: float) -> float:
    return qbi_amt * 0.2


def calc_phase_in_per(tax_inc: float, f_status: str) -> float:
    if f_status == "S":
        return (tax_inc - TaxLimits.Single.lower) / TaxLimits.Single.phase_in_range
    elif f_status == "MFJ":
        return (tax_inc - TaxLimits.MFJ.lower) / TaxLimits.MFJ.phase_in_range


def calc_cat_one(tax_inc: float, qbi_amt: float, net_cap_gain: float, b_type: str) -> float:
    tn_qbi: float = calc_tn_qbi(qbi_amt)
    if b_type.lower() == "qtb":
        return tn_qbi
    elif b_type.lower() == "sstb":
        limit: float = (tax_inc - net_cap_gain) * 0.2
        if limit < tn_qbi:
            return limit
        else:
            return tn_qbi


def calc_cat_three(tax_inc: float, qbi_amt: float, w2_wages: float, f_status: str, b_type: str) -> float:
    if b_type.lower() == "qtb":
        tn_qbi: float = calc_tn_qbi(qbi_amt)
        w2_limit: float = calc_w2_limit(w2_wages)
        overall_limit: float = calc_tn_qbi(tax_inc)

        phase_in_per: float = calc_phase_in_per(tax_inc, f_status)
        excess: float = calc_excess(qbi_amt, w2_limit)

        red_amt: float = excess * phase_in_per
        red_qbi: float = tn_qbi - red_amt

        return min(red_qbi, w2_limit, overall_limit)

    elif b_type.lower() == "sstb":
        phase_in_per: float = calc_phase_in_per(tax_inc, f_status)
        applied_per: float = 1 - phase_in_per

        tn_qbi: float = calc_tn_qbi(qbi_amt * applied_per)
        w2_limit: float = calc_w2_limit(w2_wages * applied_per)
        overall_limit: float = calc_tn_qbi(tax_inc)

        excess: float = calc_excess(tn_qbi, w2_limit)
        red_amt: float = excess * phase_in_per
        red_qbi: float = tn_qbi - red_amt

        return min(red_qbi, w2_limit, overall_limit)


def calc_cat_two(tax_inc: float, qbi_amt: float, w2_wages: float, ubia: float, b_type: str) -> float:
    if b_type.lower() == "qtb":
        tn_qbi: float = calc_tn_qbi(qbi_amt)
        w2_limit: float = calc_w2_limit(w2_wages, ubia)
        overall_limit: float = calc_tn_qbi(tax_inc)

        return min(tn_qbi, w2_limit, overall_limit)

    elif b_type.lower() == "sstb":
        return 0  # There is no QBI deduction allowed for an SSTB for Category 2.


def qbi(filing_status: str,
        b_type: str,
        taxable_income: float,
        net_capital_gains: float,
        qbi_amt: float,
        w2_wages: float,
        ubia: float = 0) -> float:

    # For taxpayers with a filing status of Single or Head of Household.
    # Married Filing Single is included in here, since it's treated the same as filing single.
    if filing_status.lower() == "s" or filing_status.lower == "hoh" or filing_status.lower() == "mfs":
        if taxable_income <= TaxLimits.Single.lower:
            # Category 1
            return calc_cat_one(taxable_income, qbi_amt, net_capital_gains, b_type)
        elif TaxLimits.Single.lower < taxable_income < TaxLimits.Single.upper:
            # Category 3
            return calc_cat_three(taxable_income, qbi_amt, w2_wages, filing_status, b_type)
        elif taxable_income >= TaxLimits.Single.upper:
            # Category 2
            return calc_cat_two(taxable_income, qbi_amt, w2_wages, ubia, b_type)
        else:
            return 0  # Returns 0 if they enter an invalid filing status.

    # For taxpayers with a filing status of Married Filing Jointly.
    elif filing_status.lower() == "mfj":
        if taxable_income <= TaxLimits.MFJ.lower:
            return calc_cat_one(taxable_income, qbi_amt, net_capital_gains, b_type)
        elif TaxLimits.MFJ.lower < taxable_income < TaxLimits.MFJ.upper:
            return calc_cat_three(taxable_income, qbi_amt, w2_wages, filing_status, b_type)
        elif taxable_income >= TaxLimits.MFJ.upper:
            return calc_cat_two(taxable_income, qbi_amt, w2_wages, ubia, b_type)
        else:
            return 0
