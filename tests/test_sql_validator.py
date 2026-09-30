from app.sql_validator import SQLValidator


def test_valid_select():
    validator = SQLValidator()

    valid, message = validator.validate(
        "SELECT * FROM orders"
    )

    assert valid is True
    assert message == "Query is valid."


def test_reject_insert():
    validator = SQLValidator()

    valid, message = validator.validate(
        "INSERT INTO orders VALUES (1, 1, '2026-01-01', 100, 'completed')"
    )

    assert valid is False


def test_reject_delete():
    validator = SQLValidator()

    valid, message = validator.validate(
        "DELETE FROM orders"
    )

    assert valid is False


def test_reject_drop():
    validator = SQLValidator()

    valid, message = validator.validate(
        "DROP TABLE orders"
    )

    assert valid is False


def test_reject_empty_query():
    validator = SQLValidator()

    valid, message = validator.validate("")

    assert valid is False


def test_reject_non_select():
    validator = SQLValidator()

    valid, message = validator.validate(
        "UPDATE orders SET amount = 0"
    )

    assert valid is False