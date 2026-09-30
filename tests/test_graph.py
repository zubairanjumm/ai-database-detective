from app.database import Database
from app.graph import build_graph


def test_graph_generates_final_report():
    database = Database("sqlite:///samples/business.db")
    graph = build_graph(database)

    result = graph.invoke(
        {
            "question": "What is the total revenue for each order status?",
            "schema": {},
            "queries": [],
            "results": [],
            "findings": [],
            "current_step": 0,
            "max_steps": 2,
            "needs_more_evidence": False,
            "final_report": None,
        }
    )

    assert result["current_step"] == 2
    assert len(result["queries"]) == 2
    assert len(result["results"]) == 2
    assert result["final_report"] is not None
    assert "DATABASE INVESTIGATION REPORT" in result["final_report"]
    assert "QUERIES EXECUTED" in result["final_report"]
    assert "3130.0" in result["final_report"]