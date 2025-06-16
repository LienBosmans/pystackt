from pystackt.utils import (
    _clear_schema
)

def export_to_promg(quack_db:str="./quack.duckdb",schema_in:str="main",schema_out:str="promg",parent_folder:str='./promg_export'):
    """Uses the DuckDB database `quack_db` to map OCED data stored using Stack't relational schema.
    Intermediate tables will be stored in `schema_out` database schema.
    Afterwards, data will be written to csv files in `parent_folder/data`, 
    dataset descriptions will be generated as json files in `parent_folder/json_files`,
    and the semantic header will be generated as json file in `parent_folder/json_files`."""

    # Below functions include print statements, no need to add more
    _clear_schema(quack_db,schema_out)


    # print(f"Exporting '{schema_out}' from {quack_db} to {parent_folder}...")

    # print("All done!")

    return None


export_to_promg(
    quack_db='./pandas_small.duckdb',
    schema_in='stackt'
)
