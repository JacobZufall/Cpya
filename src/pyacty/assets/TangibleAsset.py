"""
TangibleAsset.py
"""

from .Asset import Asset
from ..fundamentals.Money import Money


class TangibleAsset(Asset):
    def __init__(self, name: str, life: int, value: Money | float | int, slvg_value: Money | float | int = 0.0,
                 prod_cap: int = 0) -> None:
        super().__init__(name, life, value)
        self._slvg_value: Money = slvg_value if type(slvg_value) == Money else Money(slvg_value)
        self.prod_cap: int = prod_cap
        # Also known as accumulated depreciation.
        self._total_depr: Money = Money()

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
        return self._slvg_value
    
    @slvg_value.setter
    def slvg_value(self, new_value: Money | float | int) -> None:
        self._slvg_value = new_value if type(new_value) == Money else Money(new_value)

    @property
    def total_depr(self) -> Money:
        return self._total_depr

    @total_depr.setter
    def total_depr(self, new_value: Money | float | int):
        self._total_depr = new_value if type(new_value) == Money else Money(new_value)

    # Methods
    def _validate_depreciation(self, depr_amt: Money) -> Money:
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
        :param method:
        :param periods:
        :param decline:
        :param units_prod:
        :return:
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
