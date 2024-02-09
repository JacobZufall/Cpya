"""
Computer.py

The default life of a computer, per GAAP, is 5 years (60 months).
"""

from src.taxpy.assets.TangibleAsset import TangibleAsset


class Computer(TangibleAsset):
    def __init__(self, name: str, value: float, s_value: float = 0):
        """
        Per GAAP, the default life is 5 years (60 months). This can be changed by modifying the life attribute.
        :param name: The name of the asset.
        :param value: The value of the asset ($).
        :param s_value: The salvage value of the asset ($).
        """
        super().__init__(name=name, life=60, value=value, s_value=s_value)
