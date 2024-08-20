"""
FinancialStatement.py

FinancialStatement is a partially abstract class due to the unique nature of each financial statement.

This class also serves as a blank statement for one to make their own custom financial statement.
"""

from abc import abstractmethod
import csv
from csv import writer
import json
import os
from typing import TextIO, final, override

from ..constants import ALL_CATEGORIES
from ..custom_types import fnstmt
from ..custom_exceptions import SupportError


class FinancialStatement:
    def __init__(self, company_name: str, date: str) -> None:
        """
        A blank financial statement.
        :param company_name: The name of the company.
        :param date: The date of the financial statement.
        """
        self.fs: fnstmt = {}
        self.company: str = company_name
        # This is more of a place-holder name. If someone is making a custom financial statement they can change it.
        self.fs_name: str = "Financial Statement"
        self.date: str = date

    @override
    def __str__(self) -> str:
        return Skeleton(self.fs, self.company, self.fs_name, self.date).return_output()

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__dict__}"

    def reset(self) -> None:
        """
        Returns the financial statement to its default state.
        :return: Nothing.
        """
        self.fs = {}

    # Is this not already handled by the TrueBalance class?
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
    # I'm not sure if this should be final or not. Overriding it may make it so that load_fs() won't work properly.
    # @final
    def save_fs(self, directory: str, file_name: str, file_type: str = "all") -> None:
        """
        Saves the financial statement to the given directory.
        :param directory: The directory to save the financial statement to.
        :param file_name: The name of the file.
        :param file_type: The type of file to save to (CSV or JSON).
        :return: Nothing.
        """
        valid_file_types: list[str] = ["csv", "json"]

        # I'm not entirely sure if I want this to be private or not.
        def __make_file(extension: str) -> TextIO:
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
            # TODO: When saving to a CSV file, we need to make contra-accounts negative/positive depending on what the
            #  non-contra equivalent is. For example, treasury stock should be stored in the CSV file as a negative
            #  number. Expenses should be negative as well. The true_value() function should be useful for this.
            if option == 1 or option == 0:
                try:
                    outfile = __make_file("csv")

                except FileNotFoundError:
                    os.mkdir(directory)
                    outfile = __make_file("csv")

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
                    outfile = __make_file("json")

                except FileNotFoundError:
                    os.mkdir(directory)
                    outfile = __make_file("json")

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

    def total_accounts(self) -> dict[str:float]:
        totals: dict[str:float] = {}

        for category, accounts in self.fs.items():
            for account, attributes in accounts.items():
                for attribute, value in attributes.items():
                    if attribute == "bal":
                        try:
                            totals[category] += value

                        except KeyError:
                            totals[category] = value

        return totals

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


if __name__ == "__main__":
    testFs: FinancialStatement = FinancialStatement("PyActy", "12/31/2024")
    print(testFs)
