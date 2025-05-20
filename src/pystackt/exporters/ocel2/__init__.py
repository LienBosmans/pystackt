from pystackt.utils import (
    _clear_schema
)

from pystackt.exporters.ocel2.map_data import (  # maps the data from Stack't relational schema to OCEL 2.0 relational schema
    _ocel2_event,
    _ocel2_event_map_type,
    _ocel2_event_object, 
    _ocel2_object_object, 
    _ocel2_object,
    _ocel2_object_map_type,
    _ocel2_type_tables
)

from pystackt.exporters.ocel2.output_data import ( # writes data from DuckDB to SQLite
    _copy_schema_to_sqlite
)


def export_to_ocel2(quack_db:str="./quack.duckdb",schema_in:str="main",schema_out:str="ocel2",sqlite_db:str="./ocel2.sqlite"):
    """Uses the DuckDB database `quack_db` to map OCED data stored using Stack't relational schema 
    (located in `schema_in` database schema), to OCED data using OCEL 2.0 format (will be stored in `schema_out` database schema).
    Afterwards, the tables in `schema_out` will be copied to a (new) SQLite database `sqlite_db`. 
    It is recommended to always create a new SQLite database instead of re-using an existing one."""

    # Below functions include print statements, no need to add more
    _clear_schema(quack_db,schema_out)
    _ocel2_event(quack_db,schema_in,schema_out)
    _ocel2_event_map_type(quack_db,schema_in,schema_out)
    _ocel2_event_object(quack_db,schema_in,schema_out)
    _ocel2_object_object(quack_db,schema_in,schema_out)
    _ocel2_object(quack_db,schema_in,schema_out)
    _ocel2_object_map_type(quack_db,schema_in,schema_out)
    _ocel2_type_tables(True,quack_db,schema_in,schema_out)
    _ocel2_type_tables(False,quack_db,schema_in,schema_out)


    print(f"Exporting '{schema_out}' from {quack_db} to {sqlite_db}...")
    _copy_schema_to_sqlite(quack_db,schema_out,sqlite_db)

    print("All done!")

    return None
