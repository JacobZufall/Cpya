"""
Money.py

The Money class is a class that is designed to be used internally in PyActy to assist in formatting numbers when they
are output to the console. The class attribute "show_decimals" can be changed to allow a user to either show or hide
decimals across an entire project easily.
"""

from typing import Any, override, Self


class Money:
    show_decimals: bool = False

    def __init__(self, value: int | float = 0, symbol: str = "$") -> None:
        """
        An object to handle rounding and formatting for monetary values.
        :param value: The value of the object.
        :param symbol: The symbol that represents the desired currency.
        """
        self._value: float = float(round(value, 2))
        self.symbol: str = symbol

    # Dunders
    @override
    def __str__(self) -> str:
        return f"{self.symbol}{self._value:{self.num_format}}"

    def __add__(self, other: Any) -> Self:
        return Money(self.value + other.value)

    def __eq__(self, other: Any) -> bool:
        return self.value == other.value

    def __floordiv__(self, other: Any) -> Self:
        return Money(self.value // other.value)

    def __ge__(self, other: Any) -> bool:
        return self.value >= other.value

    def __gt__(self, other: Any) -> bool:
        return self.value > other.value

    def __le__(self, other: Any) -> bool:
        return self.value <= other.value

    def __lt__(self, other: Any) -> bool:
        return self.value < other.value

    def __mod__(self, other: Any) -> Self:
        return Money(self.value % other.value)

    def __mul__(self, other: Any) -> Self:
        return Money(self.value * other.value)

    def __ne__(self, other: Any) -> bool:
        return self.value != other.value

    def __sub__(self, other: Any) -> Self:
        return Money(self.value - other.value)

    def __truediv__(self, other: Any) -> Self:
        return Money(self.value / other.value)

    # Properties
    @property
    def num_format(self) -> str:
        return ",.2f" if self.show_decimals else ",.0f"

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, new_value: float | int) -> None:
        self._value = float(round(new_value, 2))
