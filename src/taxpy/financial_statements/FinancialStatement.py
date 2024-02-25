"""
FinancialStatement.py

This class is mostly abstract because each financial statement is extremely unique. However, many of them require
similar functions, which is why this class exists and is inherited from.
"""

from src.taxpy.constants import ALL_CATEGORIES
from abc import abstractmethod
from typing import TypeAlias

# Is there a way to tie this to the class?
fnstmt: TypeAlias = dict[str:dict[str:dict[str:any]]]


class FinancialStatement:
    def __init__(self) -> None:
        self.fs: fnstmt = {}

    def true_value(self, account: str) -> float:
        """
        Finds the true value of an account, which is a positive float if the normal balance of the account is a
        debit, and a negative float if the normal balance of the account is a credit.
        :param account: The account to find the true value of.
        :return: The true value of the account.
        """
        # Looping through ALL_CATEGORIES allows this method to work with any financial statement saving the work of
        # having to override the method for each child class.
        for category in ALL_CATEGORIES:
            try:
                if self.fs[category][account]["d/c"] == "debit":
                    # All values should be stored as positive floats, but this is just in case they aren't for some
                    # reason. Accounts have no reason to be negative.
                    return_value = abs(self.fs[category][account]["balance"])
                    break
                else:
                    return_value = self.fs[category][account]["balance"] * -1.0
                    break
            except KeyError:
                continue
        else:
            raise KeyError("Account not found!")
        # Make two return statements.
        return return_value
                
    @abstractmethod
    def add_account(self, name: str, category: str, start_bal: float = 0.0, contra: bool = False) -> None:
        """
        Creates a new account with a default balance of $0.
        :param name: The name of the account.
        :param category: The category of the account (asset/liability/equity/revenue/expense).
        :param start_bal: The beginning balance of the account.
        :param contra: If the account is a contra account.
        :return: Nothing.
        """

    @abstractmethod
    def del_account(self, name: str) -> None:
        """
        Deletes a specified account from the financial statement.
        :param name: The name of the account.
        :return: Nothing.
        """
