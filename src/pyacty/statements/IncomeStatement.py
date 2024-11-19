"""
IncomeStatement.py
"""

from typing import override

from .FinancialStatement import FinancialStatement
from .skeletons.FsSkeleton import FsSkeleton
from .. import Money
from ..constants import IS_CATEGORIES
from ..fundamentals.Account import Account


class IncomeStatement(FinancialStatement):
    def __init__(self, company_name: str, date: str) -> None:
        """
        Here is an example of what the income statement looks like.\n
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
        :param company_name: The name of the company.
        :param date: The date of the financial statement.
        """
        super().__init__("Income Statement", company_name, date)
        self.fn_stmt: dict[str:list[Account]] = {
            "revenue": {},
            "expense": {}
        }
        self.default_fs: dict[str:list[Account]] = self.fn_stmt

    @override
    def __str__(self) -> str:
        return FsSkeleton(self.fn_stmt, self.company, self.fs_name, self.date).auto_render()

    @override
    def reset(self) -> None:
        self.fn_stmt = self.default_fs

    # TODO: Consider adding automatic determination of the normal_balance argument?
    @override
    def add_account(self, category: str = "", name: str = "", normal_balance: str = "debit",
                    starting_balance: float | Money = Money(), contra: bool = False, term: str | None = None,
                    new_account: Account | None = None) -> None:
        if category != "" and category not in IS_CATEGORIES:
            raise ValueError

        super().add_account(category, name, normal_balance, starting_balance,
                            contra, term, new_account)

    def net_income(self) -> float:
        """
        Calculates net income based on the current state of the income statement. This method may be too simple for some
        purposes.
        :return: Calculated net income.
        """
        totals: dict[str:float] = self.total_accounts()

        return totals["revenue"] - totals["expense"]
