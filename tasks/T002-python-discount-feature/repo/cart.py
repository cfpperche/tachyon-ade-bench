from pricing import subtotal_cents, total_cents


def build_receipt(items):
    subtotal = subtotal_cents(items)
    total = total_cents(items)
    return {
        "subtotal_cents": subtotal,
        "total_cents": total,
    }

