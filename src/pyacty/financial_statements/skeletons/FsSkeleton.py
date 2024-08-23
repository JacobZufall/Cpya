"""
FsSkeleton.py
"""

from string import Template
from typing import Any, Final

DEFAULT_INDENT_SIZE: Final[int] = 4


class FsSkeleton:
    class _Element:
        auto_mappings: list[str] = ["divider", "indent", "spacer", "left_spacer", "central_spacer", "right_spacer"]

        def __init__(self, template: Template, indent_level: int, indent_size: int, edge: bool,
                     mappings: dict[str:str] = None) -> None:
            """
            A single line in the output of FsSkeleton. This class allows the dynamic updating of the width so that it
            can adapt when new elements are added.
            :param template: A string template.
            :param mappings: A dictionary of mappings that will be used, in {mapping: keyword} format.
            """
            self.template: Template = template

            if mappings is None:
                mappings = {}

            self.mappings: dict[str:str] = mappings

            # Spacers shouldn't be manually controlled by the user, so this gets rid of any they may have inserted into
            # mappings.
            for key, mapping in self.mappings.items():
                if key in self.auto_mappings:
                    self.mappings.pop(key)

            self.indent_level: int = indent_level
            self.indent_size: int = indent_size
            self.edge: bool = edge

            self._string: str = ""

        @property
        def total_indent(self) -> int:
            result: int = 0

            if self.indent_level > 0:
                result = (self.indent_level * self.indent_size) - 1

            return result

        # self.width needs to change whenever self._string does, so this allows us to calculate it when width is called.
        @property
        def width(self) -> int:
            """
            The smallest width an element can be.
            :return: The length of the string.
            """
            return len(self.template.substitute(
                self.mappings,
                end = "",
                divider = "",
                indent = " " * self.total_indent,
                spacer = "",
                left_spacer = "",
                central_spacer = "",
                right_spacer = ""
            ))

        def render(self, min_width: int) -> str:
            """
            Renders the template into a finished string based on the given elements.
            :param min_width: The minimum width of the template to render.
            :return: The finished line result.
            """
            width_diff: int = max(min_width - self.width, 0)

            # Some elements are centered, so we need the space on either side to be equal while still being the proper
            # width. In the case where the resulting space needed is an odd number, it'll put more space on the right
            # side than the left, which tends to look better.
            if width_diff % 2 == 0:
                left_space: int = width_diff // 2
                right_space: int = left_space

            else:
                left_space: int = int(width_diff / 2 - 0.5)
                right_space: int = int(width_diff / 2 + 0.5)

            div_end_char = "+" if self.edge else "|"

            # Subtracting 2 from min_width accounts for the border.
            self._string = self.template.substitute(
                self.mappings,
                end = div_end_char,
                divider = "-" * (min_width - 2),
                indent = " " * self.total_indent,
                spacer = " " * width_diff,
                left_spacer = " " * left_space,
                central_spacer = "·" * width_diff,
                right_spacer = " " * right_space
            )

            return self._string

    # Not sure if this should be final or not.
    MONTHS: Final[dict[str:str]] = {
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

    def __init__(self, fn_stmt: dict[str:dict[str:dict[str:Any]]], company: str, fs_name: str, date: str,
                 min_width: int = 75, margin: int = 2, indent_size: int = DEFAULT_INDENT_SIZE, column_space: int = 20,
                 decimals: bool = True) -> None:
        self.fn_stmt: dict[str:dict[str:dict[str:Any]]] = fn_stmt
        self.company: str = company
        self.fs_name: str = fs_name
        self.f_date: str = self._format_date(date)

        self._min_width: int = min_width
        self.margin: int = margin
        self.indent_size: int = indent_size
        self.column_space: int = column_space
        self.decimals: str = ",.2f" if decimals else ",.0f"

        # Should there be a class attribute for templates which is then passed into self.templates by value? That way
        # one can choose to add a template to all instances or just a single instance easily. I'm not sure if this is a
        # good practice or not, however.
        self.templates: dict[str:Template] = {
            "account": Template("| $indent$account_name$central_spacer$account_bal |"),
            "divider": Template("$end$divider$end"),
            "header": Template("|$left_spacer$header_name$right_spacer|"),
            "spacer": Template("|$spacer|"),
            "subtotal": Template("| $indent$subtotal_name$central_spacer$subtotal_bal |"),
            "title": Template("| $title$spacer|"),
            "total": Template("| Total $total_name$spacer$total_bal |")
        }
        self.elements: dict[str:FsSkeleton._Element] = {}

    @property
    def min_width(self) -> int:
        longest_str_len: int = 0

        for key, element in self.elements.items():
            longest_str_len = max(longest_str_len, element.width)

        return longest_str_len

    @min_width.setter
    def min_width(self, width: int) -> None:
        """
        Used to manually set the width. You cannot use this setter to change self._min_width to less than what the
        getter calculates as the minimum width, because it'll be overridden. This is used when you want the output to
        be even wider.
        :param width: The minimum width of the output.
        :return: Nothing.
        """
        self._min_width = width

    def _format_date(self, date: str) -> str:
        """
        Converts a date from MM/DD/YYYY format to the conventional one found commonly on most financial statements.
        :param date: The date in "MM/DD/YYYY" format.
        :return: The formatted date.
        """
        split_date: list[str] = date.split("/")
        return f"For year ended {self.MONTHS[split_date[0]]} {split_date[1]}, {split_date[2]}"

    def render(self, print_output: bool = False) -> str:
        """
        Renders all added elements.
        :param print_output: If the output should display in console.
        :return: A list of strings of each element.
        """
        output: str = ""

        for key, element in self.elements.items():
            output += element.render(self._min_width)

            if print_output:
                print(element.render(self._min_width))

        return output

    def auto_render(self, print_output: bool = False) -> str:
        """
        Unlike the render() method, this generates an output automatically based on self.fn_stmt.
        :param print_output: If the output should display in console.
        :return: A list of strings of each element.
        """
        output: str = ""
        # Temporarily stores elements that have been manually added so that they can be restored at the end of the
        # method.
        auto_elements: dict[str:FsSkeleton._Element] = self.elements

        # Header Elements
        self.add_element(self.templates["divider"], "div_top", edge = True)
        self.add_element(self.templates["header"], "header_company", header_name = self.company)
        self.add_element(self.templates["divider"], "div_1")
        self.add_element(self.templates["header"], "header_fs_name", header_name = self.fs_name)
        self.add_element(self.templates["divider"], "div_2")
        self.add_element(self.templates["header"], "header_date", header_name = self.f_date)
        self.add_element(self.templates["divider"], "div_3")

        num_of_divs: int = 3
        # Body Elements
        print(self.decimals)
        for category, accounts in self.fn_stmt.items():
            self.add_element(self.templates["title"], f"title_{category.lower()}",
                             title = category.lower().capitalize())

            total_bal: float | int = 0.0

            for account, attributes in accounts.items():
                if attributes["d/c"] == "debit":
                    total_bal += attributes["bal"]

                else:
                    total_bal -= attributes["bal"]

                self.add_element(self.templates["account"], f"account_{account.lower()}",
                                 account_name = account, account_bal = f"{attributes["bal"]:{self.decimals}}",
                                 indent_level = 1)

            self.add_element(self.templates["total"], f"total_{category.lower()}",
                             total_name = category.lower().capitalize(),
                             total_bal = f"{abs(total_bal):{self.decimals}}")
            num_of_divs += 1
            self.add_element(self.templates["divider"], f"div_{num_of_divs}")


        else:
            self.del_element(f"div_{num_of_divs}")
            self.add_element(self.templates["divider"], "div_bottom", edge = True)


        for key, element in auto_elements.items():
            output += element.render(self._min_width) + "\n"

            if print_output:
                print(element.render(self._min_width))

        self.elements = auto_elements
        return output

    def add_element(self, template: Template | str, key: str, indent_level: int = 0,
                    indent_size: int = DEFAULT_INDENT_SIZE, edge: bool = False, **kwargs) -> None:
        if type(template) is str:
            template = Template(template)

        # Checks if the template exists.
        if template not in self.templates.values():
            raise KeyError

        # Keys need to be unique so that we can delete them later, if needed. This checks to make sure that an element
        # with said key doesn't already exist.
        if key in self.elements:
            raise ValueError

        # By storing the template used and the elements to substitute, we can perform the substitution later after all
        # elements are added. This allows us to dynamically update the width of the output as new elements are added.
        new_element: FsSkeleton._Element = self._Element(template, indent_level, indent_size, edge)

        for mapping, keyword in kwargs.items():
            new_element.mappings[mapping] = keyword

        self.elements[key] = new_element

    def del_element(self, key: str) -> None:
        """
        Deletes the specified element from the statement.
        :param key: The key of the element to delete.
        :return: Nothing.
        """
        if key not in self.elements:
            raise KeyError

        self.elements.pop(key)

    def add_template(self, template_name: str, template: Template | str) -> None:
        """
        Adds a template to the statement.
        :param template_name: The name of the template.
        :param template: The actual Template object or a string.
        :return: Nothing.
        """
        # I figured this would be good to add in case someone doesn't want to import Template from string in a separate
        # file.
        if type(template) is str:
            template = Template(template)

        for name, _ in self.templates.items():
            if name == template_name:
                raise ValueError

        self.templates[template_name] = template

    def del_template(self, template_name: str) -> None:
        """
        Attempts to delete a template and throws a KeyError if it fails to do so.
        :param template_name: The name of the template to be deleted.
        :return: Nothing.
        """
        if template_name not in self.templates:
            raise KeyError

        self.templates.pop(template_name)
