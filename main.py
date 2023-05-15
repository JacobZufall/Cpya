# Versioning for this file is formatted by date.
# YYYY.MM.DD.v
# The last number is for if there are multiple versions in a single day.
# For example, a release on May 15th, 2023 would be "2023.05.15.1", assuming it's the first release of the day.

taxpayer_category: list[str] = ["category 1", "category 3", "category 2"]


class TaxLimits:
    class Single:
        lower: int = 170_050
        upper: int = 220_050
        phase_in_range: int = 50_000

    class MFJ:
        lower: int = 340_100
        upper: int = 440_100
        phase_in_range: int = 100_000


def calc_reduction_ratio(tax_inc: float, f_status: str) -> float:
    if f_status == "S":

        return (tax_inc - TaxLimits.Single.lower) / TaxLimits.Single.phase_in_range

    elif f_status == "MFJ":

        return (tax_inc - TaxLimits.MFJ.upper) / TaxLimits.MFJ.phase_in_range


def calc_w2_limit(wages: float, ubia: float = 0) -> float:
    num_one: float = wages * 0.5  # Will always get returned if there's no argument for UBIA.
    num_two: float = (wages * 0.25) + (ubia * 0.025)

    return max(num_one, num_two)


def calc_excess(qbi: float, w2_limit: float) -> float:
    return (0.2 * qbi) - w2_limit


def calc_tn_qbi(qbi: float) -> float:
    return qbi * 0.2


def calc_phase_in_per(tax_inc: float, f_status: str) -> float:
    if f_status == "S":
        return (tax_inc - TaxLimits.Single.lower) / TaxLimits.Single.phase_in_range
    elif f_status == "MFJ":
        return (tax_inc - TaxLimits.MFJ.lower) / TaxLimits.MFJ.phase_in_range


def find_category(f_status: str, t_inc: float) -> str | bool:

    # For taxpayers with a filing status of Single or Head of Household.
    if f_status == "S" or f_status == "HOH":
        if t_inc <= TaxLimits.Single.lower:
            # Category 1
            return taxpayer_category[0]
        elif TaxLimits.Single.lower < t_inc < TaxLimits.Single.upper:
            # Category 3
            return taxpayer_category[1]
        elif t_inc >= TaxLimits.Single.upper:
            # Category 2
            return taxpayer_category[2]
        else:
            return False

    # For taxpayers with a filing status of Married Filing Jointly.
    elif f_status == "MFJ":
        if t_inc <= TaxLimits.MFJ.lower:
            # Category 1
            return taxpayer_category[0]
        elif TaxLimits.MFJ.lower < t_inc < TaxLimits.MFJ.upper:
            # Category 3
            return taxpayer_category[1]
        elif t_inc >= TaxLimits.MFJ.upper:
            # Category 2
            return taxpayer_category[2]
        else:
            return False

    else:
        pass


def calc_cat_one(tax_inc: float, qbi: float, net_cap_gain: float, b_type: str) -> float:
    tn_qbi: float = calc_tn_qbi(qbi)
    if b_type.lower() == "qtb":
        return tn_qbi
    elif b_type.lower() == "sstb":
        limit: float = (tax_inc - net_cap_gain) * 0.2
        if limit < tn_qbi:
            return limit
        else:
            return tn_qbi


def calc_cat_three(tax_inc: float, qbi: float, w2_wages: float, f_status: str, b_type: str) -> float:
    if b_type.lower() == "qtb":
        tn_qbi: float = calc_tn_qbi(qbi)
        w2_limit: float = calc_w2_limit(w2_wages)
        overall_limit: float = calc_tn_qbi(tax_inc)

        phase_in_per: float = calc_phase_in_per(tax_inc, f_status)
        excess: float = calc_excess(qbi, w2_limit)

        red_amt: float = excess * phase_in_per
        red_qbi: float = tn_qbi - red_amt

        return min(red_qbi, w2_limit, overall_limit)

    elif b_type.lower() == "sstb":
        phase_in_per: float = calc_phase_in_per(tax_inc, f_status)
        applied_per: float = 1 - phase_in_per

        tn_qbi: float = calc_tn_qbi(qbi * applied_per)
        w2_limit: float = calc_w2_limit(w2_wages * applied_per)
        overall_limit: float = calc_tn_qbi(tax_inc)

        excess: float = calc_excess(tn_qbi, w2_limit)
        red_amt: float = excess * phase_in_per
        red_qbi: float = tn_qbi - red_amt

        return min(red_qbi, w2_limit, overall_limit)


def calc_cat_two(tax_inc: float, qbi: float, w2_wages: float, ubia: float, b_type: str) -> float:
    if b_type.lower() == "qtb":
        tn_qbi: float = calc_tn_qbi(qbi)
        w2_limit: float = calc_w2_limit(w2_wages, ubia)
        overall_limit: float = calc_tn_qbi(tax_inc)

        return min(tn_qbi, w2_limit, overall_limit)

    elif b_type.lower() == "sstb":
        return 0  # There is no QBI deduction allowed for an SSTB for Category 2.
