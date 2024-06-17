"""
TrueBalance.py
"""


class TrueBalance:
    def __init__(self, account: dict[str:dict[str:str | int | float]]) -> None:
        self.account: str = account
        self.true_balance: int | float = account["bal"] if account["d/c"] == "debit" else account["bal"] * -1.0
