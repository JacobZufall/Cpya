"""
Money.py

The Money class is a class that is designed to be used internally in PyActy to assist in formatting numbers when they
are output to the console. The class attribute "show_decimals" can be changed to allow a user to either show or hide
decimals across an entire project easily.
"""

from typing import Any, override, Self

# Not sure if there's a better way to do this.
def assure_type(other) -> float | int:
    """
    Used to allow users to add/subtract/etc. an instance of Money with an integer or a float.
    :param other: The other instance that math is being performed on.
    :return: The value to add or subtract.
    """
    return other.value if type(other) == Money else other


class Money:
    show_decimals: bool = False

    def __init__(self, value: int | float = 0, symbol: str = "$") -> None:
        """
        An object to handle rounding and formatting for monetary values.
        :param value: The value of the object.
        :param symbol: The symbol that represents the desired currency.
        """
        self._value: float = value
        self.symbol: str = symbol

    # Dunders
    @override
    def __str__(self) -> str:
        return f"{self.symbol}{self.rounded_value:{self.num_format}}"

    def __add__(self, other: Any) -> Self:
        return Money(self.value + assure_type(other))

    def __radd__(self, other: Any) -> Self:
        return Money(assure_type(other) + self.value)

    def __eq__(self, other: Any) -> bool:
        return self.rounded_value == assure_type(other)

    def __float__(self) -> float:
        return float(self.value)

    def __floordiv__(self, other: Any) -> Self:
        return Money(self.value // assure_type(other))

    def __rfloordiv__(self, other: Any) -> Self:
        return Money(assure_type(other) // self.value)

    def __ge__(self, other: Any) -> bool:
        return self.rounded_value >= assure_type(other)

    def __gt__(self, other: Any) -> bool:
        return self.rounded_value > assure_type(other)

    def __int__(self) -> int:
        return int(self.value)

    def __le__(self, other: Any) -> bool:
        return self.rounded_value <= assure_type(other)

    def __lt__(self, other: Any) -> bool:
        return self.rounded_value < assure_type(other)

    def __mod__(self, other: Any) -> Self:
        return Money(self.value % assure_type(other))

    def __mul__(self, other: Any) -> Self:
        return Money(self.value * assure_type(other))

    def __rmul__(self, other: Any) -> Self:
        return Money(assure_type(other) * self.value)

    def __ne__(self, other: Any) -> bool:
        return self.rounded_value != assure_type(other)

    def __pow__(self, other: Any) -> Self:
        return Money(self.value ** assure_type(other))

    def __rpow__(self, other: Any) -> Self:
        return Money(assure_type(other) ** self.value)

    def __sub__(self, other: Any) -> Self:
        return Money(self.value - assure_type(other))

    def __rsub__(self, other: Any) -> Self:
        return Money(assure_type(other) - self.value)

    def __truediv__(self, other: Any) -> Self:
        return Money(self.value / assure_type(other))

    def __rtruediv__(self, other: Any) -> Self:
        return Money(assure_type(other) / self.value)

    # Properties
    @property
    def rounded_value(self) -> float:
        """
        When performing math such as addition, subtraction, multiplication, division, etc. on Money, we want to preserve
        every single decimal place to ensure the most accurate answer. However, when performing comparisons, or
        displaying the number to the user, we don't need to be more precise than the second decimal.
        :return: The value of Money, rounded to the nearest 100ths.
        """
        return round(self.value, 2)

    @property
    def num_format(self) -> str:
        return ",.2f" if self.show_decimals else ",.0f"

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, new_value: float | int) -> None:
        self._value = float(round(new_value, 2))
