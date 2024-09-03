"""
test_Money.py
"""

import unittest as ut

from src.pyacty.fundamentals.Money import Money


class TestMoney(ut.TestCase):
    bal_one: Money = Money(10_000.101)
    bal_two: Money = Money(20_000.202, "₱")
    bal_three: Money = Money(30_000.303, "£")
    bal_four: Money = Money(40_000.404, "€")
    bal_five: Money = Money(50_000.505, "₩")
    bal_six: Money = Money(60_000.606, "¥")
    bal_seven: Money = Money(10_000.554555555555555555)

    Money.show_decimals = True

    def test_rounded_values(self) -> None:
        self.assertEqual(self.bal_one.rounded_value, 10_000.10)
        self.assertEqual(self.bal_two.rounded_value, 20_000.20)
        self.assertEqual(self.bal_three.rounded_value, 30_000.30)
        self.assertEqual(self.bal_four.rounded_value, 40_000.40)
        self.assertEqual(self.bal_five.rounded_value, 50_000.51)
        self.assertEqual(self.bal_six.rounded_value, 60_000.61)
        self.assertEqual(self.bal_seven.rounded_value, 10_000.56)


if __name__ == "__main__":
    ut.main()