"""
FsTable.py
"""

from typing import override, Any


class FsTable:
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

    def __init__(self, company: str, fs_name: str, date: str,
                 pyacty_fs: Any, min_width: int = 50) -> None:
        """

        :param company:
        :param fs_name:
        :param date:
        :param pyacty_fs:
        :param min_width: The minimum width of the financial statement.
        """
        self.company: str = company
        self.fs_name: str = fs_name
        self.date: str = date
        self.f_date: str = self.date_to_header(date)
        self.pyacty_fs: Any = pyacty_fs
        self.min_width: int = min_width

    @override
    def __str__(self):
        # I'm going to make this function do something (besides call itself) later when this class is more developed.
        super().__str__()

    @override
    def __repr__(self):
        return f"{self.__class__.__name__}: {self.__dict__}"

    def date_to_header(self, date: str) -> str:
        """
        Formats a date as "For year ended December 31st, 2024", or the applicable date.\n
        Dates should be in MM/DD/YYYY format.
        :param date:
        :return: The date formatted for a financial statement.
        """
        split_date: list[str] = date.split("/")
        return (f"For year ended {self.months[split_date[0]]} {split_date[1]}, "
                f"{split_date[2]}")

    def format_fs(self) -> str:
        """
        Prints the financial statement.
        :return: Nothing.
        """

        # In order to properly format the width, we need to know the longest string out of every title, so we know how
        # wide to make it.
        titles: list[str] = []

        if self.company is not None:
            titles.append(self.company)

        if self.fs_name is not None:
            titles.append(self.fs_name)

        if self.f_date is not None:
            titles.append(self.f_date)

        if self.pyacty_fs is not None:
            for category, accounts in self.pyacty_fs.fs.items():
                for account, attributes in accounts.items():
                    titles.append(account)

        # Find the longest string in the list.
        max_width: int = -1
        for i in titles:
            if len(i) > max_width:
                max_width = len(i)

        if max_width < self.min_width:
            max_width = self.min_width

        # How many blank spaces should be around the longest object (on each side)?
        margin: int = 2
        # How many blank spaces an account should be indented.
        indent: int = 4

        def divider(border: bool = False) -> str:
            """
            Prints a divider on the financial statement that covers the longest title and the margin.
            :param border: Is this divider the top or bottom border?
            :return: Nothing.
            """
            output: str

            if border:
                output = f"+{"-" * (max_width + margin)}+"
            else:
                output = f"|{"-" * (max_width + margin)}|"

            return output

        def header(header_name: str) -> str:
            space_needed: int = (max_width + margin - len(header_name))
            l_space_needed: int
            r_space_needed: int

            # This is to handle an odd amount of space, since we can't have half of a space.
            # In the case of an odd number, the right side will have one more space than the left.
            if space_needed % 2 != 0:
                l_space_needed = int((space_needed / 2) - 0.5)
                r_space_needed = int((space_needed / 2) + 0.5)

            else:
                l_space_needed = r_space_needed = space_needed // 2

            return f"|{" " * l_space_needed}{header_name}{" " * r_space_needed}|"

        def title(title_name: str) -> str:
            space_needed: int = max_width - len(title_name) + margin
            return f"|{title_name}{" " * space_needed}|"

        def account(account_name: str, show_decimals: bool = True) -> str:
            account_bal: float | int = 550.52
            space_needed: int = max_width - len(account_name) + margin - indent - len(str(account_bal))
            r_padding: int = 1

            return f"|{" " * indent}{account_name}{" " * (space_needed - r_padding)}{account_bal}{" " * r_padding}|"

        # TODO: This needs to be modular. This class shouldn't require interaction from anyone, and should format
        #   based on its corresponding class.
        formatted_fs: str = (
            f"{divider(True)}\n"
            f"{header(self.company)}\n"
            f"{divider(False)}\n"
            f"{header(self.fs_name)}\n"
            f"{divider(False)}\n"
            f"{header(self.f_date)}\n"
            f"{divider(False)}\n"
            f"{title("Assets")}\n"
            f"{account("Cash")}\n"
            f"{divider(True)}"
        )

        return formatted_fs
