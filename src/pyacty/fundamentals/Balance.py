"""
Balance.py
"""

from ..constants import ALL_CATEGORIES


class Balance:
    # True is debit, False is credit. See find_default_balance method.
    classifications: dict[str:bool] = {
        "asset": True,
        "liability": False,
        "equity": False,
        "revenue": False,
        "expense": True
    }

    @staticmethod
    def find_default_balance(category: str, contra: bool = False) -> str:
        """
        Finds a certain account and finds its default balance.
        :param category: The category of the account (asset, liability, equity, revenue, and expense).
        :param contra: Is the account a contra-account?
        :return: The default balance, which is "debit" or "credit" depending on the category.
        """
        if category.lower() not in ALL_CATEGORIES:
            # I don't think this will ever be raised because other files check this first, but it's a good failsafe.
            raise ValueError("Invalid category type.")

        def_bal: str
        cat_value: bool = Balance.classifications[category] if not contra else not Balance.classifications[category]

        if cat_value:
            def_bal = "debit"

        else:
            def_bal = "credit"

        return def_bal

    @staticmethod
    def find_true_balance(account: dict[str:dict[str:str | int | float]]) -> float:
        """
        Returns the true value of an account depending on if its true balance is debit or credit.
        :param account: The account to find the true balance of.
        :return: The true balance of the account.
        """
        return account["bal"] if account["d/c"] == "debit" else account["bal"] * -1.0

