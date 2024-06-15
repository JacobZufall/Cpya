"""
BsSkeleton.py
"""

from typing import override
from statementskeleton import Skeleton, Title


class BsSkeleton(Skeleton):
    def __init__(self, fnstmt: dict[str:dict[str:dict[str:any]]], company: str, fs_name: str, date: str,
                 min_width: int = 50, margin: int = 2, indent: int = 4, column_space: int = 20,
                 decimals: bool = True) -> None:
        """
        Creates a skeleton to add elements into in order to neatly display a balance sheet in the console.
        :param company: The name of the company.
        :param fs_name: The name of the financial statement.
        :param date: The date of the financial statement.
        :param fnstmt: The financial statement.
        :param min_width: The minimum width the financial statement will be in the output.
        :param margin: How many spaces are on each side of headers.
        :param column_space: The minimum space between the account name and its balance.
        :param indent: How many spaces are between an account name and the side.
        """
        # The reason I don't force the fs_name is because someone might want to make a non-GAAP balance sheet, in which
        # case it would be named something else to comply.
        super().__init__(fnstmt, company, fs_name, date, min_width, margin,
                         indent, column_space, decimals)

    @override
    def define_body(self) -> None:
        next_div_num: int = 4

        # A "c" prefix represents "current" while an "nc" prefix represents "non-current".
        c_assets_bal: float | int = 0.0
        nc_assets_bal: float | int = 0.0
        c_liabilities_bal: float | int = 0.0
        nc_liabilities_bal: float | int = 0.0

        for category, accounts in self.fnstmt.items():


        for category, accounts in self.fnstmt.items():
            self.implement(Title(self, (category.lower()).capitalize()),
                           f"title_{category.lower()}")

            total_bal: float | int = 0.0

            for account, attributes in accounts.items():
                if attributes["d/c"] == "debit":
                    total_bal += attributes["bal"]

                else:
                    total_bal -= attributes["bal"]

