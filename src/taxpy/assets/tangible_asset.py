"""
tangible_assets.py
"""

from asset import Asset


class TangibleAsset(Asset):
    def __init__(self, name: str, life: int, value: float, slvg_value: float = 0.0):
        """
        :param name: The name of the asset.
        :param life: The life of the asset (months).
        :param value: The value of the asset ($).
        :param slvg_value: The salvage value of the asset ($).
        """
        super().__init__(name=name, life=life, value=value)
        self.slvg_value: float = slvg_value

        self.depr_value: float = self.value - self.slvg_value
        self.rem_life: int = self._life
        # Used to store the previous amount depreciated for non-linear methods.
        self._prev_depr: int = 0

    def depreciate(self, method: int, periods: int = 1, decline: float = 1.0) -> None:
        """
        [Supported Depreciation Methods] \n
        0: Straight Line Method \n
        1: Declining Balance Method \n
        2: Sum of the Years' Digits Method \n
        3: Units of Production Method \n
        :param method: The depreciation method.
        :param periods: The number of periods (months) to depreciate.
        :return: Nothing.
        """
        if self.depr_value > 0:
            match method:
                # Straight Line
                case 0:
                    self.value -= periods * (self.depr_value / self._life)
                    self.rem_life -= periods

                    self.depr_value = self.value - self.slvg_value

                # Declining Balance
                case 1:
                    pass

                # Sum of the Years' Digits
                case 2:
                    pass

                # Units of Production
                case 3:
                    pass

        else:
            # The amount of value that can be depreciated cannot be negative.
            if self.depr_value < 0:
                self.depr_value = 0

            print(f"Asset \"{self.name}\" is fully depreciated! Current value = {self.value}.")

    def change_life(self, new_life: int) -> None:
        self.rem_life += new_life - self._life
