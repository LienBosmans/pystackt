from pystackt.utils import (
    _clear_schema
)

from pystackt.exporters.promg.map_data import (
    _event_log,
    _object_type,
    _dataset_description,
    _semantic_header
)

from pystackt.exporters.promg.output_data import (
    _create_folder_structure,
    _copy_schema_to_csv
)


def export_to_promg(quack_db:str="./quack.duckdb",schema_in:str="main",schema_out:str="promg",parent_folder:str='./promg_export',dataset_name:str='stackt'):
    """Uses the DuckDB database `quack_db` to map OCED data stored using Stack't relational schema.
    Intermediate tables will be stored in `schema_out` database schema.
    Afterwards, data will be written to csv files in `parent_folder/data`, 
    dataset descriptions will be generated as json files in `parent_folder/json_files`,
    and the semantic header will be generated as json file in `parent_folder/json_files`."""

    #   Clear `schema_out` (already includes print statements)
    _clear_schema(quack_db,schema_out)
    
    #   Create dataset tables (already includes print statements)
    _event_log(quack_db, schema_in, schema_out)
    _object_type(quack_db, schema_in, schema_out)

    #   Export dataset tables to csv
    print(f"Creating folders in {parent_folder}")
    _create_folder_structure(dataset_name, parent_folder)
    print(f"Exporting datasets as csv files to {parent_folder}/{dataset_name}/data")
    _copy_schema_to_csv(quack_db=quack_db, quack_schema=schema_out, parent_folder=parent_folder, dataset_name=dataset_name)


    #   Create dataset descriptions & save as json
    print(f"Creating dataset descriptions and save as json file {parent_folder}/{dataset_name}/json_files/{dataset_name}_DS.json")
    _dataset_description(dataset_name=dataset_name,parent_folder=parent_folder,quack_db=quack_db,quack_schema=schema_out)

    #   Create semantic header & save as json
    print(f"Creating semantic header and save as json file {parent_folder}/{dataset_name}/json_files/{dataset_name}.json")
    _semantic_header(dataset_name=dataset_name,parent_folder=parent_folder,quack_db=quack_db,quack_schema=schema_out)


    # print("All done!")

    return None
