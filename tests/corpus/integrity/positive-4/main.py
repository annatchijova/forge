import sqlite3


def init_db(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            price_cents INTEGER NOT NULL,
            discount_percent REAL NOT NULL DEFAULT 0
        );
        """
    )


def line_total(product, quantity):
    unit = round(product["price_cents"] * (1 - product["discount_percent"] / 100))
    return unit * quantity
