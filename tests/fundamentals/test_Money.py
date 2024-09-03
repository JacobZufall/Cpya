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
    # This looks ridiculous, but it ensures that it rounds as an accountant would expect it to.
    bal_seven: Money = Money(10_000.554555555555555555)

    def test_add(self) -> None:
        self.assertEqual(self.bal_one + self.bal_two, 30_000.30)
        self.assertEqual(self.bal_five + self.bal_six, 110_001.11)

    def test_radd(self) -> None:
        self.assertEqual(self.bal_two + self.bal_one, 30_000.30)
        self.assertEqual(self.bal_six + self.bal_five, 110_001.11)

    def test_eq(self) -> None:
        self.assertTrue(self.bal_one == 10_000.10)
        self.assertTrue(self.bal_two == 20_000.20)
        self.assertTrue(self.bal_three == 30_000.30)
        self.assertTrue(self.bal_four == 40_000.40)
        self.assertTrue(self.bal_five == 50_000.51)
        self.assertTrue(self.bal_six == 60_000.61)
        self.assertTrue(self.bal_seven == 10_000.56)

    def test_float(self) -> None:
        self.assertIsInstance(float(self.bal_one), float)

    def test_floordiv(self) -> None:
        self.assertEqual(self.bal_one // 10, 1_000)
        self.assertEqual(self.bal_two // 10, 2_000)
        self.assertEqual(self.bal_three // 10, 3_000)
        self.assertEqual(self.bal_four // 10, 4_000)
        self.assertEqual(self.bal_five // 10, 5_000)
        self.assertEqual(self.bal_six // 10, 6_000)
        self.assertEqual(self.bal_seven // 10, 1_000)

    def test_rfloordiv(self) -> None:
        self.assertEqual(100_000 // self.bal_one, 9)
        self.assertEqual(100_000 // self.bal_two, 4)
        self.assertEqual(100_000 //self.bal_three, 3)
        self.assertEqual(100_000 //self.bal_four, 2)
        self.assertEqual(100_000 //self.bal_five, 1)
        self.assertEqual(100_000 //self.bal_six, 1)
        self.assertEqual(100_000 //self.bal_seven, 9)

    def test_ge(self) -> None:
        self.assertGreaterEqual(self.bal_two, self.bal_one)
        self.assertGreaterEqual(self.bal_one, 10_000.10)

    def test_gt(self) -> None:
        self.assertGreater(self.bal_two, self.bal_one)
        self.assertGreater(self.bal_one, 9_000)

    def test_int(self) -> None:
        self.assertIsInstance(int(self.bal_one), int)

    def test_le(self) -> None:
        self.assertLessEqual(self.bal_one, self.bal_two)
        self.assertLessEqual(20_000.20, self.bal_two)

    def test_lt(self) -> None:
        self.assertLess(self.bal_one, self.bal_two)
        self.assertLess(15_000, self.bal_two)

    def test_mod(self) -> None:
        self.assertEqual(self.bal_one % 10, 0.10)

    def test_mul(self) -> None:
        pass

    def test_rmul(self) -> None:
        pass

    def test_ne(self) -> None:
        pass

    def test_pow(self) -> None:
        pass

    def test_rpow(self) -> None:
        pass

    def test_sub(self) -> None:
        pass

    def test_rsub(self) -> None:
        pass

    def test_truediv(self) -> None:
        pass

    def test_rtruediv(self) -> None:
        pass

    def test_rounded_values(self) -> None:
        self.assertEqual(self.bal_one.rounded_value, 10_000.10)
        self.assertEqual(self.bal_two.rounded_value, 20_000.20)
        self.assertEqual(self.bal_three.rounded_value, 30_000.30)
        self.assertEqual(self.bal_four.rounded_value, 40_000.40)
        self.assertEqual(self.bal_five.rounded_value, 50_000.51)
        self.assertEqual(self.bal_six.rounded_value, 60_000.61)
        self.assertEqual(self.bal_seven.rounded_value, 10_000.56)

    def test_format(self) -> None:
        self.assertEqual(self.bal_one.num_format, ",.0f")
        self.assertEqual(self.bal_one.__str__(), "$10,000")
        self.assertEqual(self.bal_two.__str__(), "₱20,000")
        self.assertEqual(self.bal_three.__str__(), "£30,000")
        self.assertEqual(self.bal_four.__str__(), "€40,000")
        self.assertEqual(self.bal_five.__str__(), "₩50,001")
        self.assertEqual(self.bal_six.__str__(), "¥60,001")
        self.assertEqual(self.bal_seven.__str__(), "$10,001")

        Money.show_decimals = True

        self.assertEqual(self.bal_one.num_format, ",.2f")
        self.assertEqual(self.bal_one.__str__(), "$10,000.10")
        self.assertEqual(self.bal_two.__str__(), "₱20,000.20")
        self.assertEqual(self.bal_three.__str__(), "£30,000.30")
        self.assertEqual(self.bal_four.__str__(), "€40,000.40")
        self.assertEqual(self.bal_five.__str__(), "₩50,000.51")
        self.assertEqual(self.bal_six.__str__(), "¥60,000.61")
        self.assertEqual(self.bal_seven.__str__(), "$10,000.56")

if __name__ == "__main__":
    ut.main()