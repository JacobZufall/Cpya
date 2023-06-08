# qbi.py
# 2023.06.08

# Tax note: QBI deductions are only allowed for a QTB or SSTB. If it is neither of those, then a QBI deduction is not
# allowed. This module only asks IF your business is a QTB OR an SSTB, not if it's one of the two. It is assumed that
# you, as the user, know not to take a QBI deduction if your business is not a QTB or an SSTB.

# DO NOT INCLUDE NET CAPITAL GAINS IN ORDINARY INCOME.

from tax_def.standard_deduction import StandardDeduction
from tax_def.qbi_range import QbiRange

qbi_range: QbiRange = QbiRange()
std_ded: StandardDeduction = StandardDeduction()


class Qbi:
    def __init__(self, tax_year: int, filing_status: str, ord_inc: float, agi: float, w2_wages: float, ubia: float,
                 net_cap_gain: float = 0.0, sstb: bool = False):
        self.tax_year = tax_year
        self.filing_status = filing_status
        self.ord_inc = ord_inc
        self.agi = agi
        self.w2_wages = w2_wages
        self.ubia = ubia
        self.net_cap_gain = net_cap_gain
        self.sstb = sstb

        std_ded.year = tax_year
        qbi_range.year = tax_year
        std_ded.reset_deduction()
        qbi_range.reset_qbi()

        self.tax_inc = self.agi - std_ded.__getattribute__(self.filing_status)
        self.phase_in = (self.tax_inc - qbi_range.__getattribute__(f"{self.filing_status}_lower") /
                         qbi_range.__getattribute__(f"{self.filing_status}_phase_in"))

        # If it's a QTB (not an SSTB), then there is no SSTB%. In this case, self.sstb_per = 1, or 100%, so it has no
        # effect when it is used.
        if sstb:
            self.sstb_per = 1 - self.phase_in
        else:
            self.sstb_per = 1

        self.overall_limit = (self.tax_inc - self.net_cap_gain) * 0.2
        self.w2_limit = max(self.w2_wages * self.sstb_per * 0.5,
                            (self.w2_wages * self.sstb_per * 0.25) + (self.ubia * 0.025))

        self.ten_qbi = self.ord_inc * self.sstb_per * 0.2
        self.red_qbi = self.ten_qbi - ((self.ten_qbi - min(self.ten_qbi, self.w2_limit)) * self.phase_in)

        # Category 1
        if self.tax_inc <= qbi_range.__getattribute__(f"{self.filing_status}_lower"):
            self.qbi = min(self.ten_qbi, self.overall_limit)
        # Category 3
        elif qbi_range.__getattribute__(f"{self.filing_status}_lower") < self.tax_inc < qbi_range.__getattribute__(
                f"{self.filing_status}_upper"):
            self.qbi = min(self.red_qbi, self.overall_limit)
        # Category 2
        else:
            min(self.red_qbi, self.overall_limit) * self.sstb_per


if __name__ == "__main__":
    myQbi: Qbi = Qbi(2022, "s", 400_000, 148_000, 50_000, 30_000, 7_500)
    print(myQbi.qbi)
