"""
Money.py

The Money class is a class that is designed to be used internally in PyActy to assist in formatting numbers when they
are output to the console. The class attribute "show_decimals" can be changed to allow a user to either show or hide
decimals across an entire project easily.
"""

from typing import override


class Money:
    show_decimals: bool = False

    def __init__(self, value: int | float, symbol: str = "$") -> None:
        """
        An object to handle rounding and formatting for monetary values.
        :param value: The value of the object.
        :param symbol: The symbol that represents the desired currency.
        """
        self._value: float = float(round(value, 2))
        self.symbol: str = symbol

    @override
    def __str__(self) -> str:
        return f"{self.symbol}{self._value:{self.num_format}}"

    @property
    def num_format(self) -> str:
        return ",.2f" if self.show_decimals else ",.0f"

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, new_value: float | int) -> None:
        self._value = float(round(new_value, 2))
