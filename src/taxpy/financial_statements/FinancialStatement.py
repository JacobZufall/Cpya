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

    @staticmethod
    def calc_true_value(fs: fnstmt, category: str, account: str) -> float:
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
