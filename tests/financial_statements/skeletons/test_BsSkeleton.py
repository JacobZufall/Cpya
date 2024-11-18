"""
test_BsSkeleton.py
"""

from src.pyacty.statements.skeletons.BsSkeleton import BsSkeleton


test_bs: dict[str:dict[str:dict[str:str | float]]] = {
    "Assets": {
        "Cash": {
            "d/c": "debit",
            "bal": 400.0,
            "term": "current"
        },

        "Accounts Receivable": {
            "d/c": "debit",
            "bal": 1_000.0,
            "term": "current"
        }
    },

    "Liabilities": {
        "Accounts Payable": {
            "d/c": "credit",
            "bal": 200.0,
            "term": "current"
        }
    },

    "Stockholders' Equity": {
        "Common Stock": {
            "d/c": "credit",
            "bal": 200
        },

        "Retained Earnings": {
            "d/c": "credit",
            "bal": 1_000
        }
    }
}

test_balance_sheet: BsSkeleton = BsSkeleton(test_bs, "Test Company", "Balance Sheet",
                                            "12/31/20XX", decimals=False)

test_balance_sheet.print_output()
