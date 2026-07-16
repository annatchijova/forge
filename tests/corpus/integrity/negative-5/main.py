import sqlite3
from fractions import Fraction


def init_db(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            price_cents INTEGER NOT NULL,
            discount_percent_bp INTEGER NOT NULL DEFAULT 0
        );
        """
    )


def line_total(product, quantity):
    discount = Fraction(product["discount_percent_bp"], 10000)
    unit = round(product["price_cents"] * (1 - discount))
    return unit * quantity
