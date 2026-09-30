from app.models import InvestigationState


class ReportGenerator:
    def generate(self, state: InvestigationState) -> str:
        lines = [
            "DATABASE INVESTIGATION REPORT",
            "",
            f"Question: {state['question']}",
            "",
            "FINDINGS",
            "--------",
        ]

        if state["findings"]:
            for finding in state["findings"]:
                lines.append(f"- {finding}")
        else:
            lines.append("- No findings were generated.")

        lines.extend(
            [
                "",
                "INTERPRETATION",
                "--------------",
            ]
        )

        lines.extend(self._build_interpretation(state))

        lines.extend(
            [
                "",
                "QUERIES EXECUTED",
                "-----------------",
            ]
        )

        for index, query in enumerate(state["queries"], start=1):
            lines.append(f"{index}. {query.purpose}")
            lines.append(f"   SQL: {query.query}")

        lines.extend(
            [
                "",
                "RESULTS",
                "-------",
            ]
        )

        for index, result in enumerate(state["results"], start=1):
            lines.append(
                f"Query {index}: {result.row_count} rows returned"
            )

            for row in result.rows:
                lines.append(f"  {row}")

        lines.extend(
            [
                "",
                f"Investigation steps: {state['current_step']}",
            ]
        )

        return "\n".join(lines)

    def _build_interpretation(
        self,
        state: InvestigationState,
    ) -> list[str]:
        interpretations = []

        for result in state["results"]:
            for row in result.rows:
                if (
                    "status" in row
                    and "order_count" in row
                    and "total_revenue" in row
                ):
                    interpretations.append(
                        f"{row['status'].capitalize()} orders: "
                        f"{row['order_count']} orders generating "
                        f"${row['total_revenue']:.2f} in revenue."
                    )

        if not interpretations:
            interpretations.append(
                "The available evidence does not support "
                "a higher-level interpretation yet."
            )

        return interpretations