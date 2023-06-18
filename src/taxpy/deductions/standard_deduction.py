"""
standard_deduction.py

Need to consider how many years to include.
Does the IRS have an API?
"""

import datetime


class StandardDeduction:
    current_year: int = int(datetime.date.today().year)

    std_ded_years: dict[int:list[int]] = {
        # year: [single, head of household]
        
        # Use a tuple probably. as well as allow the user to define values to this customlly
        2013: [6_100, 8_950],
        2014: [6_200, 9_100],
        2015: [6_300, 9_250],
        2016: [6_300, 9_300],
        2017: [6_350, 9_350],
        2018: [12_000, 18_000],
        2019: [12_200, 18_350],
        2020: [12_400, 18_650],
        2021: [12_550, 18_800],
        2022: [12_950, 19_400],
        2023: [13_850, 20_800]
    }
    
    def __init__(self, year: int = current_year):
        """
        :param year: The relevant tax year.
        """
        self.year = year

        self.s = None
        self.mfj = None
        self.mfs = None
        self.hoh = None

        self.define_std_ded()

    def define_std_ded(self) -> None:
        """
        :return: Nothing.
        """
        # You would likely be much better off using the datetime lib.
        if self.current_year < self.year or self.year < (self.current_year - 10):
            self.year: int = self.current_year
            print(f"The year {self.year} is not supported and the attribute has defaulted to the current year of "
                  f"{self.current_year}\n. Please call the override_deduction() method in order to use non-supported "
                  f"years.")
        else:
            self.year: int = self.year

        self.s: int = self.std_ded_years[self.year][0]
        self.mfj: int = self.std_ded_years[self.year][0] * 2
        self.mfs: int = self.std_ded_years[self.year][0]
        self.hoh: int = self.std_ded_years[self.year][1]

    def override_std_ded(self, s: float, hoh: float) -> None:
        """
        Used to change the standard deduction for filing statuses manually. Useful when trying to use a year that is
        no longer supported.

        :param s: The desired value for single filing status. Used to calculate other filing statuses.
        :param hoh: The desired value for head of household filing status.
        :return: Nothing.
        """
        self.s = s
        self.mfj = s * 2
        self.mfs = s
        self.hoh = hoh

