"""
constants.py
"""

# Balance types
CREDIT: str = "credit"
DEBIT: str = "debit"
BAL_TYPES: list[str] = [
    CREDIT,
    DEBIT,
]

# Balance sheet account categories
ASSET: str = "asset"
LIABILITY: str = "liability"
EQUITY: str = "equity"
BS_CATEGORIES: list[str] = [
    ASSET,
    LIABILITY,
    EQUITY,
]

# Income statement account categories
REVENUE: str = "revenue"
EXPENSE: str = "expense"
IS_CATEGORIES: list[str] = [
    REVENUE,
    EXPENSE
]

# Comprehensive list of all categories
ALL_CATEGORIES: list[str] = []

for category in BS_CATEGORIES or IS_CATEGORIES:
    ALL_CATEGORIES.append(category)

for category in IS_CATEGORIES:
    ALL_CATEGORIES.append(category)
