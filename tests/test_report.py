from app.models import InvestigationState, QueryResult, SQLQuery
from app.report import ReportGenerator


def test_report_generator():
    state: InvestigationState = {
        "question": "What is the total revenue for each order status?",
        "schema": {},
        "queries": [
            SQLQuery(
                query=(
                    "SELECT status, SUM(amount) AS total_revenue "
                    "FROM orders GROUP BY status"
                ),
                purpose="Calculate total revenue grouped by order status.",
            ),
            SQLQuery(
                query=(
                    "SELECT status, COUNT(*) AS order_count, "
                    "SUM(amount) AS total_revenue, "
                    "AVG(amount) AS average_order_value "
                    "FROM orders GROUP BY status"
                ),
                purpose=(
                    "Investigate order count and average order value "
                    "for each status."
                ),
            ),
        ],
        "results": [
            QueryResult(
                query=(
                    "SELECT status, SUM(amount) AS total_revenue "
                    "FROM orders GROUP BY status"
                ),
                rows=[
                    {
                        "status": "completed",
                        "total_revenue": 3130.0,
                    }
                ],
                row_count=1,
            ),
            QueryResult(
                query=(
                    "SELECT status, COUNT(*) AS order_count, "
                    "SUM(amount) AS total_revenue, "
                    "AVG(amount) AS average_order_value "
                    "FROM orders GROUP BY status"
                ),
                rows=[
                    {
                        "status": "completed",
                        "order_count": 9,
                        "total_revenue": 3130.0,
                        "average_order_value": 347.77777777777777,
                    }
                ],
                row_count=1,
            ),
        ],
        "findings": [
            "The query returned 1 rows."
        ],
        "current_step": 2,
        "max_steps": 2,
        "needs_more_evidence": False,
        "final_report": None,
    }

    generator = ReportGenerator()

    report = generator.generate(state)

    assert "DATABASE INVESTIGATION REPORT" in report
    assert state["question"] in report
    assert "FINDINGS" in report
    assert "INTERPRETATION" in report
    assert "QUERIES EXECUTED" in report
    assert "RESULTS" in report
    assert "3130.0" in report
    assert (
        "Completed orders: 9 orders generating $3130.00 in revenue."
        in report
    )