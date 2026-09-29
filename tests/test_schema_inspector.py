from app.database import Database
from app.schema_inspector import SchemaInspector


def test_schema_inspection():
    db = Database("sqlite:///samples/business.db")
    inspector = SchemaInspector(db)

    schema = inspector.inspect()

    assert "customers" in schema
    assert "orders" in schema

    customer_columns = [column["name"] for column in schema["customers"]]
    order_columns = [column["name"] for column in schema["orders"]]

    assert "name" in customer_columns
    assert "country" in customer_columns

    assert "customer_id" in order_columns
    assert "amount" in order_columns
    assert "status" in order_columns