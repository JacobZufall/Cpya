"""
Analytics.py
"""

from src.pyacty.financial_statements.BalanceSheet import BalanceSheet
from src.pyacty.financial_statements.IncomeStatement import IncomeStatement


class Analytics:
    def __init__(self, bal_sht: BalanceSheet, inc_stmt: IncomeStatement) -> None:
        """
        Automatically takes accounts from related financial statements to calculate analytics.
        :param bal_sht: The related balance sheet to calculate analytics based on.
        :param inc_stmt: The related income statement to calculate analytics based on.
        """
        self.bal_sht: BalanceSheet = bal_sht
        self.inc_stmt: IncomeStatement = inc_stmt

    # None of the names for the following functions are final, nor are any of the functions themselves final. These
    # are just some basic analytical functions that should be implemented. Some of these may end up being their own
    # class, depending on how much abstraction is deemed necessary.

    def ar_turnover(self):
        pass

    def asset_turnover(self):
        pass

    def basic_eps(self):
        pass

    def cash_conversion_cycle(self):
        pass

    def current_ratio(self):
        pass

    def days_in_inventory(self):
        pass

    def days_payable_outstanding(self):
        pass

    def days_sales_ar(self):
        pass

    def debt_to_equity(self):
        pass

    def dividend_payout(self):
        pass

    def equity_multiplier(self):
        pass

    def gross_margin(self):
        pass

    def inventory_turnover(self):
        pass

    def operating_cash_flow(self):
        pass

    def price_earnings(self):
        pass

    def profit_margin(self):
        pass

    def quick_ratio(self):
        pass

    def return_on_equity(self):
        pass

    def return_on_sales(self):
        pass

    def times_interest_earned(self):
        pass

    def total_debt_ratio(self):
        pass
