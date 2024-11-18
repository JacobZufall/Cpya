from src.pyacty.statements.FinancialStatement import FinancialStatement
from src.pyacty.fundamentals.Account import Account
from src.pyacty.fundamentals.Money import Money

test_fs: FinancialStatement = FinancialStatement("Financial Statement", "PyActy", "12/31/2024")

test_fs.add_account("asset", "Cash", "debit", 500)

test_money: Money = Money(500)
test_account: Account = Account("Cash", "Debit", test_money)

print(test_account.__repr__())
