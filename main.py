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


def calc_w2_limit(wages: float) -> float:
    return wages * 0.5


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


def calc_cat_one(qbi: float) -> float:
    return calc_tn_qbi(qbi)


def calc_cat_three(tax_inc: float, qbi: float, w2_wages: float, f_status: str) -> float:
    tn_qbi = calc_tn_qbi(qbi)
    overall_limit = calc_tn_qbi(tax_inc)

    phase_in_per: float = calc_phase_in_per(tax_inc, f_status)
    excess: float = calc_excess(qbi, calc_w2_limit(w2_wages))
    red_amt: float = excess * phase_in_per

    red_qbi: float = tn_qbi - red_amt

    if red_qbi > overall_limit:
        return overall_limit
    elif red_qbi <= overall_limit:
        return red_qbi


def calc_cat_two(qbi: float, w2_limit: float) -> float:
    return min(calc_tn_qbi(qbi), w2_limit)


if __name__ == "__main__":
    pass
