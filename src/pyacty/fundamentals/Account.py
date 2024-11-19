"""
Account.py

The justification for this class is to reduce the amount of for loops used in other files to improve readability. Prior
    to this class, dictionaries were used, which required nested loops often, which got annoying. The ability to access
    an attribute directly reduces the amount of for loops needed.

Alternatively, I considered making a "Category" class, since a category holds a bunch of instances of Account inside
    an instance of FinancialStatement. However, I decided against this so that the Account class could be used in more
    places. Also, it felt unnecessary to have a category be anything more than a list.

TODO: Add support for a t-chart so that one can view the history of changes to the balance of the account easily. My
    idea for this involves making the balance attribute private and using getters and setters, so that when the value is
    set we can record the change to a certain list, and then display all changes when the t-chart is called.
"""

from typing import override

from .Money import Money
from ..constants import BAL_TYPES


class Account:
    def __init__(self, name: str, normal_balance: str, balance: int | float | Money, contra: bool = False,
                 term: str | None = None) -> None:
        # Ensures normal_balance is either "debit" or "credit".
        if normal_balance.lower() not in BAL_TYPES:
            raise ValueError

        self.name: str = name
        self.normal_balance: str = normal_balance.lower()
        self.balance: Money = balance if isinstance(balance, Money) else Money(balance)
        self.contra: bool = contra
        self.term: str | None = term

    # Dunders
    @override
    def __str__(self) -> str:
        return (f"{self.name}:\n"
                f"    Normal balance: {self.normal_balance}\n"
                f"    Term: {self.term}\n"
                f"    Balance: {self.balance}")

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__dict__}"

    # TODO: When performing arithmatic on this class, should a new account be returned that has all the properties of
    #  the account on the left side of the operation (with the new balance)? Or, should it just return the new balance?

    # Properties
    @property
    def true_balance(self) -> Money:
        multiplier: int = 1

        if (self.normal_balance == "debit" and self.contra) or self.normal_balance == "credit":
            multiplier = -1

        return self.balance * multiplier
