"""
Asset.py
"""

from typing import final


class Asset:
    def __init__(self, name: str, life: int, value: float) -> None:
        """
        :param name: The name of the asset.
        :param life: The life of the asset (months).
        :param value: The value of the asset ($).
        """
        self.name: str = name

        self.life: int = life
        self.rem_life: int = life

        self.def_value: float = value
        self.value: float = value

        self.syd: int = self._calc_syd(self.life)

    def reset(self) -> None:
        """
        Returns an asset to its original state. Designed to be used for testing.
        :return: Nothing.
        """
        self.value = self.def_value
        self.rem_life = self.life

    @final
    def update_life(self, new_life: int) -> None:
        """
        Changes the base-life of the asset and appropriately updates other attributes.
        :param new_life: The new life of the asset.
        :return: Nothing.
        """
        self.rem_life += new_life - self.life
        self.life = new_life
        self.syd = self._calc_syd(self.life)

    def update_value(self, new_value: float) -> None:
        """
        Changes the base-value of the asset and appropriately updates other attributes.
        :param new_value: The new value of the asset.
        :return: Nothing.
        """
        self.value += new_value - self.def_value
        self.def_value = new_value

    @staticmethod
    def _calc_syd(life: int) -> int:
        """
        Calculates the sum of the years' digits to be used in calculating depreciation under the applicable method.
        :param life: The life of the asset in months, usually self.LIFE when used internally.
        :return: Sum of the years' digits.
        """
        running_total: int = 0

        for i in range(1, int(life / 12) + 1):
            running_total += i

        return running_total
