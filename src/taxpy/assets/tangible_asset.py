"""
tangible_assets.py
"""

from src.taxpy.assets.asset import Asset


class TangibleAsset(Asset):
    def __init__(self, name: str, life: int, value: float, slvg_value: float = 0.0, prod_cap: int = 0) -> None:
        """
        :param name: The name of the asset.
        :param life: The life of the asset (months).
        :param value: The value of the asset ($).
        :param slvg_value: The salvage value of the asset ($).
        """
        super().__init__(name=name, life=life, value=value)
        self.slvg_value: float = slvg_value
        self.prod_cap: int = prod_cap

        self.depr_value: float = self.value - self.slvg_value
        self.amt_depr: float = 0.0

    # I'm not sure if this should be moved to the parent class or not.
    def _update_values(self, periods: int) -> None:
        """
        Re-runs all values to make sure they're consistent with each other. Used after depreciating.
        :param periods:
        :return: Nothing.
        """
        self.value -= self.amt_depr
        self.depr_value = self.value - self.slvg_value
        self.rem_life -= periods

    def depreciate(self, method: int, periods: int = 1, decline: float = 1.0, units_prod: int = 0) -> float:
        """
        [Supported Depreciation Methods] \n
        0: Straight Line Method \n
        1: Declining Balance Method \n
        2: Sum of the Years' Digits Method \n
        3: Units of Production Method \n
        :param method: The depreciation method.
        :param periods: The number of periods (months) to depreciate.
        :param decline: The factor used in the declining balance method (2.0 = 200%).
        :param units_prod: How many units produced, if using method 3.
        :return: The dollar value depreciated.
        """
        if self.depr_value > 0:
            # I'm not sure if this works properly yet. It's hard to think about depreciation in this way and I have A
            # LOT of attributes flying around, which is making it hard to keep track of.
            match method:
                # Straight Line
                case 0:
                    self.amt_depr: float = periods * (self.depr_value / self.life)
                    self._update_values(periods)

                # Declining Balance
                case 1:
                    self.amt_depr = self.value * ((self.default_value / self.life) * decline)
                    # Salvage value isn't calculated into declining balance, so this checks to make sure the value of
                    # the asset doesn't turn negative.
                    if self.amt_depr > self.depr_value:
                        self.amt_depr = self.depr_value
                    self._update_values(periods)

                # Sum of the Years' Digits
                case 2:
                    self.amt_depr = self.default_value * (self.rem_life / self.syd)
                    self._update_values(periods)

                # Units of Production
                case 3:
                    self.amt_depr = (self.depr_value / self.prod_cap) * units_prod
                    self._update_values(periods)

        else:
            # The amount of value that can be depreciated cannot be negative.
            if self.depr_value < 0:
                self.depr_value = 0

            print(f"Asset \"{self.name}\" is fully depreciated! Current value = {self.value}.")
            self.amt_depr = 0.0

        return self.amt_depr
