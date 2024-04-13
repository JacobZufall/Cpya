"""
LineObject.py
"""


class LineObject:
    def __init__(self, name: str, max_width: int, margin: int):
        self.name: str = name
        self.max_width: int = max_width
        self.margin: int = margin
