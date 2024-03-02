from src.pyacty.financial_statements.BalanceSheet import BalanceSheet

bal_sht: BalanceSheet = BalanceSheet()

bal_sht.add_account("Cash", "asset", 1_000_000)
bal_sht.add_account("Accounts Receivable (net)", "asset", 500_000)

bal_sht.add_account("Accounts Payable", "liability", 5_000)
bal_sht.add_account("Bonds Payable", "liability", 500)

bal_sht.add_account("Retained Earnings", "equity", 765_000)

bal_sht.save_fs("C:\\Users\\jacob\\OneDrive\\Desktop\\output", "test", "csv")
bal_sht.save_fs("C:\\Users\\jacob\\OneDrive\\Desktop\\output", "test", "json")
