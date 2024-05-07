"""
Money.py

# TODO: Implement this project wide after all the formatting going on in financial_statements is complete.
"""

from typing import override


class Money:
    def __init__(self, value: int | float, symbol: str = "$") -> None:
        """
        An object to handle rounding and formatting for monetary values.
        :param value: The value of the object.
        :param symbol: The symbol that represents the desired currency.
        """
        self.value: float = float(round(value, 2))
        self.symbol: str = symbol

    @override
    def __str__(self) -> str:
        return f"{self.symbol}{self.value:,2f}"

    def update_value(self, new_value: int | float) -> None:
        """
        Updates the value of a Money object and appropriately rounds it.
        :param new_value: The value to change the object to.
        :return: Nothing
        """
        self.value = float(round(new_value, 2))
