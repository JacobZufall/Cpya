"""
BalanceSheet.py

This class is primarily intended to serve as an example of how FinancialStatement can be inherited.
"""

from typing import override

from .FinancialStatement import FinancialStatement
from ..fundamentals.Money import Money
from ..constants import BS_CATEGORIES
from ..fundamentals.Account import Account


class BalanceSheet(FinancialStatement):
    def __init__(self, company_name: str, date: str) -> None:
        super().__init__("Balance Sheet", company_name, date)
        self.fn_stmt: dict[str:list[Account]] = {
            "asset": [],
            "liability": [],
            "equity": []
        }
        self.default_fs: dict[str:list[Account]] = self.fn_stmt

    # TODO: Consider adding automatic determination of the normal_balance argument?
    @override
    def add_account(self, category: str = "", name: str = "", normal_balance: str = "debit",
                    starting_balance: float | Money = Money(), contra: bool = False, term: str | None = None,
                    new_account: Account | None = None) -> None:
        """
        Overrides FinancialStatement.add_account(), see parent method for details.

        This method extends add_account() by validating the argument passed in the category parameter to see if it's
        a valid balance sheet category.

        :raises ValueError: Raises when the specified category is not listed as a valid balance sheet category in
        /pyacty/constants.py/. See file for details.
        """
        if category != "" and category not in BS_CATEGORIES:
            raise ValueError

        super().add_account(category, name, normal_balance, starting_balance,
                            contra, term, new_account)

    # I didn't change anything about this method when I adapted the Account class. But I think most of the heavy lifting
    # was done by the total_accounts() method in the parent class anyway, so it shouldn't matter.
    def check_bs(self) -> (bool, str):
        """
        Checks if the balance sheet balances.

        :return: Returns if the balance sheet balances (as a boolean) and the reason why it doesn't balance, if
        applicable.
        """
        totals: dict[str:float] = self.total_accounts()

        balances: bool = totals["asset"] == (totals["liability"] + totals["equity"])
        reason: str = "Balance sheet is balanced, no reason applicable."

        # If the balance sheet doesn't balance, this provides the reason why it doesn't balance.
        if not balances:
            if totals["asset"] > (totals["liability"] + totals["equity"]):
                reason = f"Assets exceeds liabilities and equity by {totals["asset"] - (totals["liability"] +
                                                                                        totals["equity"])}"
            else:
                reason = f"Liabilities and equity exceeds assets by {(totals["liability"] + totals["equity"]) -
                                                                     totals["asset"]}"

        return balances, reason
