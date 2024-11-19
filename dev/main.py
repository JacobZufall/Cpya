from src.pyacty.statements.FinancialStatement import FinancialStatement

test_fs: FinancialStatement = FinancialStatement("Financial Statement", "PyActy", "12/31/2024")

test_fs.add_account("asset", "Cash", "debit", 500)
test_fs.add_account("asset", "Inventory", "debit", 6_000)
test_fs.add_account("liability", "Accounts Payable", "credit", 1_000)
test_fs.add_account("equity", "Common Stock", "credit", 5_500)

test_fs.save("C:\\Users\\jacob\\OneDrive\\Desktop", "Test Financial Statement", "json")
