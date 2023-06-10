# qbi.py

# Tax note: QBI deductions are only allowed for a QTB or SSTB. If it is neither of those, then a QBI deduction is not
# allowed. This module only asks IF your business is a QTB OR an SSTB, not if it's one of the two. It is assumed that
# you, as the user, know not to take a QBI deduction if your business is not a QTB or an SSTB.

# DO NOT INCLUDE NET CAPITAL GAINS IN ORDINARY INCOME.

from src.cpya_jacobzufall.standard_deduction import StandardDeduction
from src.cpya_jacobzufall.qbi_range import QbiRange


class Qbi:
    qbi_range: QbiRange = QbiRange()
    std_ded: StandardDeduction = StandardDeduction()

    def calculate_qbi(self):
        self.std_ded.year = self.tax_year
        self.qbi_range.year = self.tax_year
        self.std_ded.define()
        self.qbi_range.define()

        self.tax_inc = self.agi - self.std_ded.__getattribute__(self.filing_status)
        self.phase_in = (self.tax_inc - self.qbi_range.__getattribute__(f"{self.filing_status}_lower") /
                         self.qbi_range.__getattribute__(f"{self.filing_status}_phase_in"))

        # If it's a QTB (not an SSTB), then there is no SSTB%. In this case, self.sstb_per = 1, or 100%, so it has no
        # effect when it is used.
        if self.sstb:
            self.sstb_per = 1 - self.phase_in
        else:
            self.sstb_per = 1

        self.overall_limit = (self.tax_inc - self.net_cap_gain) * 0.2
        self.w2_limit = max(self.w2_wages * self.sstb_per * 0.5,
                            (self.w2_wages * self.sstb_per * 0.25) + (self.ubia * 0.025))

        self.ten_qbi = self.ord_inc * self.sstb_per * 0.2
        self.red_qbi = self.ten_qbi - ((self.ten_qbi - min(self.ten_qbi, self.w2_limit)) * self.phase_in)

        # Category 1
        if self.tax_inc <= self.qbi_range.__getattribute__(f"{self.filing_status}_lower"):
            self.qbi = min(self.ten_qbi, self.overall_limit)
        # Category 3
        elif self.qbi_range.__getattribute__(
                f"{self.filing_status}_lower") < self.tax_inc < self.qbi_range.__getattribute__(
                f"{self.filing_status}_upper"):
            self.qbi = min(self.red_qbi, self.overall_limit)
        # Category 2
        else:
            min(self.red_qbi, self.overall_limit) * self.sstb_per

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

        self.qbi = None
        self.red_qbi = None
        self.ten_qbi = None
        self.w2_limit = None
        self.overall_limit = None
        self.sstb_per = None
        self.phase_in = None
        self.tax_inc = None

        self.calculate_qbi()


if __name__ == "__main__":
    myQbi: Qbi = Qbi(2022, "s", 400_000.0, 148_000.0, 50_000.0, 30_000.0, 7_500.0)
    print(myQbi.qbi)
