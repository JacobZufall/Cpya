"""
balance_sheet.py
"""


class BalanceSheet:
    @staticmethod
    def __check_balance(bal: bool) -> str:
        if bal:
            return "debit"
        else:
            return "credit"

    def add_account(self, name: str, category: str, d_bal: bool) -> None:
        """
        Creates a new account with a default balance of $0.
        :param name: The name of the account.
        :param category: The category of the account (asset/liability/equity).
        :param d_bal: Debit/credit balance. (True == debit, False == credit).
        :return: Nothing.
        """
        self.bs[category][name] = {
            "d/c": self.__check_balance(d_bal),
            "bal": 0.0
        }

    def del_account(self, name: str) -> None:
        """
        Deletes a specified account from the balance sheet.
        :param name: The name of the account.
        :return: Nothing.
        """

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

    def __calc_true_value(self, category: str, account: str,) -> float:
        """
        :param category: The category of the account.
        :param account: The name of the account.
        :return: The true value of the account.
        """
        if self.bs[category][account]["d/c"] == "debit":
            return abs(self.bs[category][account]["balance"])
        else:
            return self.bs[category][account]["balance"] * -1

    def true_value(self, account: str) -> float:
        """
        Returns a debit account as a positive float and a credit account as a negative float.
        :param account: The name of the account.
        :return: The true value of an account.
        """
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
                    return self.__calc_true_value("equity", account)
            else:
                return self.__calc_true_value("liability", account)
        else:
            return self.__calc_true_value("asset", account)

    def __init__(self):
        """
        Here is and example of what the balance sheet looks like.\n
        Type is dict[str:dict[str:[dict[str:any]]], if needed.

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


if __name__ == "__main__":
    balance_sheet: BalanceSheet = BalanceSheet()
    balance_sheet.add_account("cash", "asset", True)
    print(balance_sheet.bs)
    balance_sheet.del_account("cash")
    print(balance_sheet.bs)
