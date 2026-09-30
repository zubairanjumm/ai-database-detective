import os

import pytest

from app.database import Database
from app.schema_inspector import SchemaInspector
from app.sql_generator import SQLGenerator


@pytest.mark.skipif(
    not os.getenv("GOOGLE_API_KEY"),
    reason="GOOGLE_API_KEY is not set",
)
def test_sql_generator():
    db = Database("sqlite:///samples/business.db")
    schema = SchemaInspector(db).inspect()

    generator = SQLGenerator()

    result = generator.generate(
        "What is the total revenue for each order status?",
        schema,
    )

    assert result.query
    assert result.purpose

    valid, message = db.validator.validate(result.query)

    assert valid, message

    rows = db.execute_query(result.query)

    assert len(rows) > 0