"""
balance_sheet.py
"""

import json
from financial_statement import FinancialStatement
from financial_statement import DefaultBal


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
    
    def add_account(self, name: str, category: str, contra: bool) -> dict[str:dict[str:dict[str:any]]]:
        if category not in ["asset", "liability", "equity"]:
            raise ValueError("Invalid category type.")
        
        def_bal: str = None
        if category == "asset":
            def_bal = "credit" if contra else "debit"
        # We can assume if not asset then it is either a liability or equity.
        else:
            def_bal = "debit" if contra else "credit"

        self.bal_sht[category][name] = {
            "d/c": def_bal,
            "bal": 0.0
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
        

    # def save_fs(self, file_name: str, path: str = "data/bal_sht/") -> None:
    #     data = json.dumps(self.bal_sht, indent=4)
    #     with open(f"{path}{file_name}.json", "w") as outfile:
    #         outfile.write(data)
    
    # def load_fs(self, file: str, validate: bool = True) -> None:
    #     data = open(f"{file}.json")
    #     self.bal_sht = json.load(data)
    
    #     if validate:
    #         try:
    #             self.bal_sht["asset"]
    #         except KeyError:
    #             print(f"{file} is not a valid balance sheet!")
    
    #         while True:
    #             answer: str = input("Would you like to load the file anyway? (y/n)")
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


if __name__ == "__main__":
    balance_sheet: BalanceSheet = BalanceSheet()
    balance_sheet.add_account("cash", "asset", True)
    print(balance_sheet.bal_sht)