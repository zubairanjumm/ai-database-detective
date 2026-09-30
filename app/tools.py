from app.database import Database
from app.models import QueryResult, SQLQuery


class DatabaseTools:
    def __init__(self, database: Database):
        self.database = database

    def inspect_schema(self) -> dict:
        tables = self.database.get_tables()

        return {
            table: self.database.get_columns(table)
            for table in tables
        }

    def execute_sql(self, sql_query: SQLQuery) -> QueryResult:
        rows = self.database.execute_query(sql_query.query)

        return QueryResult(
            query=sql_query.query,
            rows=rows,
            row_count=len(rows),
        )