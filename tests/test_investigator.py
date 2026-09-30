from app.analyzer import ResultAnalyzer
from app.database import Database
from app.investigator import Investigator
from app.models import InvestigationState
from app.sql_generator import SQLGenerator
from app.tools import DatabaseTools


def test_investigator_runs_query():
    database = Database("sqlite:///samples/business.db")

    tools = DatabaseTools(database)
    generator = SQLGenerator()
    analyzer = ResultAnalyzer()

    investigator = Investigator(
        tools=tools,
        sql_generator=generator,
        analyzer=analyzer,
    )

    state: InvestigationState = {
        "question": "What is the total revenue for each order status?",
        "schema": {},
        "queries": [],
        "results": [],
        "findings": [],
        "current_step": 0,
        "max_steps": 3,
        "needs_more_evidence": False,
        "final_report": None,
    }

    result = investigator.investigate(state)

    assert result["question"] == (
        "What is the total revenue for each order status?"
    )

    assert len(result["queries"]) == 1
    assert len(result["results"]) == 1
    assert len(result["findings"]) > 0
    assert result["current_step"] == 1

    assert result["results"][0].row_count > 0
    assert result["needs_more_evidence"] is False