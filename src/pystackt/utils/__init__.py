import duckdb

def _clear_schema(quack_db:str,schema_name:str):
    """Creates a schema `schema_name`, drops and overwrites existing schema if exists."""
    if schema_name == "main":
        print('Cannot drop schema "main" because it is an internal system entry')
    else:
        print(f"Overwriting schema '{schema_name}'")

        sql_str = (
            f"CREATE SCHEMA IF NOT EXISTS {schema_name};"
            f"DROP SCHEMA {schema_name} CASCADE;"
            f"CREATE SCHEMA {schema_name};"
        )

        with duckdb.connect(quack_db) as quack:
            quack.sql(sql_str)

    return None
