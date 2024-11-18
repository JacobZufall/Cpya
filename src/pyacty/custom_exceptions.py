"""
custom_exceptions.py
"""

from typing import Any


class SupportError(Exception):
    def __init__(self, message: Any):
        super().__init__(message)


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
