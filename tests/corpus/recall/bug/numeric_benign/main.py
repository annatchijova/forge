from decimal import Decimal


def decide(score):
    return Decimal(score) > Decimal("0.75")
