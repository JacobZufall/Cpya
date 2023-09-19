"""
financial_statement.py
"""
from abc import abstractmethod


class FinancialStatement:
    def __init__(self):
        pass
    
    @classmethod
    def check_balance(cls, bal: bool) -> str:
        if bal:
            return "debit"
        else:
            return "credit"

    @classmethod
    def calc_true_value(cls, fs: dict[str:dict[str:dict[str:any]]], category: str, account: str, ) -> float:
        if fs[category][account]["d/c"] == "debit":
            return abs(fs[category][account]["balance"])
        else:
            return fs[category][account]["balance"] * -1

    @abstractmethod
    def true_value(self, account: str) -> float:
        """
        Returns a debit account as a positive float and a credit account as a negative float.
        :param account: The name of the account.
        :return: The true value of an account.
        """

    @abstractmethod
    def add_account(self, name: str, category: str, contra: bool):
        """
        Creates a new account with a default balance of $0.
        :param name: The name of the account.
        :param category: The category of the account (asset/liability/equity/revenue/expense).
        :param contra: If the account is a contra account.
        :return: Nothing.
        """

    @abstractmethod
    def del_account(self, name: str) -> None:
        """
        Deletes a specified account from the financial statement..
        :param name: The name of the account.
        :return: Nothing.
        """

    # @abstractmethod
    # def save_fs(self, file_name: str, path: str = "data/bal_sht/"):
    #     """
    #     :param file_name: The name of the JSON file to be created.
    #     :param path: The folder the file should be saved to.
    #     :return: Nothing.
    #     """
    #
    # @abstractmethod
    # def load_fs(self, file: str, validate: bool = True):
    #     """
    #     Loads said file and validates that it is the correct financial statement.
    #     :param file: The name of the JSON file to open.
    #     :param validate: Checks if the file being loaded is the correct financial statement.
    #     :return: Nothing.
    #     """


class DefaultBal:
    def __init__(self, category: str, contra: bool = False):
        # Balance sheet accounts.
        self.def_bal = None
        self.asset = "debit"
        self.contra_asset = "credit"
        self.liability = "credit"
        self.contra_liability = "debit"
        self.equity = "credit"
        self.contra_equity = "debit"

        # Income statement accounts.
        self.revenue = "credit"
        self.contra_revenue = "debit"
        self.expense = "debit"
        self.contra_expense = "credit"

        self.find_account(category, contra)

    def find_account(self, category: str, contra: bool = False):
        if not contra:
            self.def_bal = self.__getattribute__(category)
        else:
            self.def_bal = self.__getattribute__(f"contra_{category}")
