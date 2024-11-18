from src.pyacty.statements.FinancialStatement import FinancialStatement

test_fs: FinancialStatement = FinancialStatement("Financial Statement", "PyActy", "12/31/2024")

test_fs.add_account("asset", "Cash", "debit", 500)

print(test_fs)
