from langgraph.graph import END, START, StateGraph

from app.analyzer import ResultAnalyzer
from app.database import Database
from app.investigator import Investigator
from app.models import InvestigationState
from app.report import ReportGenerator
from app.sql_generator import SQLGenerator
from app.tools import DatabaseTools


def build_graph(database: Database):
    tools = DatabaseTools(database)
    generator = SQLGenerator()
    analyzer = ResultAnalyzer()
    reporter = ReportGenerator()

    investigator = Investigator(
        tools=tools,
        sql_generator=generator,
        analyzer=analyzer,
    )

    def investigate_node(
        state: InvestigationState,
    ) -> InvestigationState:
        return investigator.investigate(state)

    def should_continue(
        state: InvestigationState,
    ) -> str:
        if state["current_step"] < state["max_steps"]:
            return "investigate"

        return "report"

    def report_node(
        state: InvestigationState,
    ) -> InvestigationState:
        state["final_report"] = reporter.generate(state)

        return state

    graph = StateGraph(InvestigationState)

    graph.add_node(
        "investigate",
        investigate_node,
    )

    graph.add_node(
        "report",
        report_node,
    )

    graph.add_edge(
        START,
        "investigate",
    )

    graph.add_conditional_edges(
        "investigate",
        should_continue,
        {
            "investigate": "investigate",
            "report": "report",
        },
    )

    graph.add_edge(
        "report",
        END,
    )

    return graph.compile()