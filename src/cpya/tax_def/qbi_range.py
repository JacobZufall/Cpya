# qbi_range.py
# 2023.06.07
# Supports tax years 2018 - present.
# The QBI deduction cannot be claimed in tax years ending on or before 12/31/2025.

import datetime
current_year: int = int(datetime.date.today().year)

years: dict[int:list[int]] = {
    # year: [lower, upper]
    2018: [],
    2019: [],
    2020: [],
    2021: [],
    2022: [],
    2023: []
}


class QbiRange:
    def __init__(self, lower_s: int, upper_s: int, lower_m: int, upper_m: int):
        self.lower_s = lower_s
        self.upper_s = upper_s
        self.phase_in_s = upper_s - lower_s
        self.lower_m = lower_m
        self.lower_s = lower_s
        self.phase_in_m = upper_m - lower_m
