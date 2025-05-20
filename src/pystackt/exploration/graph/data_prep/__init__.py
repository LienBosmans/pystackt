from pystackt.utils import (
    _clear_schema,
    _create_table
)

from pystackt.exploration.graph.data_prep.sql_statements import _graph_base_table


def prepare_graph_data(quack_db:str="./quack.duckdb",schema_in:str="main",schema_out:str="graph_data_prep"):
    _clear_schema(quack_db=quack_db,schema_name=schema_out)

    tables_to_generate = [
        ["graph_base_table", _graph_base_table(schema_in,schema_out)],
    ]

    for table_name,sql_str in tables_to_generate:
        _create_table(
            quack_db=quack_db,
            schema_name=schema_out,
            table_name=table_name,
            select_statement=sql_str
        )

    print(f"All done! The OCED in schema {schema_in} was transformed into a graph-compatible base table located in {schema_out} of your DuckDB database file {quack_db}.")

    return None
  