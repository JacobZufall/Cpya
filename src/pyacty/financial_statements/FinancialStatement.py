"""
FinancialStatement.py

This class is mostly abstract because each financial statement is extremely unique. However, many of them require
similar functions, which is why this class exists and is inherited from.
"""
import os
import csv
from csv import writer
import json
from src.pyacty.constants import ALL_CATEGORIES
from abc import abstractmethod
from typing import TypeAlias, TextIO

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
                    return abs(self.fs[category][account]["balance"])
                else:
                    return self.fs[category][account]["balance"] * -1.0
            except KeyError:
                continue
        else:
            raise KeyError("Account not found!")

    def save_fs(self, directory: str, file_name: str, file_type: str = "csv") -> None:
        """
        Saves the financial statement to the given directory.
        :param directory: The directory to save the financial statement to.
        :param file_name: The name of the file.
        :param file_type: The type of file to save to (CSV or JSON).
        :return: Nothing.
        """
        valid_file_types: list[str] = ["csv", "json"]

        if file_type not in valid_file_types:
            raise ValueError("Invalid valid type.")

        # CSV file
        if file_type.lower() == valid_file_types[0]:
            outfile: TextIO

            try:
                outfile = open(f"{directory}\\{file_name}.csv", "w", newline="")
            except FileNotFoundError:
                os.mkdir(directory)
                outfile = open(f"{directory}\\{file_name}.csv", "w", newline="")

            csv_writer: writer = csv.writer(outfile)

            for fs_category, fs_accounts in self.fs.items():
                csv_writer.writerow([fs_category.capitalize()])

                for account, attributes in fs_accounts.items():
                    value: float = 0.0

                    for attribute, info in attributes.items():
                        if attribute == "bal":
                            value = info

                    csv_writer.writerow(["", account, value])

            else:
                # Inserts a blank row to separate the categories.
                csv_writer.writerow("")

        # JSON file
        elif file_type.lower() == valid_file_types[1]:
            with open(f"{directory}.{file_name}.json", "w") as outfile:
                outfile.write(self.fs)

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
