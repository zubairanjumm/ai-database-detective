from typing import TypedDict

from pydantic import BaseModel, Field


class SQLQuery(BaseModel):
    query: str = Field(min_length=1)
    purpose: str = Field(min_length=1)


class QueryResult(BaseModel):
    query: str
    rows: list[dict]
    row_count: int


class InvestigationState(TypedDict):
    question: str
    schema: dict
    queries: list[SQLQuery]
    results: list[QueryResult]
    findings: list[str]
    current_step: int
    max_steps: int
    final_report: str | None