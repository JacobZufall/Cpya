"""
DefaultBalance.py
"""


class DefaultBalance:
    def __init__(self, category: str, contra: bool = False):
        """
        :param category:
        :param contra:
        """
        self.def_bal: str | None = None

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

        self.find_account(category, contra)

    def find_account(self, category: str, contra: bool = False) -> None:
        """
        :param category:
        :param contra:
        :return:
        """
        if not contra:
            self.def_bal = self.__getattribute__(category)
        else:
            self.def_bal = self.__getattribute__(f"contra_{category}")
