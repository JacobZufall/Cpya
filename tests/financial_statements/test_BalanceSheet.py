"""
test_BalanceSheet.py
"""

from src.pyacty.financial_statements.BalanceSheet import BalanceSheet

bal_sheet: BalanceSheet = BalanceSheet()

# Assets
bal_sheet.add_account("Cash", "asset", 1_000_000.0)
bal_sheet.add_account("Accounts Receivable", "asset", 150_000.0)
bal_sheet.add_account("Inventory", "asset", 200_000.0)

bal_sheet.add_account("Property & Equipment", "asset", 750_000.0, "non-current")
bal_sheet.add_account("Goodwill", "asset", 100.0, "non-current")

# Liabilities
bal_sheet.add_account("Accounts Payable", "liability", 2_000_000.0)
bal_sheet.add_account("Accrued Expenses", "liability", 0.0)
bal_sheet.add_account("Unearned Revenue", "liability", 500_000.0)

bal_sheet.add_account("Long-term Debt", "liability", 100_000.0, "non-current")

# Equity
bal_sheet.add_account("Common Stock", "equity", 6_000_000.0)
bal_sheet.add_account("Treasury Stock", "equity", 100_000.0, contra=True)

# The balance sheet shouldn't balance right now because the numbers above were input randomly.
balances, reason = bal_sheet.check_bs()
assert not balances
assert reason == "Liabilities and equity exceeds assets by 6599900.0"

# Add a plug figure to make the balance sheet balance.
bal_sheet.add_account("Prepaid Expenses", "asset", 6_599_900.0)

balances, reason = bal_sheet.check_bs()
assert balances
assert reason == "Balance sheet is balanced, no reason applicable."

bal_sheet.save_fs("./output", "test_bs")
