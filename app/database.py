from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine


class Database:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url)

    def get_engine(self) -> Engine:
        return self.engine

    def get_tables(self) -> list[str]:
        inspector = inspect(self.engine)
        return inspector.get_table_names()

    def get_columns(self, table_name: str) -> list[dict]:
        inspector = inspect(self.engine)

        return [
            {
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column["nullable"],
            }
            for column in inspector.get_columns(table_name)
        ]

    def execute_query(self, query: str) -> list[dict]:
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            return [dict(row._mapping) for row in result]

        