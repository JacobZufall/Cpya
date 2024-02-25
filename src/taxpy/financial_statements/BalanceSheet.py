"""
BalanceSheet.py
"""

from FinancialStatement import FinancialStatement
from src.taxpy.constants import BS_CATEGORIES
from typing import TypeAlias

fnstmt: TypeAlias = dict[str:dict[str:dict[str:any]]]


class BalanceSheet(FinancialStatement):
    def __init__(self) -> None:
        """
        Here is an example of what the balance sheet looks like.\n

        self.bs = {
            "asset": {
                "cash": {
                    "d/c": "debit",\n
                    "bal": 0.0
                }
            },

            "liability": {
                "accounts payable": {
                    "d/c": "credit",\n
                    "bal": 0.0
                }
            },

            "equity": {
                "common stock": {
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

    def add_account(self, name: str, category: str, start_bal: float = 0.0, contra: bool = False) -> None:
        if category not in BS_CATEGORIES:
            raise ValueError("Invalid category type.")

        if category == "asset":
            def_bal = "debit" if not contra else "credit"
        else:
            def_bal = "credit" if not contra else "debit"

        self.fs[category][name] = {
            "d/c": def_bal,
            "bal": start_bal
        }

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

        for category, account in self.fs.items():
            for component, value in account.items():
                if component == "bal":
                    totals[category] += value

        return totals["asset"] == (totals["liability"] + totals["equity"])
