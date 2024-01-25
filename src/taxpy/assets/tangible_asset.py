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
        # Used to store the previous amount depreciated for non-linear methods.
        self._prev_depr: int = 0
        self.amount_depreciated: float = 0.0

    def depreciate(self, method: int, periods: int = 1, decline: float = 1.0) -> float:
        """
        [Supported Depreciation Methods] \n
        0: Straight Line Method \n
        1: Declining Balance Method \n
        2: Sum of the Years' Digits Method \n
        3: Units of Production Method \n
        :param method: The depreciation method.
        :param periods: The number of periods (months) to depreciate.
        :param decline: The factor used in the declining balance method (2.0 = 200%).
        :return: Nothing.
        """
        if self.depr_value > 0:
            # I'm not sure if this works properly yet. It's hard to think about depreciation in this way and I have A
            # LOT of attributes flying around, which is making it hard to keep track of.
            match method:
                # Straight Line
                case 0:
                    self.amount_depreciated: float = periods * (self.depr_value / self.life)
                    self.value -= self.amount_depreciated
                    self.rem_life -= periods

                    self.depr_value = self.value - self.slvg_value

                # Declining Balance
                case 1:
                    self.amount_depreciated = self.value * ((self.default_value / self.life) * decline)

                    # Salvage value isn't calculated into declining balance, so this checks to make sure the value of
                    # the asset doesn't turn negative.
                    if self.amount_depreciated > self.depr_value:
                        self.amount_depreciated = self.depr_value

                    self.value -= self.amount_depreciated
                    self.rem_life -= periods

                # Sum of the Years' Digits
                case 2:
                    self.amount_depreciated = self.default_value * (self.rem_life / self.syd)

                # Units of Production
                case 3:
                    pass

        else:
            # The amount of value that can be depreciated cannot be negative.
            if self.depr_value < 0:
                self.depr_value = 0

            print(f"Asset \"{self.name}\" is fully depreciated! Current value = {self.value}.")
            self.amount_depreciated = 0.0

        return self.amount_depreciated
