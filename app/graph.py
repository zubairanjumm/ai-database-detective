from langgraph.graph import END, START, StateGraph

from app.analyzer import ResultAnalyzer
from app.database import Database
from app.investigator import Investigator
from app.models import InvestigationState
from app.sql_generator import SQLGenerator
from app.tools import DatabaseTools


def build_graph(database: Database):
    tools = DatabaseTools(database)
    generator = SQLGenerator()
    analyzer = ResultAnalyzer()

    investigator = Investigator(
        tools=tools,
        sql_generator=generator,
        analyzer=analyzer,
    )

    def investigate_node(
        state: InvestigationState,
    ) -> InvestigationState:
        result = investigator.investigate(
            state["question"]
        )

        return result

    graph = StateGraph(InvestigationState)

    graph.add_node(
        "investigate",
        investigate_node,
    )

    graph.add_edge(
        START,
        "investigate",
    )

    graph.add_edge(
        "investigate",
        END,
    )

    return graph.compile()