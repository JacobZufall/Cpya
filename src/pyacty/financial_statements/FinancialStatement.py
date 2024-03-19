"""
FinancialStatement.py

This class is mostly abstract because each financial statement is extremely unique. However, many of them require
similar functions, which is why this class exists and is inherited from.

This class also allows flexibility if someone wants to create their own financial statement from scratch.
"""

import os
import csv
from csv import writer
import json
from abc import abstractmethod
from typing import TextIO, final

from src.pyacty.constants import ALL_CATEGORIES
from src.pyacty.custom_types import fnstmt
from src.pyacty.custom_exceptions import SupportError


class FinancialStatement:
    def __init__(self) -> None:
        """
        A blank financial statement.
        """
        self.fs: fnstmt = {}

    @final
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

    # I'm sorry.
    @final
    def save_fs(self, directory: str, file_name: str, file_type: str = "all") -> None:
        """
        Saves the financial statement to the given directory.
        :param directory: The directory to save the financial statement to.
        :param file_name: The name of the file.
        :param file_type: The type of file to save to (CSV or JSON).
        :return: Nothing.
        """
        valid_file_types: list[str] = ["csv", "json"]

        def make_file(extension: str) -> TextIO:
            """
            Makes the file the data is saved to.
            :param extension: The type of file to save to.
            :return: The file to save the data to.
            """
            return open(f"{directory}\\{file_name}.{extension}", "w", newline="")

        def save_files(option: int) -> None:
            """
            Saves files specified by the argument.\n
            0: Saves all files.
            1: Saves CSV file only.
            2: Saves JSON file only.
            :param option: What types of files to save.
            :return: Nothing
            """
            outfile: TextIO

            # Having "or option == 0" included in each conditional makes it possible to save each file. It's also why
            # these are separate conditional statements and aren't chained.

            # CSV file
            if option == 1 or option == 0:
                try:
                    outfile = make_file("csv")

                except FileNotFoundError:
                    os.mkdir(directory)
                    outfile = make_file("csv")

                csv_writer: writer = csv.writer(outfile)

                for fs_category, fs_accounts in self.fs.items():
                    csv_writer.writerow([fs_category.capitalize()])

                    for account, attributes in fs_accounts.items():
                        value: float = 0.0

                        for attribute, info in attributes.items():
                            if attribute == "bal":
                                value = info

                        csv_writer.writerow(["", account, value])

                outfile.close()

            # JSON file
            if option == 2 or option == 0:
                try:
                    outfile = make_file("json")

                except FileNotFoundError:
                    os.mkdir(directory)
                    outfile = make_file("json")

                outfile.write(json.dumps(self.fs, indent=4))
                outfile.close()

        if file_type == "all":
            save_files(0)

        else:
            if file_type not in valid_file_types:
                raise ValueError("Invalid valid type.")

            if file_type.lower() == "csv":
                save_files(1)
            else:
                save_files(2)

    def load_fs(self, directory: str):
        """
        Considerations for this method:
        - Should it be overridden or final?
        - Should it return the loaded file or modify self.fs directly?
        - Should we only load JSON files or CSV files too?
        """
        if not directory.lower().endswith(".json"):
            raise SupportError("PyActy only supports loading .JSON files!")

        self.fs = json.load(open(directory))

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
