import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parent / "business.db"


def create_database():
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.executescript(
        """
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT NOT NULL
        );

        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );

        INSERT INTO customers (name, country) VALUES
            ('Alice', 'USA'),
            ('Bob', 'UK'),
            ('Charlie', 'Pakistan'),
            ('David', 'USA'),
            ('Eva', 'Germany');

        INSERT INTO orders
            (customer_id, order_date, amount, status)
        VALUES
            (1, '2026-01-05', 500, 'completed'),
            (2, '2026-01-10', 300, 'completed'),
            (3, '2026-01-15', 450, 'completed'),
            (4, '2026-02-03', 700, 'completed'),
            (5, '2026-02-12', 250, 'completed'),
            (1, '2026-02-20', 600, 'completed'),
            (2, '2026-03-01', 100, 'completed'),
            (3, '2026-03-05', 120, 'completed'),
            (4, '2026-03-11', 90, 'cancelled'),
            (5, '2026-03-18', 110, 'completed');
        """
    )

    connection.commit()
    connection.close()

    print(f"Database created at {DATABASE_PATH}")


if __name__ == "__main__":
    create_database()