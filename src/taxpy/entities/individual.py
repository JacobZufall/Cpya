"""
individual.py
"""

from entity import Entity
from src.taxpy.deductions.standard_deduction import StandardDeduction


class Individual(Entity, StandardDeduction):
    def __init__(self, year: int):
        """
        :param year: The relevant tax year.
        """
        super().__init__(year=year)
