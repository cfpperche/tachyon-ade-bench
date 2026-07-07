import unittest

from cart import build_receipt
from pricing import LineItem, subtotal_cents, total_cents


class CheckoutDiscountTest(unittest.TestCase):
    def setUp(self):
        self.items = [
            LineItem("notebook", 1200, 2),
            LineItem("pen", 150, 4),
        ]

    def test_existing_subtotal_behavior_remains(self):
        self.assertEqual(subtotal_cents(self.items), 3000)
        self.assertEqual(total_cents(self.items), 3000)

    def test_save10_discount(self):
        self.assertEqual(total_cents(self.items, discount_code="SAVE10"), 2700)

    def test_vip20_discount_is_case_insensitive(self):
        self.assertEqual(total_cents(self.items, discount_code="vip20"), 2400)

    def test_unknown_and_blank_codes_do_not_discount(self):
        self.assertEqual(total_cents(self.items, discount_code="NOPE"), 3000)
        self.assertEqual(total_cents(self.items, discount_code=""), 3000)
        self.assertEqual(total_cents(self.items, discount_code=None), 3000)

    def test_receipt_includes_discount_fields(self):
        receipt = build_receipt(self.items, discount_code="SAVE10")
        self.assertEqual(receipt["subtotal_cents"], 3000)
        self.assertEqual(receipt["discount_cents"], 300)
        self.assertEqual(receipt["total_cents"], 2700)
        self.assertEqual(receipt["discount_code"], "SAVE10")


if __name__ == "__main__":
    unittest.main()

