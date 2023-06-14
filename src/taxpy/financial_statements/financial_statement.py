"""
financial_statement.py
"""
from abc import abstractmethod


class FinancialStatement:
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
    def add_account(self, name: str, category: str, d_bal: bool) -> None:
        """
        Creates a new account with a default balance of $0.
        :param name: The name of the account.
        :param category: The category of the account (asset/liability/equity/revenue/expense).
        :param d_bal: Debit/credit balance. (True == debit, False == credit).
        :return: Nothing.
        """

    @abstractmethod
    def del_account(self, name: str) -> None:
        """
        Deletes a specified account from the financial statement..
        :param name: The name of the account.
        :return: Nothing.
        """

    def __init_subclass__(cls):
        pass
