"""
IncomeStatement.py
"""

from FinancialStatement import FinancialStatement
from src.pyacty.constants import IS_CATEGORIES
from typing import TypeAlias

fnstmt: TypeAlias = dict[str:dict[str:dict[str:any]]]


class IncomeStatement(FinancialStatement):
    def __init__(self) -> None:
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
        super().__init__()
        self.fs = {
            "revenue": {},
            "expense": {}
        }

    def add_account(self, name: str, category: str, start_bal: float = 0.0, contra: bool = False) -> None:
        if category not in IS_CATEGORIES:
            raise ValueError("Invalid category type.")

        def_bal: str

        if category == "revenue":
            def_bal = "credit" if not contra else "debit"
        else:
            def_bal = "debit" if not contra else "credit"

        self.fs[category][name] = {
            "d/c": def_bal,
            "bal": start_bal
        }

    def del_account(self, name: str) -> None:
        for is_category in IS_CATEGORIES:
            try:
                self.fs[is_category].pop(name)
                break
            except KeyError:
                pass
        else:
            raise KeyError("Account not found!")


if __name__ == "__main__":
    inc_stmt: IncomeStatement = IncomeStatement()

    inc_stmt.add_account("Revenue", "revenue", 1_000_000)
    inc_stmt.add_account("Interest Revenue", "revenue", 500_000)

    inc_stmt.add_account("Interest Expense", "expense", 5_000)
    inc_stmt.add_account("Depreciation Expense", "expense", 500)

    inc_stmt.save_fs("C:\\Users\\jacob\\OneDrive\\Desktop\\output", "test_is", "csv")
    inc_stmt.save_fs("C:\\Users\\jacob\\OneDrive\\Desktop\\output", "test_is", "json")
