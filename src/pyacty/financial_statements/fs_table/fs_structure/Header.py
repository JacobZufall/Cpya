"""
Header.py
"""

from LineObject import LineObject


class Header(LineObject):
    def __init__(self, name: str, max_width: int, margin: int):
        super().__init__(name, max_width, margin)
        self.name: str = name
