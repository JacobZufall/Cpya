# Straight line depreciation.
def sl_depr(cost: float, salvage: float, life: float) -> float:
    return (cost - salvage) / life


"""
Sums up the years and distributes the majority of the depreciation to the earlier years.

With a life of 3 years:
Year 1: 3 / 6 == 50%
Year 2: 2 / 6 == 33.3%
Year 1: 1 / 6 == 16.7%

"""
def sum_of_years(cost: float, salvage: float, life: int) -> list[float]:
    dn: float = (life * (life + 1)) / 2
    percentages: list[float] = []
    depr_amt: float = cost - salvage
    depr: list[float] = []

    for i in range(life):
        percentages.append((life - i) / dn)

    for i, v in enumerate(percentages):
        depr.append(depr_amt * percentages[i])

    return depr


if __name__ == "__main__":
    print(sum_of_years(1000, 500, 5))
