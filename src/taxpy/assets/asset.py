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
        # self.LIFE = life
        self._life = life
        
        # The default value of an asset.
        # self.DEF_VALUE = value
        # self.value = self.DEF_VALUE
        
        # When declaring variables you do not wish to be changed by things outside of the class
        # we generally declare them as private, python doesn't have built in private variables
        # so any variable technically can be changed by the user but putting an _ in front of the
        # variable generally prevents it from being changed by the user and any use who does change
        # such a variable is signing themselfs up for any issues causes by such a change.
        self._default_value: float = value
        self.value: float = self.default_value
