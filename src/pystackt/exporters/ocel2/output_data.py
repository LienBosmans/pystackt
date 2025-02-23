import duckdb

def _copy_schema_to_sqlite(quack_db:str="./quack.duckdb",quack_schema:str="ocel2",sqlite_db:str="./ocel2.sqlite"):
    """Copies the tables inside `quack_schema` of DuckDB database `quack_db` into a (new) SQLite database `sqlit_db`.
    Note that tables in `sqlite_db` will be overwritten if they already exist, but tables will not be deleted.
    It is therefore recommended to always create a new SQLite database file."""

    attach_sql_sql = f"ATTACH '{sqlite_db}' as sqlite_db (TYPE sqlite);"
    get_tables_sql = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{quack_schema}'"

    with duckdb.connect(quack_db) as quack:
        quack.sql(attach_sql_sql)

        tables = quack.sql(get_tables_sql).df()
        tables = tables['table_name'].tolist()

        for table_name in tables:
            # copy_table_sql = f"COPY {quack_schema}.{table_name} TO sqlite_db (FORMAT sqlite, TABLE '{table_name}');"
            copy_table_sql = f"CREATE OR REPLACE TABLE sqlite_db.{table_name} AS SELECT * FROM {quack_schema}.{table_name};"
            quack.sql(copy_table_sql)

    return None
