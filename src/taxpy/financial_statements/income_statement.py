"""
income_statement.py
"""

from financial_statement import FinancialStatement


class IncomeStatement(FinancialStatement):
    def __init__(self):
        """
        Here is and example of what the balance sheet looks like.\n
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
        # Constructor method should always be the first method in a class if it has one.
        self.inc_stmt = {
            "revenue": {},
            "expense": {}
        }

        super().__init__()
    
    def add_account(self, name: str, category: str, contra: bool) -> None:
        # Simplified this function quite a bit, no need for double nested functions.  There is a
        # time and a place for them but something like this does not require it.
        def_bal: str = None
        
        # When it comes to short if elif blocks it can be better to make it more readable rather then
        # technically faster but more complicated.  (If you are really focused on optimaizing the code
        # then using an enum here would be much faster then having category as a string.)
        if category == "expense" and contra:
            def_bal = "credit"
        elif category == "expense":
            def_bal = "debit"
        elif category == "revenue" and contra:
            def_bal = "debit"
        elif category == "revenue":
            def_bal = "credit"
        
        # Raising a value error would be the more exspected way of handling a situation such as this, the
        # problem with just running a print statement is that it cannot be caught by the programmer easily
        # with a try except statement.  If you really do not want to raise an exception then returning a 
        # boolean value for true or false would also work rather well.
        else:
            raise ValueError("Invalid category type.")
        
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
