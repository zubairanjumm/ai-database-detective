from app.models import QueryResult


class ResultAnalyzer:
    def analyze(self, result: QueryResult) -> list[str]:
        findings = []

        if result.row_count == 0:
            findings.append(
                "The query returned no results."
            )
            return findings

        findings.append(
            f"The query returned {result.row_count} rows."
        )

        for row in result.rows:
            findings.append(
                f"Result: {row}"
            )

        return findings
    def needs_more_evidence(
    self,
    result: QueryResult,
    current_step: int,
    max_steps: int,
) -> bool:
        if current_step >= max_steps:
            return False

        if result.row_count == 0:
            return True

        return False