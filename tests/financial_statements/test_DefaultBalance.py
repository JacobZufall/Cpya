"""
test_DefaultBalance.py

Generally, contra-accounts aren't shown on the balance sheet, except for accounts like Treasury Stock.
However, some people may wish to add more detail to their balance sheet, and display gross accounts receivable and
allowance for doubtful accounts, for example. Therefore, the option exists.
"""

from src.pyacty.fundamentals.Balance import Balance

# The names of these variables don't matter, they're just examples.
scenarios: dict[str:Balance] = {
    "cash": Balance("asset"),
    "accumulated_depr": Balance("asset", True),
    "acts_payable": Balance("liability"),
    "discount_notes_payable": Balance("liability", True),
    "common_stock": Balance("equity"),
    "treasury_stock": Balance("equity", True),
    "revenue": Balance("revenue"),
    "sales_discounts": Balance("revenue", True),
    "supplies_expense": Balance("expense"),
    # I cannot think of a real-world example of a contra-expense account.
    "contra_expense": Balance("expense", True)
}

for account, balance in scenarios.items():
    if balance.category == "asset" or balance.category == "expense":
        if not balance.contra:
            assert balance.def_bal == "debit"
        else:
            assert balance.def_bal == "credit"
    else:
        if not balance.contra:
            assert balance.def_bal == "credit"
        else:
            assert balance.def_bal == "debit"
