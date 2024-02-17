"""
FinancialStatement.py
"""
from abc import abstractmethod
from typing import TypeAlias

# Is there a way to tie this to the class?
fnstmt: TypeAlias = dict[str:dict[str:dict[str:any]]]


class FinancialStatement:
    def __init__(self) -> None:
        pass

    @classmethod
    def check_balance(cls, bal: bool) -> str:
        if bal:
            return "debit"
        else:
            return "credit"

    @classmethod
    def calc_true_value(cls, fs: fnstmt, category: str, account: str) -> float:
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


class DefaultBal:
    def __init__(self, category: str, contra: bool = False):
        """
        :param category:
        :param contra:
        """
        self.def_bal: str | None = None

        # Balance sheet accounts
        self.asset: str = "debit"
        self.contra_asset: str = "credit"
        self.liability: str = "credit"
        self.contra_liability: str = "debit"
        self.equity: str = "credit"
        self.contra_equity: str = "debit"

        # Income statement accounts
        self.revenue: str = "credit"
        self.contra_revenue: str = "debit"
        self.expense: str = "debit"
        self.contra_expense: str = "credit"

        self.find_account(category, contra)

    def find_account(self, category: str, contra: bool = False) -> None:
        """
        :param category:
        :param contra:
        :return:
        """
        if not contra:
            self.def_bal = self.__getattribute__(category)
        else:
            self.def_bal = self.__getattribute__(f"contra_{category}")
