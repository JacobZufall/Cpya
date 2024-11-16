"""
test_DefaultBalance.py

Generally, contra-accounts aren't shown on the balance sheet, except for accounts like Treasury Stock.
However, some people may wish to add more detail to their balance sheet, and display gross accounts receivable and
allowance for doubtful accounts, for example. Therefore, the option exists.
"""

from src.pyacty.fundamentals.DefaultBalance import DefaultBalance

# The names of these variables don't matter, they're just examples.
scenarios: dict[str:DefaultBalance] = {
    "cash": DefaultBalance("asset"),
    "accumulated_depr": DefaultBalance("asset", True),
    "acts_payable": DefaultBalance("liability"),
    "discount_notes_payable": DefaultBalance("liability", True),
    "common_stock": DefaultBalance("equity"),
    "treasury_stock": DefaultBalance("equity", True),
    "revenue": DefaultBalance("revenue"),
    "sales_discounts": DefaultBalance("revenue", True),
    "supplies_expense": DefaultBalance("expense"),
    # I cannot think of a real-world example of a contra-expense account.
    "contra_expense": DefaultBalance("expense", True)
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
