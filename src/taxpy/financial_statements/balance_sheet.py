"""
balance_sheet.py
"""

from financial_statement import FinancialStatement


class BalanceSheet(FinancialStatement):
    def add_account(self, name: str, category: str, d_bal: bool) -> None:
        self.bs[category][name] = {
            "d/c": self.check_balance(d_bal),
            "bal": 0.0
        }

    def del_account(self, name: str) -> None:
        # This isn't pretty, but I don't have a better method at this moment.
        try:
            self.bs["asset"].pop(name)
        except KeyError:
            try:
                self.bs["liability"].pop(name)
            except KeyError:
                try:
                    self.bs["equity"].pop(name)
                except KeyError:
                    print("Account not found!")

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

        for k, v in self.bs.items():
            for j, w in v.items():
                if j == "bal":
                    totals[k] += w

        if totals["asset"] == (totals["liability"] + totals["equity"]):
            return True
        else:
            return False

    def true_value(self, account: str) -> float:
        try:
            self.bs["asset"][account]
        except KeyError:
            try:
                self.bs["liability"][account]
            except KeyError:
                try:
                    self.bs["equity"][account]
                except KeyError:
                    print("Account not found!")
                else:
                    return self.calc_true_value(self.bs, "equity", account)
            else:
                return self.calc_true_value(self.bs, "liability", account)
        else:
            return self.calc_true_value(self.bs, "asset", account)

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
        self.bs = {
            "asset": {},
            "liability": {},
            "equity": {}
        }

        super().__init__()


if __name__ == "__main__":
    balance_sheet: BalanceSheet = BalanceSheet()
    balance_sheet.add_account("cash", "asset", True)
    print(balance_sheet.bs)
    balance_sheet.del_account("cash")
    print(balance_sheet.bs)
