"""
Skeleton.py
"""

from typing import override, Any


class Skeleton:
    subclasses: list[str] = [
        "Divider",
        "Header"
    ]

    months: dict[str:str] = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    }

    def __init__(self, company: str, fs_name: str, date: str, fnstmt: dict[str:dict[str:dict[str:any]]],
                 min_width: int = 50, margin: int = 2, indent: int = 4) -> None:
        """

        :param company:
        :param fs_name:
        :param date:
        :param fnstmt:
        :param min_width:
        :param margin:
        :param indent:
        """
        self.company: str = company
        self.fs_name: str = fs_name
        self.f_date: str = self._format_date(date)
        self.fnstmt: dict[str:dict[str:dict[str:any]]] = fnstmt

        self.min_width: int = min_width
        self.margin: int = margin
        self.indent: int = indent
        self.calc_width: int = -1

        # In order to properly format the width, we need to know the longest string used, so we know how wide to make
        # the table.
        self.titles: list[str] = []
        self.implemented_elements: list[Any] = []

        if self.company is not None:
            self.add_title(self.company)

        if self.fs_name is not None:
            self.add_title(self.fs_name)

        if self.f_date is not None:
            self.add_title(self.f_date)

        if self.fnstmt is not None:
            for category, accounts in self.fnstmt.items():
                for account, attributes in accounts.items():
                    self.add_title(account)

        # self._find_subclasses()

    # @classmethod
    # def _find_subclasses(cls) -> None:
    #     """
    #     Finds all the classes that inherit from this class and appends them to a list.
    #     :return: Nothing.
    #     """
    #     for sub in cls.__subclasses__():
    #         cls.subclasses.append(sub.__name__)

    def _calc_width(self) -> None:
        """
        Calculates the width the output will be.
        :return: Nothing.
        """
        for title in self.titles:
            if len(title) > self.calc_width:
                self.calc_width = len(title)

            if self.calc_width < self.min_width:
                self.calc_width = self.min_width

    def _format_date(self, date: str) -> str:
        split_date: list[str] = date.split("/")
        return f"For year ended {self.months[split_date[0]]} {split_date[1]}, {split_date[2]}"

    def add_title(self, title: str) -> None:
        """
        Adds a title into a list that's used to calculate the width of the output. This method checks for redundancy
        and recalculates the width of the output automatically.
        :param title: The title to add/append.
        :return: Nothing.
        """
        if title not in self.titles:
            self.titles.append(title)

        self._calc_width()

    def implement(self, element: Any, key: str = ""):
        if type(element).__name__ not in self.subclasses:
            raise KeyError(f"{type(element).__name__} isn't a valid element.")

        self.implemented_elements.append(element)

    def print_output(self) -> None:
        for element in self.implemented_elements:
            print(element)
