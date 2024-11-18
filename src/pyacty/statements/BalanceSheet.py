"""
BalanceSheet.py
"""

from typing import override

from src.pyacty.statements.Balance import Balance
from .FinancialStatement import FinancialStatement
from .skeletons.FsSkeleton import FsSkeleton
from ..constants import BS_CATEGORIES


class BalanceSheet(FinancialStatement):
    def __init__(self, company_name: str, date: str) -> None:
        """
        Here is an example of what the balance sheet looks like.\n
        self.fs = {
            "asset": {
                "Cash": {
                    "d/c": "debit",\n
                    "bal": 0.0,\n
                    "term": "current"
                }
            },

            "liability": {
                "Accounts Payable": {
                    "d/c": "credit",\n
                    "bal": 0.0,\n
                    "term": "current"
                }
            },

            "equity": {
                "Common Stock": {
                    "d/c": "credit",\n
                    "bal": 0.0
                }
            }
        }
        :param company_name: The name of the company.
        :param date: The date of the financial statement.
        """
        super().__init__(company_name, date)
        self.fs: dict[str:dict[str:dict[str:str | int | float]]] = {
            "asset": {},
            "liability": {},
            "equity": {}
        }
        self.fs_name: str = "Balance Sheet"

    @override
    def __str__(self) -> str:
        return FsSkeleton(self.fs, self.company, self.fs_name, self.date,
                          decimals=self.decimals).auto_render()

    @override
    def reset(self) -> None:
        self.fs = {
            "asset": {},
            "liability": {},
            "equity": {}
        }

    # Contra should always be the last parameter because it's the least likely to be used, especially in balance sheet
    # accounts, since it's often netted with its non-contra counterpart.
    @override
    def add_account(self, name: str, category: str, start_bal: float = 0.0, term: str = "current",
                    contra: bool = False) -> None:

        if category.lower() not in BS_CATEGORIES:
            raise ValueError("Invalid category type.")

        if term.lower() not in ["current", "non-current"]:
            raise ValueError("Invalid term.")

        db: str = Balance.find_default_balance(category, contra)

        # Equity doesn't have separate sections for current and non-current, so we ignore it.
        if category.lower() == "equity":
            self.fs[category.lower()][name] = {
                "d/c": db,
                "bal": start_bal
            }

        else:
            self.fs[category.lower()][name] = {
                "d/c": db,
                "bal": start_bal,
                "term": term.lower()
            }

    @override
    def remove_account(self, name: str) -> None:
        for category in BS_CATEGORIES:
            try:
                self.fs[category].pop(name)
                break

            except KeyError:
                pass

        else:
            raise KeyError("Account not found!")

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
