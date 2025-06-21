import duckdb
import polars as pl
import json

def _create_promg_table(table_name:str,sql_query:str,quack_db:str="./quack.duckdb",schema_out:str="promg"):
    """Creates `table_name` in `schema_out` of the DuckDB database `quack_db` 
    with columns defined in `table_columns` using the `sql_query` to generate the data."""

    print(f"    creating PromG dataset table '{table_name}'")

    sql_str = (
        f"CREATE OR REPLACE TABLE {schema_out}.{table_name} AS {sql_query};"
    )

    with duckdb.connect(quack_db) as quack:
        quack.sql(sql_str)

    return None


def _event_log(quack_db:str="./quack.duckdb",schema_in:str="main",schema_out:str="promg") -> None:
    """Creates dataset table `event_log`, based on data from `schema_in` schema, inside `schema_out` schema."""

    sql_query = """--sql
        with activities_unpivoted_objects as (
            select
                events.id as event_id,
                events.timestamp as timestamp,
                event_types.description as activity,
                events.description as activity_description,
                objects.id as object_id,
                objects.description as object_description,
                event_to_object.qualifier_value as event_to_object_qualifier,
                concat(
                    lower(replace(replace(object_types.description,' ','_'),'-','_')),'__',
                    cast(row_number() over (partition by events.id, object_types.description) as string)
                ) as column_header
            from 
                """ + f"{schema_in}.events" + """--sql 
                left join """ + f"{schema_in}.event_types" + """--sql
                    on events.event_type_id = event_types.id
                left join """ + f"{schema_in}.event_to_object" + """--sql
                    on events.id = event_to_object.event_id
                left join """ + f"{schema_in}.objects" + """--sql
                    on event_to_object.object_id = objects.id
                left join """ + f"{schema_in}.object_types" + """--sql
                    on objects.object_type_id = object_types.id
            order by 
                column_header
        ),
        activities_pivoted_objects as (
            pivot activities_unpivoted_objects
            on column_header
            using first(object_id)
        ),
        activities_unpivoted_attributes as (
            select
                activities.*,
                replace(replace(event_attribute_values.attribute_value, chr(10), ''), chr(13), '') as event_attribute_value,
                lower(replace(replace(event_attributes.description,' ','_'),'-','_')) as event_attribute_description
            from
                activities_pivoted_objects as activities
                left join """ + f"{schema_in}.event_attribute_values" + """--sql
                    on activities.event_id = event_attribute_values.event_id
                left join """ + f"{schema_in}.event_attributes" + """--sql
                    on event_attribute_values.event_attribute_id = event_attributes.id
        ),
        activities_pivoted_attributes as (
            pivot activities_unpivoted_attributes
            on event_attribute_description
            using first(event_attribute_value)
        )

        select * from activities_pivoted_attributes       
    """

    # Write table to `schema_out`
    _create_promg_table(
        table_name='event_log',
        sql_query=sql_query,
        quack_db=quack_db,
        schema_out=schema_out
    )


def _object_type(quack_db:str="./quack.duckdb",schema_in:str="main",schema_out:str="promg") -> None:
    """Creates dataset table fore each object_type, based on data from `schema_in` schema, inside `schema_out` schema."""

    with duckdb.connect(quack_db) as quack:
        sql_query = f"select description from {schema_in}.object_types"
        object_types = [item[0] for item in quack.sql(sql_query).fetchall()]

    for object_type in object_types:
        sql_query = """--sql
            with objects as (
                select 
                    objects.id as object_id,
                    objects.description as object_description
                from 
                    """ + f"{schema_in}.object_types" + """--sql 
                    left join """ + f"{schema_in}.objects" + """--sql
                        on (
                            """ + f"object_types.description = '{object_type}'" + """--sql
                            and object_types.id = objects.object_type_id
                        )
            ),
            first_values_unpivoted as (
                select 
                    objects.object_id,
                    objects.object_description,
                    object_attributes.description as object_attribute,
                    argmin(replace(replace(object_attribute_values.attribute_value, chr(10), ''), chr(13), ''),timestamp) as attribute_value
                from 
                    objects
                    left join """ + f"{schema_in}.object_attribute_values" + """--sql 
                        on objects.object_id = object_attribute_values.object_id
                    left join """ + f"{schema_in}.object_attributes" + """--sql
                        on object_attribute_values.object_attribute_id = object_attributes.id
                group by all
            ),
            object_attribute_values_pivoted as (
                pivot first_values_unpivoted
                on object_attribute
                using first(attribute_value)
            )

            select * from object_attribute_values_pivoted where object_id is not null
        """

        # Write table to `schema_out`
        _create_promg_table(
            table_name=f"object_{object_type}",
            sql_query=sql_query,
            quack_db=quack_db,
            schema_out=schema_out
        )


def _dataset_description_attributes(table:str,quack_db:str="./quack.duckdb",quack_schema:str="promg") -> list:
    """Returns list of dictionaries describing each column of `table`."""

    sql_query = f"DESCRIBE TABLE {quack_schema}.{table};"

    with duckdb.connect(quack_db) as quack:
        df_columns = quack.sql(sql_query).pl()

    attributes = []
    for row in df_columns.iter_rows(named=True):
        column_name = row["column_name"]
        column_type = row["column_type"]

        if column_type == "VARCHAR":
            column_type = "str"
        elif column_type == "INTEGER":
            column_type = "int"

        if table == 'event_log' and column_name in ("event_id","timestamp"):
            is_nullable = False
        elif column_name in ("object_id"):
            is_nullable = False
        else:
            is_nullable = True

        attribute = dict()
        attribute["name"] = column_name

        if column_type == "TIMESTAMP":
            attribute["column"] = [{"name": column_name, "dtype": "str"}]
            attribute["datetime_object"] = {"format": "y-M-d H:m:s"}
        else:
            attribute["column"] = [{"name": column_name, "dtype": column_type}] 

        attribute["optional"] = is_nullable

        attributes.append(attribute)

    return attributes


def _dataset_description(dataset_name:str='stackt',parent_folder:str='./promg_export',quack_db:str="./quack.duckdb",quack_schema:str="promg") -> None:
    """Creates json file for dataset descriptions."""

    get_tables_sql = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{quack_schema}'"
    with duckdb.connect(quack_db) as quack:
        tables = quack.sql(get_tables_sql).df()
        tables = tables['table_name'].tolist()

    DS_file_content = []

    for table in tables:
        table_DS = dict()
        table_DS["name"] = table
        table_DS["file_directory"] = "data\\"
        table_DS["file_name"] = f"{table}.csv"
        table_DS["labels"] = ["Record"]
        table_DS["add_log"] = False
        table_DS["add_event_index"] = False
        table_DS["attributes"] = _dataset_description_attributes(table,quack_db,quack_schema)

        DS_file_content.append(table_DS)

    with open(f"{parent_folder}/{dataset_name}/json_files/{dataset_name}_DS.json", "w") as f:
        json.dump(DS_file_content, f)


def _semantic_header_helper(dataset_name:str='stackt',parent_folder:str='./promg_export',quack_db:str="./quack.duckdb",quack_schema:str="promg") -> dict:
    """Returns list of records and list of nodes for semantic header."""

    records = []
    nodes = []

    get_tables_sql = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{quack_schema}'"
    with duckdb.connect(quack_db) as quack:
        tables = quack.sql(get_tables_sql).df()
        tables = tables['table_name'].tolist()

    for table in tables:
        sql_query = f"DESCRIBE TABLE {quack_schema}.{table};"
        with duckdb.connect(quack_db) as quack:
            df_columns = quack.sql(sql_query).pl()

        columns = pl.Series(df_columns.select('column_name')).to_list()
        if table == "event_log":
            records.append(f"(record:EventRecord {{ {",".join([x for x in columns if '__' not in x])} }})")
            for object_column in [x for x in columns if '__' in x]:
                object_type = object_column[:-3]
                number = object_column[-1]
                records.append(f"(record:{object_type}Record:{object_type}{number}Record: {{ {object_column} }})")

            node = dict()
            node["type"] = "Event"
            node["constructor"] = [{
                "prevalent_record": "(record:EventRecord)",
                "result": "(e:Event {timestamp:record.timestamp, activity:record.activity})"
            }]
            nodes.append(node)

            node = dict()
            node["type"] = "Activity"
            node["constructor"] = [{
                "prevalent_record": "(record:EventRecord)",
                "result": "(a:Activity {activity:record.activity})",
                "infer_observed": True
            }]
            nodes.append(node)
        else:
            object_type = table[7:]
            records.append(f"(record:{object_type}Record:{object_type}0Record {{ {",".join(columns)} }})")

            node = dict()
            node["type"] = "Activity"
            node["constructor"] = [{
                "prevalent_record": f"(record:{object_type}0Record",
                "result": f"(a:Entity:{object_type} {{ {",".join([f"{x}: record.{x}" for x in columns])} }})",
                "infer_corr_from_event_record": False
            }]
            nodes.append(node)


        
    return {"records":records, "nodes":nodes}

def _semantic_header(dataset_name:str='stackt',parent_folder:str='./promg_export',quack_db:str="./quack.duckdb",quack_schema:str="promg") -> None:
    """Creates semantic header"""

    SH = dict()

    helper_output = _semantic_header_helper(dataset_name,parent_folder,quack_db,quack_schema)

    SH["name"] = dataset_name
    SH["version"] = "1.0.0"
    SH["records"] = helper_output["records"]
    SH["nodes"] = helper_output["nodes"]
    SH["relations"] = [] #todo

    with open(f"{parent_folder}/{dataset_name}/json_files/{dataset_name}.json", "w") as f:
        json.dump(SH, f)
