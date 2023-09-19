"""
intangible_asset.py
"""

from asset import Asset


class IntangibleAsset(Asset):
    def __init__(self, name: str, life: int, value: float):
        """

        :param name: The name of the asset.
        :param life: The life of the asset (months)).
        :param value: The value of the asset.
        """
        super().__init__(name=name, life=life, value=value)
    
    def amortize(self, periods: int = 1) -> None:
        """

        :param periods: The number of periods (usually years) to depreciate.
        :return: Nothing.
        """
        self.value -= periods * (self.value / self._life)

    
