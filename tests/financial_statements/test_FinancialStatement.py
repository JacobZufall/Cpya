"""
test_FinancialStatement.py
"""

from src.pyacty.financial_statements.FinancialStatement import FinancialStatement

test_fs: FinancialStatement = FinancialStatement("Zufall Company", "12/31/2024")

test_fs.fs = {
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
            "bal": 200.0
        },

        "Retained Earnings": {
            "d/c": "credit",
            "bal": 1_000.0
        }
    }
}

print(test_fs)