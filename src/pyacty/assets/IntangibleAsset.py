"""
IntangibleAsset.py

Unlike hte TangibleAsset class, this class doesn't override the reset method inherited from Asset. I don't think it
needs to because IntangibleAsset doesn't have any unique values, besides _total_amort, which always starts as a
brand-new instance of Money (which is $0).

I'm not sure if Python actually behaves as I'm expecting it to, however.
"""

from .Asset import Asset
from ..fundamentals.Money import Money


class IntangibleAsset(Asset):
    # Dunders
    def __init__(self, name: str, life: int, value: float):
        super().__init__(name, life, value)
        # Also known as accumulated amortization.
        self._total_amort: Money = Money()

    # Properties
    @property
    def net_value(self) -> Money:
        return self.value - self.total_amort

    @property
    def total_amort(self) -> Money:
        return self._total_amort

    @total_amort.setter
    def total_amort(self, new_value: Money | float | int):
        self._total_amort = new_value if type(new_value) == Money else Money(new_value)

    # Methods
    def _validate_amortization(self, amort_amt: Money) -> Money:
        actual_amort: Money

        if amort_amt <= self.net_value:
            self.total_amort += amort_amt
            actual_amort = amort_amt

        else:
            self.total_amort += self.net_value
            actual_amort = self.net_value

        return actual_amort

    def amortize(self, method: int, periods: int = 12, decline: float = 1.0) -> Money:
        """
        [Supported Amortization Methods] \n
        0: Straight Line Method \n
        1: Declining Balance Method \n
        :param method:
        :param periods:
        :param decline:
        :return:
        """
        total_amortized: Money = Money()

        match method:
            # Straight Line
            case 0:
                total_amortized = self._validate_amortization((self.value / self.life) * periods)

            # Declining Balance
            case 1:
                total_amortized = self._validate_amortization(((self.net_value / self.life) * decline) * periods)

            # Should other cases be added for annuity, bullet, balloon, and negative amortization?

        return total_amortized
