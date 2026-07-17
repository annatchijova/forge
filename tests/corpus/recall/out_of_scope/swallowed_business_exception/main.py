def apply_discount(order):
    try:
        order["discount"] = order["discount"] + 1
    except Exception:
        pass
    return order
