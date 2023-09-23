"""
balance_sheet.py
"""

from financial_statement import FinancialStatement
from typing import TypeAlias

fnstmt: TypeAlias = dict[str:dict[str:dict[str:any]]]


class BalanceSheet(FinancialStatement):
    def __init__(self) -> None:
        """
        Here is an example of what the balance sheet looks like.\n
        Type is dict[str:dict[str:dict[str:any]]], if needed.

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
        self.bal_sht = {
            "asset": {},
            "liability": {},
            "equity": {}
        }
        super().__init__()

    def add_account(self, name: str, category: str, contra: bool = False, start_bal: float = 0.0) -> fnstmt:

        if category not in ["asset", "liability", "equity"]:
            raise ValueError("Invalid category type.")

        if category == "asset":
            # Only reason I'm doing it with "not" is because it reads easier to an accountant.
            def_bal = "debit" if not contra else "credit"
        else:
            def_bal = "credit" if not contra else "debit"

        self.bal_sht[category][name] = {
            # Scope issue? I'm so bad about these.
            "d/c": def_bal,
            "bal": start_bal
        }

        return self.bal_sht[category][name]

    def del_account(self, name: str) -> None:
        for k in ["asset", "liability", "equity"]:
            try:
                self.bal_sht[k].pop(name)
                break
            except KeyError:
                pass
        else:
            raise KeyError("Account not found!")

    def true_value(self, account: str) -> float:
        for k in ["asset", "liability", "equity"]:
            try:
                self.bal_sht[k][account]
                return self.calc_true_value(self.bal_sht, k, account)
            except KeyError:
                continue
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

        # Variable names could be improved :(
        for i, v in self.bal_sht.items():
            for j, w in v.items():
                if j == "bal":
                    totals[i] += w

        # More readable
        return totals["asset"] == (totals["liability"] + totals["equity"])
