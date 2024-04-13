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

    def print_fs(self) -> None:
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

        if self.pyacty_fs is not None:
            for category, accounts in self.pyacty_fs.fs.items():
                for account, attributes in accounts.items():
                    titles.append(account)

        # Find the longest string in the list.
        max_length: int = -1
        for i in titles:
            if len(i) > max_length:
                max_length = len(i)

        # How many blank spaces should be around the longest object (on each side)?
        margin: int = 2

        def print_divider(border: bool = False) -> None:
            """
            Prints a divider on the financial statement that covers the longest title and the margin.
            :param border: Is this divider the top or bottom border?
            :return: Nothing.
            """
            add_length: int = 0

            if border:
                add_length = 2

            print("-" * (max_length + margin + add_length))

        def print_header(header_name: str) -> None:
            space_needed: int = 0

            print(f"|{" " * space_needed}{header_name}{" " * space_needed}|")

        def print_account(account_name: str, show_decimals: bool = True) -> None:
            space_needed: int = 0
            account_bal: float | int = 0

            print(f"|{account_name}{" " * space_needed}{account_bal}|")

        # Top border of the financial statement.
        print_divider(True)
        print_header(self.company)
        print_header(self.fs_name)
        # print_header(self.fdate)

        # Bottom border of the financial statement.
        print_divider(True)
