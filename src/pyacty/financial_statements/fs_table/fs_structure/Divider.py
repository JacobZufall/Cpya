"""
Divider.py
"""

from typing import override

from Skeleton import Skeleton


class Divider:
    def __init__(self, skeleton_obj: Skeleton, border: bool = False) -> None:
        self.skel: Skeleton = skeleton_obj

        self.output: str = ""

        if border:
            self.output = f"+{"-" * (self.skel.calc_width + self.skel.margin)}+"
        else:
            self.output = f"|{"-" * (self.skel.calc_width + self.skel.margin)}|"

    @override
    def __str__(self) -> str:
        return self.output
