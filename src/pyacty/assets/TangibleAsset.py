"""
TangibleAsset.py
"""

from .Asset import Asset




# class TangibleAsset(Asset):
#     def __init__(self, name: str, life: int, value: float, slvg_value: float = 0.0, prod_cap: int = 0) -> None:
#         """
#         :param name: The name of the asset.
#         :param life: The life of the asset (months).
#         :param value: The value of the asset ($).
#         :param slvg_value: The salvage value of the asset, if any ($).
#         :param prod_cap: The production capacity of the asset (if applicable).
#         """
#         super().__init__(name, life, value)
#         self.slvg_value: float = slvg_value
#         self.prod_cap: int = prod_cap
#
#         # The reason these are lists is so that someone can easily recall what the depreciation or total depreciation
#         # was n amount of years ago. For example, you can write "self.last_depr[-1]" to get the depreciation from the
#         # most recent period.
#         # This is the $ amount that can be depreciated.
#         self.depreciable_value: Delta = Delta(self.value - self.slvg_value)
#         self.last_depr: Delta = Delta(0.0)
#         self.total_depr: Delta = Delta(0.0)
#
#     @override
#     def __str__(self):
#         return (f"{self.name} has a life of {self.life:,} months, a value of ${self.value:,}, a salvage value of "
#                 f"${self.slvg_value:,}, and a production capacity of {self.prod_cap:,} units.")
#
#     @override
#     def __repr__(self):
#         return f"{self.__class__.__name__}: {self.__dict__}"
#
#     @override
#     def reset(self) -> None:
#         super().reset()
#         self.depreciable_value = Delta(self.value - self.slvg_value)
#         self.last_depr.reset()
#         self.total_depr.reset()
#
#     @override
#     def update_value(self, new_value: float) -> None:
#         super().update_value(new_value)
#         self.depreciable_value.change_value(self.value - self.slvg_value)
#
#     def update_slvg(self, new_slvg: float) -> None:
#         """
#         Updates the salvage value of the asset.
#         :param new_slvg: The new salvage value of the asset.
#         :return: Nothing
#         """
#         self.slvg_value = new_slvg
#         # Need to update self.depreciable_value, so we just run change_value but use the current value as the new value.
#         self.update_value(self.value)
#
#     def _update_attribs(self, periods: int) -> None:
#         """
#         Re-runs all values to make sure they're consistent with each other. Used after depreciating.
#         :param periods:
#         :return: Nothing.
#         """
#         self.value -= self.last_depr.get_value()
#         self.total_depr.change_value(self.total_depr.get_value() + self.last_depr.get_value())
#         self.depreciable_value.change_value(self.value - self.slvg_value)
#         self.rem_life -= periods
#
#     def _validate_depreciation(self, depr_amt: float) -> bool:
#         return depr_amt < self.depreciable_value.get_value()
#
#     def depreciate(self, method: int, periods: int = 1, decline: float = 1.0, units_prod: int = 0) -> float:
#         """
#         [Supported Depreciation Methods] \n
#         0: Straight Line Method \n
#         1: Declining Balance Method \n
#         2: Sum of the Years' Digits Method \n
#         3: Units of Production Method \n
#         :param method: The depreciation method.
#         :param periods: The number of periods (months) to depreciate.
#         :param decline: The factor used in the declining balance method (2.0 = 200%).
#         :param units_prod: How many units produced, if using method 3.
#         :return: The dollar value depreciated.
#         """
#         # The only time I can foresee this conditional being necessary is for the declining balance method,
#         # since it ignores salvage value in its calculation of depreciation while not depreciating below salvage value.
#         if self.depreciable_value.get_value() > 0:
#             match method:
#                 # Straight Line
#                 case 0:
#                     depr_amt: float = ((self.def_value - self.slvg_value) / self.life) * periods
#
#                     if self._validate_depreciation(depr_amt):
#                         self.last_depr.change_value(depr_amt)
#                     else:
#                         self.last_depr.change_value(self.depreciable_value.get_value())
#
#                     self._update_attribs(periods)
#
#                 # Declining Balance
#                 case 1:
#                     depr_amt: float = (((self.def_value - self.total_depr.get_value()) / self.life) * decline) * periods
#
#                     if self._validate_depreciation(depr_amt):
#                         self.last_depr.change_value(depr_amt)
#                     else:
#                         self.last_depr.change_value(self.depreciable_value.get_value())
#
#                     self._update_attribs(periods)
#
#                 # Sum of the Years' Digits
#                 case 2:
#                     depr_amt: float = (self.def_value - self.slvg_value) * ((self.rem_life / 12) / self.syd)
#
#                     if self._validate_depreciation(depr_amt):
#                         self.last_depr.change_value(depr_amt)
#                     else:
#                         self.last_depr.change_value(self.depreciable_value.get_value())
#
#                     self._update_attribs(periods)
#
#                 # Units of Production
#                 case 3:
#                     depr_amt: float = (self.depreciable_value.get_value() / self.prod_cap) * units_prod
#
#                     if self._validate_depreciation(depr_amt):
#                         self.last_depr.change_value(depr_amt)
#                     else:
#                         self.last_depr.change_value(self.depreciable_value.get_value())
#
#                     self._update_attribs(periods)
#
#         else:
#             if self.depreciable_value.get_value() < 0:
#                 self.depreciable_value.change_value(0)
#
#             print(f"Asset \"{self.name}\" is fully depreciated! Current value = {self.value}.")
#
#         return self.last_depr.get_value()
