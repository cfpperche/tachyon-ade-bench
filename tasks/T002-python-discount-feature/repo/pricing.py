from dataclasses import dataclass


@dataclass(frozen=True)
class LineItem:
    sku: str
    unit_price_cents: int
    quantity: int


def subtotal_cents(items):
    return sum(item.unit_price_cents * item.quantity for item in items)


def total_cents(items):
    return subtotal_cents(items)

