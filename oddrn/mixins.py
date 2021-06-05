from collections import OrderedDict


class DatabaseMixin:
    def get_database(self, database_name: str) -> str:
        data = OrderedDict({"databases": database_name})
        return self.get_oddrn(data)

    def get_table(self, database_name: str, table_name: str) -> str:
        data = OrderedDict({
            "databases": database_name,
            "tables": table_name
        })
        return self.get_oddrn(data)

    def get_column(self, database_name: str, table_name: str, column_name: str) -> str:
        data = OrderedDict({
            "databases": database_name,
            "tables": table_name,
            "columns": column_name
        })
        return self.get_oddrn(data)


class DatabaseSchemaMixin:
    def get_database(self, database_name: str) -> str:
        data = OrderedDict({"databases": database_name})
        return self.get_oddrn(data)

    def get_schema(self, database_name: str, schema_name: str) -> str:
        data = OrderedDict({
            "databases": database_name,
            "schemas": schema_name
        })
        return self.get_oddrn(data)

    def get_table(self, database_name: str, schema_name: str, table_name: str) -> str:
        data = OrderedDict({
            "databases": database_name,
            "schemas": schema_name,
            "tables": table_name
        })
        return self.get_oddrn(data)

    def get_column(self, database_name: str, schema_name: str, table_name: str, column_name: str) -> str:
        data = OrderedDict({
            "databases": database_name,
            "schemas": schema_name,
            "tables": table_name,
            "columns": column_name
        })
        return self.get_oddrn(data)


class OwnerMixin:
    def get_owner(self, owner_name: str) -> str:
        data = OrderedDict({"owners": owner_name})
        return self.get_oddrn(data)