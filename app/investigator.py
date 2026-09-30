from app.analyzer import ResultAnalyzer
from app.models import InvestigationState
from app.sql_generator import SQLGenerator
from app.tools import DatabaseTools


class Investigator:
    def __init__(
        self,
        tools: DatabaseTools,
        sql_generator: SQLGenerator,
        analyzer: ResultAnalyzer,
    ):
        self.tools = tools
        self.sql_generator = sql_generator
        self.analyzer = analyzer

    def investigate(
        self,
        state: InvestigationState,
    ) -> InvestigationState:
        if not state["schema"]:
            state["schema"] = self.tools.inspect_schema()

        query = self.sql_generator.generate(
            state["question"],
            state["schema"],
            state["results"]
        )

        result = self.tools.execute_sql(query)

        findings = self.analyzer.analyze(result)

        state["queries"].append(query)
        state["results"].append(result)
        state["findings"].extend(findings)

        state["current_step"] += 1

        state["needs_more_evidence"] = (
            self.analyzer.needs_more_evidence(
                result,
                state["current_step"],
                state["max_steps"],
            )
        )

        return state