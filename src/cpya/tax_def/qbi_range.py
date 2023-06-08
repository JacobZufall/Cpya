# qbi_range.py
# 2023.06.07
# Supports tax years 2018 - present.
# The QBI deduction cannot be claimed in tax years ending on or before 12/31/2025.
# There is no plan to remove this class after the 2025 tax year.

import datetime
current_year: int = int(datetime.date.today().year)

years: dict[int:dict[str:list[int]]] = {
    # year: {
    #     "status": [lower, upper]
    # },

    2018: {
        "s": [157_500, 207_500],
        "m": [315_000, 415_000]
    },

    2019: {
        "s": [160_700, 210_700],
        "m": [321_400, 421_400]
    },

    2020: {
        "s": [163_300, 213_300],
        "m": [326_600, 426_600]
    },

    2021: {
        "s": [164_900, 214_900],
        "m": [329_800, 429_800]
    },

    2022: {
        "s": [170_050, 220_050],
        "m": [340_100, 440_100]
    },

    2023: {
        "s": [182_100, 232_100],
        "m": [364_200, 464_200]
    },
}


class QbiRange:
    def __init__(self, year: int = current_year):
        if (current_year < year or 2025 < year) or year < 2018:
            self.year: int = current_year
            print(f"The year {year} is not supported and the attribute has defaulted to the current year of "
                  f"{current_year}\n. This may be because you are using a year in which the QBI deduction did not "
                  f"exist, or the package has not been updated with that year's numbers.\nYou can manually change the "
                  f"numbers by calling the override_qbi() method.")
        else:
            self.year: int = year

        # Currently, the phase is consistently 50,000 and 100,000 every year. However, the calculation was still
        # coded in incase the IRS decides to shake things up.

        self.s_lower = years[year]["s"][0]
        self.s_upper = years[year]["s"][1]
        self.s_phase_in = self.s_upper - self.s_lower

        self.m_lower = years[year]["m"][0]
        self.m_upper = years[year]["m"][1]
        self.m_phase_in = self.m_upper = self.m_lower

    def override_qbi(self, status: str, lower: int, upper: int):
        if status == "s":
            self.s_lower = lower
            self.s_upper = upper
        elif status == "m":
            self.m_lower = lower
            self.m_upper = upper
        else:
            print(f"Valid statuses include \"s\" and \"m\". You entered {status}.\nNo values have been updated.")

    # Resets the QBI to the default for the current year.
    def reset_qbi(self):
        if (current_year < self.year or 2025 < self.year) or self.year < 2018:
            self.year: int = current_year
            # For some reason, self.year always equals current year. Need to figure out why and fix.
            print(f"The year {self.year} is not supported and the attribute has defaulted to the current year of "
                  f"{current_year}.\nThis may be because you are using a year in which the QBI deduction did not "
                  f"exist, or the package has not been updated with that year's numbers.\nYou can manually change the "
                  f"numbers by calling the override_qbi() method.\n")

        self.s_lower = years[self.year]["s"][0]
        self.s_upper = years[self.year]["s"][1]
        self.m_lower = years[self.year]["m"][0]
        self.m_upper = years[self.year]["m"][1]
