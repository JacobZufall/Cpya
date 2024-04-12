"""
BsTable.py
"""

from typing import override
from .FsTable import FsTable
from src.pyacty.financial_statements.BalanceSheet import BalanceSheet


class BsTable(FsTable):
    def __init__(self, company: str, financial_stmt: str, date: str,
                 pyacty_fs: None | BalanceSheet = None) -> None:
        super().__init__(company, financial_stmt, date, pyacty_fs)

    @override
    def __str__(self):
        super().__str__()

    @override
    def __repr__(self):
        super().__repr__()
