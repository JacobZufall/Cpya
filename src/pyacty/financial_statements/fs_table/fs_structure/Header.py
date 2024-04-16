"""
Header.py
"""

from typing import override

from Skeleton import Skeleton


class Header:
    def __init__(self, skeleton_obj: Skeleton, header_name: str) -> None:
        self.skel: Skeleton = skeleton_obj

        self.output: str = ""

        self.space_needed: int = (self.skel.calc_width + self.skel.margin - len(header_name))
        self.l_space_needed: int = 0
        self.r_space_needed: int = 0

        if self.space_needed % 2 != 0:
            self.l_space_needed = int((self.space_needed / 2) - 0.5)
            self.r_space_needed = int((self.space_needed / 2) + 0.5)

        else:
            self.l_space_needed = self.r_space_needed = self.space_needed // 2

        self.output = f"|{" " * self.l_space_needed}{header_name}{" " * self.r_space_needed}|"

    @override
    def __str__(self) -> str:
        return self.output
