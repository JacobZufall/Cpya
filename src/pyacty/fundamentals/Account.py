"""
Account.py
"""

from ..constants import BAL_TYPES


class Account:
    def __init__(self, name: str, normal_balance: str, balance: float, term: str | None = None) -> None:
        # Ensures normal_balance is either "debit" or "credit".
        if normal_balance not in BAL_TYPES:
            raise ValueError

        self.name: str = name
        self.normal_balance: str = normal_balance
        self.balance: float = balance
        self.term: str | None = term

    @property
    def true_balance(self) -> float:
        return self.balance if self.normal_balance == "debit" else self.balance * -1.0