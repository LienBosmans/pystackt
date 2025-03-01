from pystackt.utils import (
    _clear_schema,
    _create_view
)

from pystackt.exploration.sql_statements import ( # used to generate views
    _event_stats,
    _object_stats
)

def create_statistics_views(quack_db:str="./quack.duckdb",schema_in:str="main",schema_out:str="statistics"):
    _clear_schema(quack_db=quack_db,schema_name=schema_out)

    views_to_generate = [
        ["event_stats",_event_stats(schema_in)],
        ["object_stats",_object_stats(schema_in)]
    ]

    for view_name,sql_str in views_to_generate:
        _create_view(
            quack_db=quack_db,
            schema_name=schema_out,
            view_name=view_name,
            select_statement=sql_str
        )

    print(f"All done! You can explore the statistics on you OCED using the views located in schema {schema_out} of your DuckDB database file {quack_db}.")

    return None
