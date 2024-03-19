"""
BalanceSheet.py
"""

from typing import override

from src.pyacty.financial_statements.FinancialStatement import FinancialStatement
from src.pyacty.financial_statements.DefaultBalance import DefaultBalance
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
                    "bal": 0.0
                }
            },

            "liability": {
                "Accounts Payable": {
                    "d/c": "credit",\n
                    "bal": 0.0
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
    def add_account(self, name: str, category: str, start_bal: float = 0.0, contra: bool = False) -> None:
        if category not in BS_CATEGORIES:
            raise ValueError("Invalid category type.")

        db: DefaultBalance = DefaultBalance(category, contra)

        self.fs[category][name] = {
            "d/c": db.def_bal,
            "bal": start_bal
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

    def check_bs(self) -> bool:
        """
        Checks if the balance sheet balances.
        :return: Returns True if assets = liabilities + equity.
        """
        totals: dict[str:float] = {
            "asset": 0.0,
            "liability": 0.0,
            "equity": 0.0
        }

        for bs_category, bs_account in self.fs.items():
            for attribute, value in bs_account.items():
                if attribute == "bal":
                    totals[bs_category] += value

        return totals["asset"] == (totals["liability"] + totals["equity"])
