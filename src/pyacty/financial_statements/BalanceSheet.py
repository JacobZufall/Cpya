"""
BalanceSheet.py
"""

from typing import override

from .FinancialStatement import FinancialStatement
from .DefaultBalance import DefaultBalance
from src.pyacty.constants import BS_CATEGORIES
from src.pyacty.custom_types import fnstmt


class BalanceSheet(FinancialStatement):
    def __init__(self) -> None:
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
        """
        super().__init__()
        self.fs: fnstmt = {
            "asset": {},
            "liability": {},
            "equity": {}
        }

    @override
    def reset(self) -> None:
        self.fs = {
            "asset": {},
            "liability": {},
            "equity": {}
        }

    # Contra should always be the last parameter because it's the least likely to be used, especially in balance sheet
    # accounts.
    @override
    def add_account(self, name: str, category: str, start_bal: float = 0.0, term: str = "current",
                    contra: bool = False) -> None:

        if category.lower() not in BS_CATEGORIES:
            raise ValueError("Invalid category type.")

        if term.lower() not in ["current", "non-current"]:
            raise ValueError("Invalid term.")

        db: DefaultBalance = DefaultBalance(category.lower(), contra)

        # Equity doesn't have separate sections for current and non-current, so we ignore it.
        if category.lower() == "equity":
            self.fs[category.lower()][name] = {
                "d/c": db.def_bal,
                "bal": start_bal
            }

        else:
            self.fs[category.lower()][name] = {
                "d/c": db.def_bal,
                "bal": start_bal,
                "term": term.lower()
            }

    @override
    def del_account(self, name: str) -> None:
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
        totals: dict[str:float] = {
            "asset": 0.0,
            "liability": 0.0,
            "equity": 0.0
        }

        for bs_category, bs_accounts in self.fs.items():
            for account, attributes in bs_accounts.items():
                for attribute, value in attributes.items():
                    if attribute == "bal":
                        totals[bs_category] += value

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
