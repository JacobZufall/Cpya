"""
custom_exceptions.py
"""


class SupportError(Exception):
    def __init__(self, message):
        super().__init__(message)
