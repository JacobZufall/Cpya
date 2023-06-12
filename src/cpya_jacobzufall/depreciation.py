"""
# depreciation.py
"""


class Depreciation:
    def __init__(self):
        pass

    @staticmethod
    def sl_depr(cost: float, salvage: float, life: float) -> float:
        """

        :param cost:
        :param salvage:
        :param life:
        :return: The amount of depreciation per month.
        """
        return (cost - salvage) / life

    @staticmethod
    def sum_of_years(cost: float, salvage: float, life: int) -> list[float]:
        """
        Sums up the years and distributes the majority of the depreciation to the earlier years.

        With a life of 3 years:
        Year 1: 3 / 6 == 50%
        Year 2: 2 / 6 == 33.3%
        Year 1: 1 / 6 == 16.7%

        :param cost:
        :param salvage:
        :param life:
        :return: The amount of depreciation per year.
        """
        dn: float = (life * (life + 1)) / 2
        percentages: list[float] = []
        depr_amt: float = cost - salvage
        depr: list[float] = []

        for i in range(life):
            percentages.append((life - i) / dn)

        for i, v in enumerate(percentages):
            depr.append(depr_amt * percentages[i])

        return depr
