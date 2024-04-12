"""
BsTable.py
"""

from typing import override
from .FsTable import FsTable
from src.pyacty.financial_statements.BalanceSheet import BalanceSheet


class BsTable(FsTable):
    def __init__(self, company: str, fs_name: str, date: str,
                 pyacty_fs: None | BalanceSheet = None) -> None:
        super().__init__(company, fs_name, date, pyacty_fs)

    @override
    def __str__(self):
        super().__str__()

    @override
    def __repr__(self):
        super().__repr__()
