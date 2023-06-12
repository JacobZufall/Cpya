"""
tangible_assets.py
"""

from asset import Asset


class TangibleAsset(Asset):
    def __init__(self, name: str, life: int, value: float, s_value: float = 0.0):
        """

        :param name: The name of the asset.
        :param life: The life of the asset (months).
        :param value: The value of the asset ($).
        :param s_value: The salvage value of the asset.
        """
        super().__init__(name=name, life=life, value=value)
        self.s_value = s_value
        # The depreciable value.
        self.d_value = value - s_value

    def depreciate(self, periods: int = 1):
        """

        :param periods: The number of periods (months) to depreciate.
        :return: Nothing.
        """
        self.value -= periods * (self.d_value / self.life)
        self.d_value = self.value - self.s_value
