from app.database import Database


class SchemaInspector:
    def __init__(self, database: Database):
        self.database = database

    def inspect(self) -> dict:
        schema = {}

        for table in self.database.get_tables():
            schema[table] = self.database.get_columns(table)

        return schema

