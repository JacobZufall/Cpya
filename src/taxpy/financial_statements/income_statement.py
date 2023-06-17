"""
income_statement.py
"""

from financial_statement import FinancialStatement


class IncomeStatement(FinancialStatement):
    def add_account(self, name: str, category: str, contra: bool) -> None:
        def create_account(def_bal: str) -> None:
            """
            :param def_bal: The default balance of an account (debit/credit).
            :return: Nothing.
            """
            if def_bal == "debit" or def_bal == "credit":
                self.inc_stmt[category][name] = {
                    "d/c": def_bal,
                    "bal": 0.0
                }
            else:
                print(f"{def_bal} is not a valid balance type. Please choose either \"debit\" or \"credit\".")

        if category == "expense":
            if contra:
                create_account("credit")
            else:
                create_account("debit")
        elif category == "revenue":
            if contra:
                create_account("debit")
            else:
                create_account("credit")
        else:
            print("Category not found!")

    def del_account(self, name: str) -> None:
        try:
            self.inc_stmt["revenue"].pop(name)
        except KeyError:
            try:
                self.inc_stmt["expense"].pop(name)
            except KeyError:
                print("Account not found!")

    def true_value(self, account: str) -> float:
        try:
            self.inc_stmt["revenue"][account]
        except KeyError:
            try:
                self.inc_stmt["expense"][account]
            except KeyError:
                print("Account not found!")
            else:
                return self.calc_true_value(self.inc_stmt, "expense", account)
        else:
            return self.calc_true_value(self.inc_stmt, "revenue", account)

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
        self.inc_stmt = {
            "revenue": {},
            "expense": {}

        }

        super().__init__()


if __name__ == "__main__":
    income_statement: IncomeStatement = IncomeStatement()
    income_statement.add_account("general revenue", "revenue", False)
    print(income_statement.inc_stmt)
    income_statement.del_account("general revenue")
    print(income_statement.inc_stmt)
