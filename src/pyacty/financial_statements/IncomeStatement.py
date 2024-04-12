"""
IncomeStatement.py
"""

from typing import override

from .FinancialStatement import FinancialStatement
from .DefaultBalance import DefaultBalance
from src.pyacty.constants import IS_CATEGORIES
from src.pyacty.custom_types import fnstmt


class IncomeStatement(FinancialStatement):
    def __init__(self, **info) -> None:
        """
        Here is an example of what the income statement looks like.\n
        Type is dict[str:dict[str:dict[str:any]]], if needed.

        self.fs = {
            "revenue": {
                "Revenue": {
                    "d/c": "credit",\n
                    "bal": 0.0
                }
            },

            "expense": {
                "Interest Expense": {
                    "d/c": "debit",\n
                    "bal": 0.0
                }
            }
        }
        """
        super().__init__(**info)
        self.fs: fnstmt = {
            "revenue": {},
            "expense": {}
        }
        self.fs_name: str = "Income Statement"

    @override
    def reset(self) -> None:
        self.fs = {
            "revenue": {},
            "expense": {}
        }

    @override
    def add_account(self, name: str, category: str, start_bal: float = 0.0, contra: bool = False) -> None:
        if category.lower() not in IS_CATEGORIES:
            raise ValueError("Invalid category type.")

        db: DefaultBalance = DefaultBalance(category.lower(), contra)

        self.fs[category.lower()][name] = {
            "d/c": db.def_bal,
            "bal": start_bal
        }

    @override
    def del_account(self, name: str) -> None:
        for category in IS_CATEGORIES:
            try:
                self.fs[category].pop(name)
                break

            except KeyError:
                pass

        else:
            raise KeyError("Account not found!")

    def net_income(self) -> float:
        """
        Calculates net income based on the current state of te income statement.
        :return: Calculated net income.
        """
        totals: dict[str:float] = self.total_accounts()

        return totals["revenue"] - totals["expense"]
