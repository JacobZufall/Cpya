"""
DefaultBalance.py
"""

from ..constants import ALL_CATEGORIES


class DefaultBalance:
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
        cat_value: bool = DefaultBalance.classifications[category] if not contra else not DefaultBalance.classifications[category]

        if cat_value:
            def_bal = "debit"

        else:
            def_bal = "credit"

        return def_bal
