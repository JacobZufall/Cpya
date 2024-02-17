"""
IncomeStatement.py
"""

from typing import TypeAlias
from FinancialStatement import FinancialStatement
from FinancialStatement import DefaultBal

fnstmt: TypeAlias = dict[str:dict[str:dict[str:any]]]


class IncomeStatement(FinancialStatement):
    def __init__(self):
        """
        Here is an example of what the income statement looks like.\n
        Type is dict[str:dict[str:dict[str:any]]], if needed.

        self.inc_stmt = {
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
            def_bal: DefaultBal = DefaultBal(category, contra)
        
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
        # Else statement called when for loop completes itteration without breaking.
        else:
            # Calling an exception here will be more exspected and easier for the programmer to catch.
            raise KeyError("Account not found!")

    def true_value(self, account: str) -> float:
        # This would be the other method to approaching this type of problem where you just pass
        # if a key error occurs.
        try:
            self.inc_stmt["revenue"][account]
            return self.calc_true_value(self.inc_stmt, "revenue", account)
        except KeyError:
            pass
        
        try:
            self.inc_stmt["expense"][account]
            return self.calc_true_value(self.inc_stmt, "expense", account)
        except KeyError:
            pass
        
        # Returning earlier in the function stops this from being called.
        raise KeyError("Account not found!")


if __name__ == "__main__":
    income_statement: IncomeStatement = IncomeStatement()
    income_statement.add_account("general revenue", "revenue", False)
    print(income_statement.inc_stmt)
    income_statement.del_account("general revenue")
    print(income_statement.inc_stmt)
