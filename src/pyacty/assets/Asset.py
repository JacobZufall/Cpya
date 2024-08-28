"""
Asset.py
"""

from typing import override

from ..fundamentals.Money import Money


class Asset:
    def __init__(self, name: str, life: int, value: Money | float | int) -> None:
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
        return self._life

    @life.setter
    def life(self, new_life) -> None:
        self._rem_life += new_life - self._life
        self._life = new_life

    @property
    def rem_life(self) -> int:
        return self._rem_life

    @property
    def syd(self) -> int:
        running_total: int = 0

        for i in range(1, self.life // 12 + 1):
            running_total += i

        return running_total

    @property
    def value(self) -> Money:
        return self._value

    @value.setter
    def value(self, new_value: Money | float | int) -> None:
        # I don't know if this should happen, but I can't think of any reason why it shouldn't...
        self._value = new_value if type(new_value) == Money else Money(new_value)
