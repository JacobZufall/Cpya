"""
DefaultBalance.py
"""


class DefaultBalance:
    def __init__(self, category: str, contra: bool = False):
        """
        Contains the default balance (debit or credit) for all accounts and finds the default balance of a specified
        account.
        :param category: The category of the account (asset, liability, equity, revenue, and expense).
        :param contra: Is the account a contra-account?
        """
        # Balance sheet accounts
        self.asset: str = "debit"
        self.contra_asset: str = "credit"
        self.liability: str = "credit"
        self.contra_liability: str = "debit"
        self.equity: str = "credit"
        self.contra_equity: str = "debit"

        # Income statement accounts
        self.revenue: str = "credit"
        self.contra_revenue: str = "debit"
        self.expense: str = "debit"
        self.contra_expense: str = "credit"

        self.def_bal: str = self.find_account(category, contra)

    def find_account(self, category: str, contra: bool = False) -> str:
        """
        Finds a certain account and finds its default balance.
        :param category: The category of the account (asset, liability, equity, revenue, and expense).
        :param contra: Is the account a contra-account?
        :return: The default balance, which is "debit" or "credit" depending on the category.
        """
        if not contra:
            return self.__getattribute__(category)
        else:
            return self.__getattribute__(f"contra_{category}")
