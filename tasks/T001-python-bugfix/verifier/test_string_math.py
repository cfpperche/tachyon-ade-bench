import unittest

from string_math import add_numbers, multiply_numbers


class StringMathTest(unittest.TestCase):
    def test_adds_comma_separated_numbers(self):
        self.assertEqual(add_numbers("2, 3, 4"), 9)

    def test_ignores_empty_parts_for_addition(self):
        self.assertEqual(add_numbers("2,, 3"), 5)

    def test_multiplies_comma_separated_numbers(self):
        self.assertEqual(multiply_numbers("2, 3, 4"), 24)

    def test_ignores_empty_parts_for_multiplication(self):
        self.assertEqual(multiply_numbers("2,, 3"), 6)


if __name__ == "__main__":
    unittest.main()

