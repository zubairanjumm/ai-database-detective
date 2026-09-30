from app.database import Database
import pytest

from app.database import Database

def test_get_tables():
    db = Database("sqlite:///samples/business.db")

    tables = db.get_tables()

    assert "customers" in tables
    assert "orders" in tables


def test_get_columns():
    db = Database("sqlite:///samples/business.db")

    columns = db.get_columns("orders")

    column_names = [column["name"] for column in columns]

    assert "customer_id" in column_names
    assert "order_date" in column_names
    assert "amount" in column_names
    assert "status" in column_names


def test_execute_query():
    db = Database("sqlite:///samples/business.db")

    result = db.execute_query(
        "SELECT status, SUM(amount) AS revenue "
        "FROM orders GROUP BY status"
    )

    assert len(result) == 2

    completed = next(
        row for row in result if row["status"] == "completed"
    )

    assert completed["revenue"] == 3130.0


def test_database_rejects_delete():
    db = Database("sqlite:///samples/business.db")

    with pytest.raises(ValueError):
        db.execute_query("DELETE FROM orders")


def test_database_rejects_drop():
    db = Database("sqlite:///samples/business.db")

    with pytest.raises(ValueError):
        db.execute_query("DROP TABLE orders")