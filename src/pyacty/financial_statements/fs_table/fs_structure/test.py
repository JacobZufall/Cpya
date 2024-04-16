from src.pyacty.financial_statements.FinancialStatement import FinancialStatement
from Skeleton import Skeleton
from Divider import Divider
from Header import Header

testFs: FinancialStatement = FinancialStatement(company="Zufall Company", date="12/31/2024")

testFs.fs = {
    "asset": {
        "Cash": {
            "d/c": "debit",
            "bal": 0.0,
            "term": "current"
        }
    },

    "liability": {
        "Accounts Payable": {
            "d/c": "credit",
            "bal": 0.0,
            "term": "current"
        }
    },

    "equity": {
        "Common Stock": {
            "d/c": "credit",
            "bal": 0.0
        }
    }
}

testSkeleton: Skeleton = Skeleton("Zufall Company", "Financial Statement", "12/31/2024", testFs.fs)

testSkeleton.implement(Divider(testSkeleton, True), "top_border")
testSkeleton.implement(Header(testSkeleton, "Zufall Company"))
testSkeleton.print_output()
