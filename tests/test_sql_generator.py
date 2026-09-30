from app.sql_generator import SQLGenerator


def test_generate_revenue_by_status():
    generator = SQLGenerator()

    query = generator.generate(
        "What is the total revenue for each order status?",
        {},
        [],
    )

    assert "GROUP BY status" in query.query
    assert "SUM(amount)" in query.query


def test_generate_follow_up_revenue_query():
    generator = SQLGenerator()

    first_query = generator.generate(
        "What is the total revenue for each order status?",
        {},
        [],
    )

    query_result = {
        "query": first_query.query,
        "rows": [
            {
                "status": "cancelled",
                "total_revenue": 90.0,
            },
            {
                "status": "completed",
                "total_revenue": 3130.0,
            },
        ],
        "row_count": 2,
    }

    from app.models import QueryResult

    previous_result = QueryResult(**query_result)

    follow_up = generator.generate(
        "What is the total revenue for each order status?",
        {},
        [previous_result],
    )

    assert "COUNT(*)" in follow_up.query
    assert "AVG(amount)" in follow_up.query
    assert follow_up.query != first_query.query
    