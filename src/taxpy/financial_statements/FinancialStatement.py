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

    # This method is terrible and could be vastly improved. It should be considered adding an attribute named
    # "self.fnstmt" to this class which is used by its children instead of each child having its own unique name for
    # their financial statement. This method would be a lot better if it weren't static as well.
    @staticmethod
    def calc_true_value(fs: fnstmt, category: str, account: str) -> float:
        """

        :param fs: The financial statement the category is in.
        :param category: The category the account is in.
        :param account: The account to find the true value of.
        :return: The true value of the account.
        """
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
