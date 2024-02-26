"""
Qbi.py
"""

from src.pyacty.deductions.QbiRange import QbiRange
from src.pyacty.deductions.StandardDeduction import StandardDeduction


class Qbi(QbiRange, StandardDeduction):
    def __init__(self, tax_year: int, filing_status: str, ord_inc: float, agi: float, w2_wages: float,
                 ubia: float = 0.0, net_cap_gain: float = 0.0, sstb: bool = False) -> None:
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
        super().__init__(year=tax_year)

        # Checks to make sure that the tax year is eligible for a QBI and supported by StandardDeduction.py.
        if tax_year in QbiRange.qbi_years and tax_year in StandardDeduction.std_ded_years:
            self.tax_year: int = tax_year

        else:
            # If it's not valid, we default to the current year, or the last year available if the QBI deduction
            # isn't available for the current year.
            if self.current_year in QbiRange.qbi_years:
                self.tax_year = self.current_year

            else:
                # I'm not sure if dictionaries work this way, but it should set it to the last index, which will be
                # the last year available.
                self.tax_year = QbiRange.qbi_years[-1]

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
        # It looks weird to use __getattribute__ on self. I have two reasons for doing so in the next two lines. The
        # line below uses the filing_status to get the proper attribute inherited from StandardDeduction.py. It's a
        # string, and I'm not sure if there's a better way to get it than this.
        self.tax_inc = self.agi - self.__getattribute__(self.filing_status)

        # The line below uses qbi_status and combines it with the proper suffix to obtain the correct attribute from
        # QbiRange.py.
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
        # You should feel bad about this line of code, I am impressed, but you should still feel bad.
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
