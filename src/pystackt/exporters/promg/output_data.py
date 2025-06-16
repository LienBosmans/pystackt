import os
import duckdb

def _create_folder_structure(parent_folder:str='./promg_export') -> None:
    """Creates `data` and `json_files` folders inside `parent_folder` to store the export files to PromG."""
    for folder in [f"{parent_folder}/data",f"{parent_folder}/json_files"]:
        try:
            os.mkdir(folder)
        except Exception as e:
            print(f"An error occured when attempting to create folder structure inside {parent_folder}: {e}")


def _copy_schema_to_csv(quack_db:str="./quack.duckdb",quack_schema:str="promg",parent_folder:str='./promg_export'):
    """Copies the tables inside `quack_schema` of DuckDB database `quack_db` into csv files in folder `parent_folder/data`."""

    get_tables_sql = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{quack_schema}'"

    with duckdb.connect(quack_db) as quack:
        tables = quack.sql(get_tables_sql).df()
        tables = tables['table_name'].tolist()

        for table_name in tables:
            copy_table_sql = f"COPY {quack_schema}.{table_name} TO '{parent_folder}/data/{table_name}.csv' (HEADER, DELIMITER ',');"
            quack.sql(copy_table_sql)
