"""
qbi.py

Tax note: QBI deductions are only allowed for a QTB or SSTB. If it is neither of those, then a QBI deduction is not
allowed. This module only asks IF your business is a QTB OR an SSTB, not if it's one of the two. It is assumed that
you, as the user, know not to take a QBI deduction if your business is not a QTB or an SSTB.

DO NOT INCLUDE NET CAPITAL GAINS IN ORDINARY INCOME.
"""

from src.taxpy.deductions.qbi_range import QbiRange
from src.taxpy.deductions.standard_deduction import StandardDeduction


# Would it be better to combine QbiRange into Qbi, or is it better that Qbi inherits QbiRange. I don't think any other
# class would need to inherit from QbiRange, so it doesn't make much sense for it to be its own class in its own file.
class Qbi(QbiRange, StandardDeduction):
    def __init__(self, tax_year: int, filing_status: str, ord_inc: float, agi: float, w2_wages: float,
                 ubia: float = 0.0, net_cap_gain: float = 0.0, sstb: bool = False):
        """
        :param tax_year: The relevant tax year.
        :param filing_status: The filing status of the taxpayer.
        :param ord_inc: The ordinary income of the taxpayer.
        :param agi: The adjusted gross income of the taxpayer.
        :param w2_wages: The W-2 wages of the taxpayer.
        :param ubia: The unadjusted basis immediately after acquisition.
        :param net_cap_gain: The net capital gain.
        :param sstb: Is the business a specified service or trade business?
        """
        # I'm assuming that accounts know what all of these variable names mean but I for sure do not.
        QbiRange.__init__(self, tax_year)
        StandardDeduction.__init__(self, tax_year)

        # Checks to make sure that the tax year is eligible for a QBI and supported by standard_deduction.py.
        if tax_year in QbiRange.qbi_years and tax_year in StandardDeduction.std_ded_years:
            self.tax_year: int = tax_year
        else:
            # If it's not valid, we default to the current year.
            self.tax_year: int = self.current_year
            print(f"The year {tax_year} is not a valid year for a QBI deduction or is no longer supported for a "
                  f"standard deduction. The year {self.tax_year} has been selected. If needed, call \"override_qbi\" "
                  f"and \"override_std_ded\" to manually input your own numbers. These methods will automatically "
                  f"calculate the rest from the numbers given.")

        self.filing_status: str = filing_status
        self.ord_inc: float = ord_inc
        self.agi: float = agi
        self.w2_wages: float = w2_wages
        self.ubia: float = ubia
        self.net_cap_gain: float = net_cap_gain
        self.sstb: bool = sstb

        # For QBI deductions, the only one that's different is MFJ. Single, MFS, and HoH are all treated the same.
        if filing_status == "mfj":
            self.qbi_status: str = "m"
        else:
            self.qbi_status: str = "s"

        self.red_qbi = None
        self.ten_qbi = None
        self.overall_limit = None
        self.sstb_per = None
        self.phase_in = None
        self.tax_inc = None

        self.qbi = self.calculate_qbi()
    
    def calculate_qbi(self) -> float:
        """
        :return: The QBI deduction.
        """
        self.tax_inc = self.agi - self.__getattribute__(self.filing_status)
        
        # Why are you calling self.__getattribute__ on your own instance.  In the case where this is
        # required you are likely doing something wrong.

        # I don't remember :(
        self.phase_in = (self.tax_inc - self.__getattribute__(f"{self.qbi_status}_lower") /
                         self.__getattribute__(f"{self.qbi_status}_phase_in"))

        # If it's a QTB (not an SSTB), then there is no SSTB%. In this case, self.sstb_per = 1, or 100%, so it has no
        # effect when it is used.
        if self.sstb:
            self.sstb_per = 1 - self.phase_in
        else:
            self.sstb_per = 1

        self.overall_limit = (self.tax_inc - self.net_cap_gain) * 0.2

        self.ten_qbi = self.ord_inc * self.sstb_per * 0.2
        
        # You should feel bad about this line of code, I am impressed but you should still feel bad.
        self.red_qbi = self.ten_qbi - ((self.ten_qbi - min(self.ten_qbi,
                                                           max(self.w2_wages * self.sstb_per * 0.5,
                                                               (self.w2_wages * self.sstb_per * 0.25) +
                                                               (self.ubia * 0.025)))) * self.phase_in)

        # Category 1
        if self.tax_inc <= self.__getattribute__(f"{self.qbi_status}_lower"):
            return min(self.ten_qbi, self.overall_limit)
        # Category 3
        elif self.__getattribute__(
                f"{self.qbi_status}_lower") < self.tax_inc < self.__getattribute__(
                f"{self.qbi_status}_upper"):
            return min(self.red_qbi, self.overall_limit)
        # Category 2
        else:
            return min(self.red_qbi, self.overall_limit) * self.sstb_per
