def add_numbers(text):
    total = 0
    for part in text.split(","):
        value = part.strip()
        if value:
            total += int(value)
    return total


def multiply_numbers(text):
    product = 0
    for part in text.split(","):
        value = part.strip()
        if value:
            product *= int(value)
    return product

