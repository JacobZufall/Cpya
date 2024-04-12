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

    def __init__(self, company: str, financial_stmt: str, date: str,
                 pyacty_fs: None | FinancialStatement = None) -> None:
        """

        :param company:
        :param financial_stmt:
        :param date:
        :param pyacty_fs:
        """
        self.company: str = company
        self.financial_stmt: str = financial_stmt
        self.date: str = date
        self.pyacty_fs: None | FinancialStatement | BalanceSheet | IncomeStatement = pyacty_fs

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





