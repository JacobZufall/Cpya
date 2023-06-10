# standard_deduction.py

# Supports the current year and the previous 10 years.
# Non-supported years can be used by calling the override_deduction() method.

import datetime


class StandardDeduction:
    current_year: int = int(datetime.date.today().year)

    years: dict[int:list[int]] = {
        # year: [single, head of household]
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
        if self.current_year < year or year < (self.current_year - 10):
            self.year: int = self.current_year
            print(f"The year {year} is not supported and the attribute has defaulted to the current year of "
                  f"{self.current_year}\n. Please call the override_deduction() method in order to use non-supported years.")
        else:
            self.year: int = year

        self.s: int = self.years[year][0]
        self.mfj: int = self.years[year][0] * 2
        self.mfs: int = self.years[year][0]
        self.hoh: int = self.years[year][1]

    # Overrides the default deduction set by the IRS.
    # Useful if you need to use the standard deduction from a year that is no longer supported.
    def override_deduction(self, s: int, hoh: int):
        self.s = s
        self.mfj = s * 2
        self.mfs = s
        self.hoh = hoh

    # Resets the deductions to default.
    def reset_deduction(self):
        if self.current_year < self.year or self.year < (self.current_year - 10):
            self.year: int = self.current_year
            # For some reason, self.year always equals current year. Need to figure out why and fix.
            print(f"The year {self.year} is not supported and the attribute has defaulted to the current year of "
                  f"{self.current_year}.\nPlease call the override_deduction() method in order to use "
                  f"non-supported years.\n")

        self.s = self.years[self.year][0]
        self.mfj = self.years[self.year][0] * 2
        self.mfs = self.years[self.year][0]
        self.hoh = self.years[self.year][1]
