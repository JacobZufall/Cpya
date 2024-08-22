"""
FsSkeleton.py
"""

from string import Template
from typing import Any, Final


class FsSkeleton:
    class _Element:
        # TODO: Work out how to implement dynamic spacers. I'm thinking that when the parent class calls its render
        #  function, each instance of _Element will compare their width to the highest width, and adjust their central
        #  spacer so that everything lines up.
        def __init__(self, template: Template, mappings: dict[str:str] = None) -> None:
            """
            A single line in the output of FsSkeleton. This class allows the dynamic updating of the width so that it
            can adapt when new elements are added.
            :param template: A string template.
            :param mappings: A dictionary of mappings that will be used, in {mapping: keyword} format.
            """
            if mappings is None:
                mappings = {}

            self.template: Template = template
            self.mappings: dict[str:str] = mappings

            self._string: str = ""

        # self.width needs to change whenever self._string does, so this allows us to calculate it when width is called.
        @property
        def width(self) -> int:
            """
            The current width of the fully rendered template, including spaces.
            :return: The length of the string.
            """
            self.render()
            return len(self._string)

        def render(self) -> str:
            """
            Renders the template into a finished string based on the given elements.
            :return: The finished line result.
            """
            self._string = self.template.safe_substitute(self.mappings)
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
                 min_width: int = 50, margin: int = 2, indent_size: int = 4, column_space: int = 20,
                 decimals: bool = True) -> None:
        self.fn_stmt: dict[str:dict[str:dict[str:Any]]] = fn_stmt
        self.company: str = company
        self.fs_name: str = fs_name
        self.f_date: str = self._format_date(date)

        self.min_width: int = min_width
        self.margin: int = margin
        self.indent_size: int = indent_size
        self.column_space: int = column_space
        self.decimals: bool = decimals

        # Should there be a class attribute for templates which is then passed into self.templates by value? That way
        # one can choose to add a template to all instances or just a single instance easily. I'm not sure if this is a
        # good practice or not, however.
        self.templates: dict[str:Template] = {
            "account": Template("| $indent$account_name$central_spacer$account_bal|"),
            "divider": Template("|$divider|"),
            "header": Template("|$left_spacer$header_name$right_spacer|"),
            "spacer": Template("|$spacer|"),
            "subtotal": Template("| $indent$subtotal_name$central_spacer$subtotal_bal |"),
            "title": Template("| $title$spacer|"),
            "total": Template("| Total $total_name$central_spacer$total_bal |")
        }
        self.elements: dict[str:FsSkeleton._Element] = {}

    def _calc_width(self) -> None:
        longest_str_len: int = 0

        for key, element in self.elements.items():
            longest_str_len = max(longest_str_len, element.width)

    def _format_date(self, date: str) -> str:
        """
        Converts a date from MM/DD/YYYY format to the conventional one found commonly on most financial statements.
        :param date: The date in "MM/DD/YYYY" format.
        :return: The formatted date.
        """
        split_date: list[str] = date.split("/")
        return f"For year ended {self.MONTHS[split_date[0]]} {split_date[1]}, {split_date[2]}"

    def render(self, print_output: bool = False) -> list[str]:
        output: list[str] = []

        for key, element in self.elements.items():
            output.append(element.render())

            if print_output:
                print(element.render())

        return output

    def add_element(self, template: Template | str, key: str, **kwargs) -> None:
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
        new_element: FsSkeleton._Element = self._Element(template)

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


if __name__ == "__main__":
    fs_skeleton: FsSkeleton = FsSkeleton({}, "company", "name", "12/31/2021")
    fs_skeleton.add_element(fs_skeleton.templates["account"], "test_account")
    print(fs_skeleton.elements["test_account"].width)
