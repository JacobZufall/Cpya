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
        self.name = name
        self.LIFE = life
        # The default value of an asset.
        self.D_VALUE = value
        self.value = self.D_VALUE
