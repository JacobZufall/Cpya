"""
custom_exceptions.py
"""

from typing import Any


class AccountExistsError(Exception):
    def __init__(self, message: Any) -> None:
        """
        Account already exists.
        """
        super.__init__(message)


class AccountNotFoundError(Exception):
    def __init__(self, message: Any) -> None:
        """
        Account not found.
        """
        super().__init__(message)
