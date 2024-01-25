"""
asset.py
"""


class Asset:
    def __init__(self, name: str, life: int, value: float):
        """
        :param name: The name of the asset.
        :param life: The life of the asset (months).
        :param value: The value of the asset ($).
        """
        self.name: str = name
        self.life: int = life
        self.value: float = value
        self.default_value: float = value

        self.rem_life: int = self.life
        self.syd: int = self._calc_syd()

    def change_life(self, new_life: int) -> None:
        """
        Changes the life of the asset and appropriately updates other attributes.
        :param new_life: The new life of the asset.
        :return: Nothing.
        """
        self.rem_life += new_life - self.life
        self.life = new_life

    @staticmethod
    def _calc_syd() -> int:
        """
        Calculates the sum of the years' digits to be used in calculating depreciation under the applicable method.
        :return: Sum of the years' digits.
        """
        running_total: int = 0

        for i in range(1, 6):
            print(i)
            running_total += i

        return running_total





