"""
FsTable.py
"""

from typing import override
from src.pyacty.financial_statements.FinancialStatement import FinancialStatement
from src.pyacty.financial_statements.BalanceSheet import BalanceSheet
from src.pyacty.financial_statements.IncomeStatement import IncomeStatement


class FsTable:
    months: dict[int:str] = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    def __init__(self, company: str, fs_name: str, date: str,
                 pyacty_fs: None | FinancialStatement = None) -> None:
        """

        :param company:
        :param fs_name:
        :param date:
        :param pyacty_fs:
        """
        self.company: str = company
        self.fs_name: str = fs_name
        self.date: str = date
        self.pyacty_fs: None | FinancialStatement | BalanceSheet | IncomeStatement = pyacty_fs

        # self.formatted_date

    @override
    def __str__(self):
        # I'm going to make this function do something (besides call itself) later when this class is more developed.
        super().__str__()

    @override
    def __repr__(self):
        return f"{self.__class__.__name__}: {self.__dict__}"

    def print(self) -> None:
        """
        Prints the financial statement.
        :return: Nothing.
        """

        # In order to properly format the width, we need to know the longest string out of every title, so we know how
        # wide to make it.
        titles: list[str] = []

        if self.company is not None:
            titles.append(self.company)

        if self.fs_name is not None:
            titles.append(self.fs_name)

        # self.date won't work since it's most likely formatted as "12/31/2024", and it needs to be formatted as
        # "For Year Ended December 31, 2024". So a self.formatted_date or something is needed to append to the list.
