"""
TangibleAsset.py
"""
from typing import override

from .Asset import Asset
from ..fundamentals.Money import Money


class TangibleAsset(Asset):
    # Dunders
    def __init__(self, name: str, life: int, value: Money | float | int, slvg_value: Money | float | int = 0.0,
                 prod_cap: int = 0) -> None:
        """
        A tangible asset, which includes additional properties and methods specific to tangible assets.
        :param name: The name of the asset.
        :param life: The life of the asset (in months).
        :param value: The value of the asset.
        :param slvg_value: The salvage value of the asset.
        :param prod_cap: The estimated maximum production of the asset.
        """
        super().__init__(name, life, value)
        self._slvg_value: Money = slvg_value if type(slvg_value) == Money else Money(slvg_value)
        # I don't think prod_cap needs any further considerations, since it's just a denominator in a single equation.
        self.prod_cap: int = prod_cap
        # Also known as accumulated depreciation.
        self._total_depr: Money = Money()

        # Stored for later use.
        self.init_values["slvg_value"] = self._slvg_value
        self.init_values["prod_cap"] = self.prod_cap

    # Properties
    @property
    def depreciable_allocation(self) -> Money:
        """
        :return: The asset's value that is allowed to be depreciated.
        """
        return self.value - self.slvg_value

    # Unlike depreciable_allocation, depreciable_value doesn't include dollars that have already been depreciated.
    @property
    def depreciable_value(self) -> Money:
        """
        :return: The asset's value that can currently be depreciated.
        """
        return self.net_value - self.slvg_value

    @property
    def net_value(self) -> Money:
        """
        :return: The current value of the asset net of accumulated depreciation.
        """
        return self.value - self.total_depr

    @property
    def slvg_value(self) -> Money:
        """
        :return: The asset's salvage value.
        """
        return self._slvg_value
    
    @slvg_value.setter
    def slvg_value(self, new_value: Money | float | int) -> None:
        """
        Updates the salvage value of the asset and automatically handles types.
        :param new_value: The new salvage value of the asset.
        """
        self._slvg_value = new_value if type(new_value) == Money else Money(new_value)

    @property
    def syd(self) -> int:
        """
        :return: The denominator used when calculating depreciation using the Sum of the Years' Digits method.
        """
        running_total: int = 0

        for i in range(1, self.life // 12 + 1):
            running_total += i

        return running_total

    @property
    def total_depr(self) -> Money:
        """
        :return: The total dollar value currently depreciated.
        """
        return self._total_depr

    # I can't think of a good reason to use this, but I figured it's a good idea to provide a safe way to hard-key in
    # a number.
    @total_depr.setter
    def total_depr(self, new_value: Money | float | int):
        """
        Updates the total value depreciated and automatically handles types.
        :param new_value: The new value of the asset which has been depreciated.
        :return: Nothing.
        """
        self._total_depr = new_value if type(new_value) == Money else Money(new_value)

    # Methods
    def _validate_depreciation(self, depr_amt: Money) -> Money:
        """
        Validates the amount of depreciation to ensure that the net value of the asset does not go below zero or its
        salvage value.
        :param depr_amt: The amount being depreciated.
        :return: The amount that is permitted to be depreciated.
        """
        actual_depr: Money

        if depr_amt <= self.net_value:
            self.total_depr += depr_amt
            actual_depr = depr_amt

        else:
            self.total_depr += self.depreciable_value
            actual_depr = self.depreciable_value

        return actual_depr

    def depreciate(self, method: int, periods: int = 12, decline: float = 1.0, units_prod: int = 0) -> Money:
        """
        [Supported Depreciation Methods] \n
        0: Straight Line Method \n
        1: Declining Balance Method \n
        2: Sum of the Years' Digits Method \n
        3: Units of Production Method \n
        :param method: The method of depreciation to use.
        :param periods: How many periods to depreciate (in months).
        :param decline: The decline used when depreciating with the Declining Balance Method.
        :param units_prod: The number of units produced, used when depreciating with the Units of Production Method.
        :return: The dollar value depreciated.
        """
        total_depreciated: Money = Money()

        match method:
            # Straight Line
            case 0:
                total_depreciated = self._validate_depreciation((self.depreciable_allocation / self.life) * periods)

            # Declining Balance
            case 1:
                total_depreciated = self._validate_depreciation(((self.net_value / self.life) * decline) * periods)

            # Sum of the Years' Digits
            case 2:
                total_depreciated = self._validate_depreciation(self.depreciable_allocation *
                                                                ((self._rem_life / 12) / self.syd))

            # Units of Production
            case 3:
                total_depreciated = self._validate_depreciation((self.depreciable_value / self.prod_cap) * units_prod)

        self._rem_life -= periods

        return total_depreciated

    # Is there a more efficient way to override this?
    @override
    def reset(self) -> None:
        self.__init__(
            self.init_values["name"],
            self.init_values["life"],
            self.init_values["value"],
            self.init_values["slvg_value"],
            self.init_values["prod_cap"]
        )
