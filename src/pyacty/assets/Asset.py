"""
Asset.py
"""

from typing import override

from ..fundamentals.Money import Money


class Asset:
    def __init__(self, name: str, life: int, value: Money | float | int) -> None:
        """
        A partially abstract class.
        :param name: The name of the asset.
        :param life: The life of the asset (in months).
        :param value: The value of the asset.
        """
        self.name: str = name
        self._life: int = life
        self._rem_life: int = life
        self._value: Money = value if type(value) == Money else Money(value)

    # Dunders
    @override
    def __str__(self) -> str:
        pass

    # Properties
    @property
    def life(self) -> int:
        """
        :return: The life of the asset (in months).
        """
        return self._life

    @life.setter
    def life(self, new_life) -> None:
        """
        Updates the life and remaining life of an asset accordingly.
        :param new_life: The new life of the asset (in months).
        :return: Nothing.
        """
        self._rem_life += new_life - self._life
        self._life = new_life

    @property
    def rem_life(self) -> int:
        """
        :return: The remaining life of the asset (in months).
        """
        return self._rem_life

    @property
    def value(self) -> Money:
        """
        :return: The value of the asset.
        """
        return self._value

    # I believe that since any change in value is considered a change of an accounting estimate, everything is handled
    # prospectively, so we don't need to touch other numbers like the totals for depreciation and amortization.
    @value.setter
    def value(self, new_value: Money | float | int) -> None:
        """
        Updates the value of the asset and automatically handles types.
        :param new_value: The new value of the asset.
        :return: Nothing.
        """
        # I don't know if this should happen, but I can't think of any reason why it shouldn't...
        self._value = new_value if type(new_value) == Money else Money(new_value)
