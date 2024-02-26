"""
Individual.py
"""

from Entity import Entity
from src.pyacty.deductions.StandardDeduction import StandardDeduction


class Individual(Entity, StandardDeduction):
    def __init__(self, year: int):
        """
        :param year: The relevant tax year.
        """
        super().__init__(year=year)
