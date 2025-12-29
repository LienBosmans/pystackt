from pystackt.utils.class_definitions import *
from pystackt.utils.duckdb_helpers import _clear_schema
import polars as pl
import duckdb
from datetime import datetime

def _extract_dataframe(table:dict) -> pl.DataFrame:
    """Converts a dictionary of objects into a table (as a dataframe)."""

    lst_records = []
    for key,record in table.items():
        lst_records.append(record.get_dict())

    df_records = pl.DataFrame(lst_records)

    return df_records

def _dataframe_to_persistent_duckdb(df_records:pl.DataFrame,table_name:str,duckdb_file_name,schema_name:str) -> None:
    """Stores a dataframe in a duckdb table (in defined duckdb_file database).
    Overwrites a table if it already exists."""

    # connect to DuckDB database
    con = duckdb.connect(duckdb_file_name)

    # drop table if it already exists
    con.sql('''--sql
    drop table if exists ''' + f"{schema_name}.{table_name}" + '''
    ''')

    # check if empty table needs to be generated
    if not df_records.is_empty():
        select_statement = _get_sql_statement(table_name,is_empty_table=False)
    else:
        select_statement = _get_sql_statement(table_name,is_empty_table=True)
    
    # write table to database
    con.sql('''--sql
    create table  ''' + f"{schema_name}.{table_name}" + ''' as       
        ''' + select_statement + '\n'
    )

    return None

def _get_sql_statement(table_name:str,is_empty_table:bool,df_name:str="df_records"):
    """Used to generate an empty table in case the dataframe is empty,
    or to cast all columns to the correct datatype."""

    if table_name == 'event_types':
        columns = [['id',  'INTEGER'],  ['description','VARCHAR']]
    elif table_name == 'events':
        columns = [['id','INTEGER'],  ['event_type_id', 'INTEGER'], ['timestamp','TIMESTAMP'], ['description','VARCHAR']]
    elif table_name == 'event_attributes':
        columns = [['id','INTEGER'],  ['event_type_id', 'INTEGER'], ['description','VARCHAR'], ['datatype','VARCHAR']]
    elif table_name == 'event_attribute_values':
        columns = [['id','INTEGER'],  ['event_id','INTEGER'], ['event_attribute_id','INTEGER'],['attribute_value','VARCHAR']]
    elif table_name == 'object_types':
        columns = [['id','INTEGER'],  ['description','VARCHAR']]
    elif table_name == 'objects':
        columns = [['id','INTEGER'],  ['object_type_id','INTEGER'], ['description','VARCHAR']]
    elif table_name == 'object_attributes':
        columns = [['id','INTEGER'],  ['object_type_id','INTEGER'], ['description','VARCHAR'], ['datatype','VARCHAR']]
    elif table_name == 'object_attribute_values':
        columns = [['id','INTEGER'],  ['object_id','INTEGER'], ['object_attribute_id','INTEGER'], ['timestamp','TIMESTAMP'], ['attribute_value','VARCHAR']]
    elif table_name == 'event_to_object':
        columns = [['id','INTEGER'],  ['event_id','INTEGER'], ['object_id','INTEGER'], ['qualifier_id','INTEGER'], ['qualifier_value','VARCHAR']]
    elif table_name == 'event_to_object_attribute_value':
        columns = [['id','INTEGER'],  ['event_id','INTEGER'], ['object_attribute_value_id','INTEGER'], ['qualifier_id','INTEGER'], ['qualifier_value','VARCHAR']]
    elif table_name == 'object_to_object':
        columns = [['id','INTEGER'],  ['source_object_id','INTEGER'], ['target_object_id','INTEGER'], ['qualifier_id','INTEGER'], ['timestamp','TIMESTAMP'], ['qualifier_value','VARCHAR']]
    elif table_name == 'relation_qualifiers':
        columns = [['id','INTEGER'],  ['description','VARCHAR'], ['datatype','VARCHAR']]
    
    if is_empty_table:
        select_statement = "select " + ",".join([f"null::{column[1]} as {column[0]}" for column in columns]) + " where 1!=1"
    else:
       select_statement = "select " + ",".join([f"{column[0]}::{column[1]} as {column[0]}" for column in columns]) + f" from {df_name}"

    return select_statement


def _store_result(object_types:dict,object_attributes:dict,objects:dict,object_attribute_values:dict,
                  event_types:dict,event_attributes:dict,events:dict,event_attribute_values:dict,
                  relation_qualifiers:dict,event_to_object:dict,object_to_object:dict,event_to_object_attribute_value:dict,
                  extracted_from_message:str="",quack_db:str="./quack.duckdb",schema:str="main") -> None:
    ## Store the result
    print(f"{datetime.now().strftime("%d-%m-%Y %H:%M")}    Saving object-centric event data {extracted_from_message}to DuckDB database file {quack_db}, schema {schema}.")
    tables_to_store = [['object_types',object_types],
                    ['object_attributes',object_attributes],
                    ['objects',objects],
                    ['object_attribute_values',object_attribute_values],
                    ['event_types',event_types],
                    ['events',events],
                    ['event_attributes',event_attributes],
                    ['event_attribute_values',event_attribute_values],
                    ['relation_qualifiers',relation_qualifiers],
                    ['event_to_object',event_to_object],
                    ['object_to_object',object_to_object],
                    ['event_to_object_attribute_value',event_to_object_attribute_value],
                    ]
    
    _clear_schema(quack_db,schema)

    for tbl in tables_to_store:
        _dataframe_to_persistent_duckdb(
            df_records=_extract_dataframe(tbl[1]),
            table_name=tbl[0],
            duckdb_file_name=quack_db,
            schema_name=schema
            )
        print(f"    Table {tbl[0]} ({len(tbl[1])} records) done.")
