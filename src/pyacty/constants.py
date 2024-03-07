"""
constants.py
"""

from typing import Final

# Balance types
CREDIT: Final[str] = "credit"
DEBIT: Final[str] = "debit"
BAL_TYPES: Final[list[str]] = [
    CREDIT,
    DEBIT,
]

# Balance sheet account categories
ASSET: Final[str] = "asset"
LIABILITY: Final[str] = "liability"
EQUITY: Final[str] = "equity"
BS_CATEGORIES: Final[list[str]] = [
    ASSET,
    LIABILITY,
    EQUITY,
]

# Income statement account categories
REVENUE: Final[str] = "revenue"
EXPENSE: Final[str] = "expense"
IS_CATEGORIES: Final[list[str]] = [
    REVENUE,
    EXPENSE
]

# Comprehensive list of all categories
ALL_CATEGORIES: Final[list[str]] = []

for category in BS_CATEGORIES or IS_CATEGORIES:
    ALL_CATEGORIES.append(category)

for category in IS_CATEGORIES:
    ALL_CATEGORIES.append(category)
