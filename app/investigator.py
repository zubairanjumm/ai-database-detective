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

    def investigate(self, question: str) -> InvestigationState:
        schema = self.tools.inspect_schema()

        state: InvestigationState = {
            "question": question,
            "schema": schema,
            "queries": [],
            "results": [],
            "findings": [],
            "current_step": 0,
            "max_steps": 3,
            "final_report": None,
        }

        query = self.sql_generator.generate(
            question,
            schema,
        )

        result = self.tools.execute_sql(query)

        findings = self.analyzer.analyze(result)

        state["queries"].append(query)
        state["results"].append(result)
        state["findings"].extend(findings)
        state["current_step"] = 1

        return state