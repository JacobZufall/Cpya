"""
test_BalanceSheet.py
"""

from src.pyacty.statements.BalanceSheet import BalanceSheet

#
bal_sheet: BalanceSheet = BalanceSheet("PyActy", "12/31/2024")

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


def test_one() -> None:
    """
    Tests to make sure the balance sheet balances. It also makes sure the add_account() method works properly.
    :return:
    """

    # The balance sheet shouldn't balance right now because the numbers above were input randomly.
    balances, reason = bal_sheet.check_bs()
    assert not balances
    assert reason == "Liabilities and equity exceeds assets by 6599900.0"

    # Add a plug figure to make the balance sheet balance.
    bal_sheet.add_account("Prepaid Expenses", "asset", 6_599_900.0)

    balances, reason = bal_sheet.check_bs()
    assert balances
    assert reason == "Balance sheet is balanced, no reason applicable."


def test_two() -> None:
    """
    Saves the balance sheet, resets it, and loads it.
    :return: Nothing.
    """
    # save_fs() isn't directly tested. But, if the other assertions in this test pass, that means it worked.
    bal_sheet.save_fs("./output", "test_bs")

    bal_sheet.reset()
    assert bal_sheet.fs == {"asset": {}, "liability": {}, "equity": {}}

    bal_sheet.load_fs("./output/test_bs.json")
    assert bal_sheet.fs == {
        "asset": {
            "Cash": {
                "d/c": "debit",
                "bal": 1000000.0,
                "term": "current"
            },
            "Accounts Receivable": {
                "d/c": "debit",
                "bal": 150000.0,
                "term": "current"
            },
            "Inventory": {
                "d/c": "debit",
                "bal": 200000.0,
                "term": "current"
            },
            "Property & Equipment": {
                "d/c": "debit",
                "bal": 750000.0,
                "term": "non-current"
            },
            "Goodwill": {
                "d/c": "debit",
                "bal": 100.0,
                "term": "non-current"
            },
            "Prepaid Expenses": {
                "d/c": "debit",
                "bal": 6599900.0,
                "term": "current"
            }
        },
        "liability": {
            "Accounts Payable": {
                "d/c": "credit",
                "bal": 2000000.0,
                "term": "current"
            },
            "Accrued Expenses": {
                "d/c": "credit",
                "bal": 0.0,
                "term": "current"
            },
            "Unearned Revenue": {
                "d/c": "credit",
                "bal": 500000.0,
                "term": "current"
            },
            "Long-term Debt": {
                "d/c": "credit",
                "bal": 100000.0,
                "term": "non-current"
            }
        },
        "equity": {
            "Common Stock": {
                "d/c": "credit",
                "bal": 6000000.0
            },
            "Treasury Stock": {
                "d/c": "debit",
                "bal": 100000.0
            }
        }
    }


if __name__ == "__main__":
    print(bal_sheet)
    test_one()
    test_two()
