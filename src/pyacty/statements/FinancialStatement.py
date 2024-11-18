"""
FinancialStatement.py

This is the main class for all financial statement related classes. It is designed to serve as a blank template that is
easy to use and inherit.

PyActy also contains pre-made BalanceSheet and IncomeStatement classes, mainly for usage but also to provide an example
of how this class can be inherited and used.
"""

import csv
from csv import writer
import json
import os
from typing import TextIO, final, override

from .skeletons.FsSkeleton import FsSkeleton
from ..fundamentals.Account import Account
from ..fundamentals.Money import Money
from ..custom_exceptions import AccountExistsError


class FinancialStatement:
    def __init__(self, statement_name: str, company_name: str, date: str) -> None:
        """
        A blank financial statement.
        :param company_name: The name of the company.
        :param date: The date of the financial statement.
        """
        self.fn_stmt: dict[str:list[Account]] = {}
        self.company: str = company_name
        # This is more of a place-holder name. If someone is making a custom financial statement they can change it.
        self.fs_name: str = statement_name
        self.date: str = date

    @override
    def __str__(self) -> str:
        return FsSkeleton(self.fn_stmt, self.company, self.fs_name, self.date).auto_render()

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__dict__}"

    def reset(self) -> None:
        """
        Returns the financial statement to its default state.
        :return: Nothing.
        """
        self.fn_stmt = {}

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

        def _make_file(extension: str) -> TextIO:
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
            :param option: What types of file(s) to save.
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
                    outfile = _make_file("csv")

                except FileNotFoundError:
                    os.mkdir(directory)
                    outfile = _make_file("csv")

                csv_writer: writer = csv.writer(outfile)

                for fs_category, fs_accounts in self.fn_stmt.items():
                    csv_writer.writerow([fs_category.capitalize()])

                    for account in fs_accounts:
                        csv_writer.writerow(["", account.name, account.value])

                outfile.close()

            # JSON file
            if option == 2 or option == 0:
                try:
                    outfile = _make_file("json")

                except FileNotFoundError:
                    os.mkdir(directory)
                    outfile = _make_file("json")

                # Neither Account nor Money objects can be stored in a JSON file, so they must be serialized.
                serial_fs: dict[str:list[dict[str:str | bool | dict[str:str | int | float] | None]]] = {}

                for category, accounts in self.fn_stmt.items():
                    serial_fs[category] = []

                    for account in accounts:
                        serial_fs[category].append({
                            "name": account.name,
                            "normal_balance": account.normal_balance,
                            "balance": {
                                "value": account.balance.value,
                                "symbol": account.balance.symbol
                            },
                            "contra": account.contra,
                            "term": account.term
                        })

                outfile.write(json.dumps(self.fn_stmt, indent=4))
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

    @final
    def load_fs(self, directory: str):
        # TODO: Make it so financial statements can be loaded from files.
        pass

    def total_accounts(self) -> dict[str:float]:
        """
        Totals the value of each account in each financial statement category.
        :return: The totals, separated by category.
        """
        totals: dict[str:float] = {}

        for category, accounts in self.fn_stmt.items():
            for account in accounts:
                try:
                    totals[category] += account.balance

                except KeyError:
                    totals[category] = account.balance

        return totals

    def add_account(self, category: str = "", name: str = "", normal_balance: str = "debit",
                    starting_balance: float | Money = Money(), contra: bool = False, term: str | None = None,
                    new_account: Account | None = None) -> None:
        """
        Creates a new account and adds it to the financial statement.
        :param name: The name of the account.
        :param category: The category of the account (asset/liability/equity/revenue/expense).
        :param normal_balance: The normal balance of the account.
        :param starting_balance: The beginning balance of the account.
        :param contra: If the account is a contra-account or not.
        :param term: The term of the account (short or long).
        :param new_account: An already existing instance of Account. If this argument is filled, all other arguments
        (except category) are ignored.
        :return: Nothing.
        """
        # Ensures that the account doesn't already exist in ANY category. This means you can't have an account named
        # "Cash" in the "Assets" category and the "Equity" category.
        for _, accounts in self.fn_stmt.items():
            for account in accounts:
                if name == account.name:
                    raise AccountExistsError

        # A new account can be created with this function, or an already existing account may be used.
        if new_account is None:
            new_account = Account(name, normal_balance, starting_balance, contra, term)

        try:
            self.fn_stmt[category].insert(new_account)

        except KeyError:
            self.fn_stmt[category] = [new_account]

    def remove_account(self, name: str) -> None:
        """
        Deletes a specified account from the financial statement.
        :param name: The name of the account.
        :return: Nothing.
        """
        for category, accounts in self.fn_stmt.items():
            for i in range(len(accounts)):
                if name == accounts[i].name:
                    self.fn_stmt[category].remove(i)
                    break

        else:
            raise NameError
