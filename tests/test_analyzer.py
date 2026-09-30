from app.analyzer import ResultAnalyzer
from app.models import QueryResult


def test_analyzer_finds_results():
    result = QueryResult(
        query="SELECT status, SUM(amount) AS total_revenue FROM orders GROUP BY status",
        rows=[
            {"status": "cancelled", "total_revenue": 90.0},
            {"status": "completed", "total_revenue": 3130.0},
        ],
        row_count=2,
    )

    analyzer = ResultAnalyzer()

    findings = analyzer.analyze(result)

    assert len(findings) == 3
    assert "The query returned 2 rows." in findings
    assert "Result: {'status': 'cancelled', 'total_revenue': 90.0}" in findings
    assert "Result: {'status': 'completed', 'total_revenue': 3130.0}" in findings


def test_analyzer_handles_empty_results():
    result = QueryResult(
        query="SELECT * FROM orders WHERE amount > 100000",
        rows=[],
        row_count=0,
    )

    analyzer = ResultAnalyzer()

    findings = analyzer.analyze(result)

    assert findings == [
        "The query returned no results."
    ]