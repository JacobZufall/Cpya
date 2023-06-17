"""
balance_sheet.py
"""

import json
from financial_statement import FinancialStatement


class BalanceSheet(FinancialStatement):
    def add_account(self, name: str, category: str, contra: bool) -> dict[str:dict[str:dict[str:any]]] | None:
        def create_account(def_bal: str) -> dict[str:dict[str:dict[str:any]]]:
            """
            :param def_bal: The default balance of an account (debit/credit).
            :return: Nothing.
            """
            if def_bal == "debit" or def_bal == "credit":
                self.bal_sht[category][name] = {
                    "d/c": def_bal,
                    "bal": 0.0
                }

                return self.bal_sht[category][name]
            else:
                print(f"{def_bal} is not a valid balance type. Please choose either \"debit\" or \"credit\".")

        if category == "asset":
            if contra:
                return create_account("credit")
            else:
                return create_account("debit")
        elif category == "liability" or category == "equity":
            if contra:
                return create_account("debit")
            else:
                return create_account("credit")
        else:
            print("Category not found!")

    def del_account(self, name: str) -> None:
        try:
            self.bal_sht["asset"].pop(name)
        except KeyError:
            try:
                self.bal_sht["liability"].pop(name)
            except KeyError:
                try:
                    self.bal_sht["equity"].pop(name)
                except KeyError:
                    print("Account not found!")

    def true_value(self, account: str) -> float:
        try:
            self.bal_sht["asset"][account]
        except KeyError:
            try:
                self.bal_sht["liability"][account]
            except KeyError:
                try:
                    self.bal_sht["equity"][account]
                except KeyError:
                    print("Account not found!")
                else:
                    return self.calc_true_value(self.bal_sht, "equity", account)
            else:
                return self.calc_true_value(self.bal_sht, "liability", account)
        else:
            return self.calc_true_value(self.bal_sht, "asset", account)

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

        for i, v in self.bal_sht.items():
            for j, w in v.items():
                if j == "bal":
                    totals[i] += w

        if totals["asset"] == (totals["liability"] + totals["equity"]):
            return True
        else:
            return False

    # def save_fs(self, file_name: str, path: str = "data/bal_sht/") -> None:
    #     data = json.dumps(self.bal_sht, indent=4)
    #     with open(f"{path}{file_name}.json", "w") as outfile:
    #         outfile.write(data)
    #
    # def load_fs(self, file: str, validate: bool = True) -> None:
    #     data = open(f"{file}.json")
    #     self.bal_sht = json.load(data)
    #
    #     if validate:
    #         try:
    #             self.bal_sht["asset"]
    #         except KeyError:
    #             print(f"{file} is not a valid balance sheet!")
    #
    #         while True:
    #             answer: str = input("Would you like to load the file anyway? (y/n)")
    #
    #             if answer == "n":
    #                 self.bal_sht = {
    #                     "asset": {},
    #                     "liability": {},
    #                     "equity": {}
    #                 }
    #                 break
    #             elif answer == "y":
    #                 break
    #             else:
    #                 print(f"{answer} is not a valid answer.")

    def __init__(self):
        """
        Here is and example of what the balance sheet looks like.\n
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


if __name__ == "__main__":
    balance_sheet: BalanceSheet = BalanceSheet()
    balance_sheet.add_account("cash", "asset", True)
    print(balance_sheet.bal_sht)