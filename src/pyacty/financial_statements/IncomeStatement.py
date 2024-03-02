"""
IncomeStatement.py
"""

from typing import TypeAlias
from FinancialStatement import FinancialStatement
from src.pyacty.financial_statements.DefaultBalance import DefaultBalance

fnstmt: TypeAlias = dict[str:dict[str:dict[str:any]]]


class IncomeStatement(FinancialStatement):
    def __init__(self) -> None:
        """
        Here is an example of what the income statement looks like.\n
        Type is dict[str:dict[str:dict[str:any]]], if needed.

        self.fs = {
            "revenue": {
                "general revenue": {
                    "d/c": "credit",\n
                    "bal": 0.0
                }
            },

            "expense": {
                "interest expense": {
                    "d/c": "debit",\n
                    "bal": 0.0
                }
            }
        }
        """
        super().__init__()
        self.inc_stmt = {
            "revenue": {},
            "expense": {}
        }
    
    def add_account(self, name: str, category: str, contra: bool) -> None:

        if not category == "revenue" or not category == "expense":
            raise ValueError
        else:
            def_bal: DefaultBalance = DefaultBalance(category, contra)
        
        self.inc_stmt[category][name] = {
            "d/c": def_bal,
            "bal": 0.0
        }

    def del_account(self, name: str) -> None:
        # Looping try except statements creates a lot of code that is very hard to read and tell
        # what the program is doing, I find it much better to either pass on the exception or use
        # a for loop.
        for k in ["revenue", "expense"]:
            try:
                self.inc_stmt[k].pop(name)
                break
            except KeyError:
                pass
        else:
            raise KeyError("Account not found!")

    def true_value(self, account: str) -> float:
        # This would be the other method to approaching this type of problem where you just pass
        # if a key error occurs.
        try:
            self.inc_stmt["revenue"][account]
            return self.true_value(self.inc_stmt, "revenue", account)
        except KeyError:
            pass
        
        try:
            self.inc_stmt["expense"][account]
            return self.true_value(self.inc_stmt, "expense", account)
        except KeyError:
            pass
        
        # Returning earlier in the function stops this from being called.
        raise KeyError("Account not found!")
