from app.analyzer import ResultAnalyzer
from app.database import Database
from app.investigator import Investigator
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

    state = investigator.investigate(
        "What is the total revenue for each order status?"
    )

    assert state["question"] == (
        "What is the total revenue for each order status?"
    )

    assert len(state["queries"]) == 1
    assert len(state["results"]) == 1
    assert state["current_step"] == 1

    assert state["results"][0].row_count > 0