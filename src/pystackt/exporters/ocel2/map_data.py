import duckdb

def _create_ocel2_table(table_name:str,table_columns:list[str],sql_query:str,quack_db:str="./quack.duckdb",schema_out:str="ocel2"):
    """Creates `table_name` in `schema_out` of the DuckDB database `quack_db` 
    with columns defined in `table_columns` using the `sql_query` to generate the data."""

    print(f"    creating OCEL 2.0 table '{table_name}'")

    sql_str = (
        f"CREATE OR REPLACE TABLE {schema_out}.{table_name} ({", ".join(table_columns)});"
        f"INSERT INTO {schema_out}.{table_name} {sql_query};"
    )

    with duckdb.connect(quack_db) as quack:
        quack.sql(sql_str)

    return None


def _ocel2_event(quack_db:str="./quack.duckdb",schema_in:str="main",schema_out:str="ocel2"):
    """Creates the OCEL 2.0 `event` table in `schema_out` using the tables in `schema_in` 
    of the DuckDB database `quack_db`."""

    # Prepare OCEL 2.0 table
    sql_query = """--sql
        select
            id as ocel_id,
            event_type_id as ocel_type
        from
            """ + schema_in + ".events"

    # Write OCEL 2.0 table
    _create_ocel2_table("event",['ocel_id VARCHAR','ocel_type VARCHAR'],sql_query,quack_db,schema_out)

    return None


def _ocel2_event_map_type(quack_db:str="./quack.duckdb",schema_in:str="main",schema_out:str="ocel2"):
    """Creates the OCEL 2.0 `event_map_type` table in `schema_out` using the tables in `schema_in` 
    of the DuckDB database `quack_db`."""

    # Prepare OCEL 2.0 table
    sql_query = """--sql
        select
            id as ocel_id,
            lower(replace(replace(description,' ','_'),'-','_')) as ocel_type_map
        from
            """ + schema_in + ".event_types"

    # Write OCEL 2.0 table
    _create_ocel2_table("event_map_type",['ocel_type VARCHAR','ocel_type_map VARCHAR'],sql_query,quack_db,schema_out)

    return None


def _ocel2_event_object(quack_db:str="./quack.duckdb",schema_in:str="main",schema_out:str="ocel2"):
    """Creates the OCEL 2.0 `event_object` table in `schema_out` using the tables in `schema_in` 
    of the DuckDB database `quack_db`."""

    # Prepare OCEL 2.0 table
    sql_query = """--sql
        select
            event_to_object.event_id as ocel_event_id,
            event_to_object.object_id as ocel_object_id,
            qualifiers.description as ocel_qualifier
        from
            """ + f"{schema_in}.event_to_object as event_to_object" + """--sql
            inner join """ + f"{schema_in}.relation_qualifiers as qualifiers" + """--sql
                on event_to_object.qualifier_id = qualifiers.id
    """

    # Write OCEL 2.0 table
    _create_ocel2_table("event_object",['ocel_event_id VARCHAR','ocel_object_id VARCHAR','ocel_qualifier VARCHAR'],sql_query,quack_db,schema_out)

    return None


def _ocel2_object_object(quack_db:str="./quack.duckdb",schema_in:str="main",schema_out:str="ocel2"):
    """Creates the OCEL 2.0 `object_object` table in `schema_out` using the tables in `schema_in` 
    of the DuckDB database `quack_db`. Only first object-to-object connections are used because 
    OCEL 2.0 does not support dynamic object-to-object relationships."""

    # Prepare OCEL 2.0 table
    sql_query = """--sql
        with first_object_to_object as (
            select
                source_object_id,
                target_object_id,
                qualifier_id
            from
                """ + f"{schema_in}.object_to_object as object_to_object" + """--sql
            group by
                source_object_id,
                target_object_id,
                qualifier_id
        )

        select
            first_object_to_object.source_object_id as ocel_source_id,
            first_object_to_object.target_object_id as ocel_target_id,
            qualifiers.description as ocel_qualifier
        from
            first_object_to_object
            inner join """ + f"{schema_in}.relation_qualifiers as qualifiers" + """--sql
                on first_object_to_object.qualifier_id = qualifiers.id
    """

    # Write OCEL 2.0 table
    _create_ocel2_table("object_object",['ocel_source_id VARCHAR','ocel_target_id VARCHAR','ocel_qualifier VARCHAR'],sql_query,quack_db,schema_out)

    return None


def _ocel2_object(quack_db:str="./quack.duckdb",schema_in:str="main",schema_out:str="ocel2"):
    """Creates the OCEL 2.0 `object` table in `schema_out` using the tables in `schema_in` 
    of the DuckDB database `quack_db`."""

    # Prepare OCEL 2.0 table
    sql_query = """--sql
        select
            id as ocel_id,
            object_type_id as ocel_type
        from
            """ + f"{schema_in}.objects"

    # Write OCEL 2.0 table
    _create_ocel2_table("object",['ocel_id VARCHAR','ocel_type VARCHAR'],sql_query,quack_db,schema_out)

    return None


def _ocel2_object_map_type(quack_db:str="./quack.duckdb",schema_in:str="main",schema_out:str="ocel2"):
    """Creates the OCEL 2.0 `object_map_type` table in `schema_out` using the tables in `schema_in` 
    of the DuckDB database `quack_db`."""

    # Prepare OCEL 2.0 table
    sql_query = """--sql
        select
            id as ocel_type,
            lower(replace(replace(description,' ','_'),'-','_')) as ocel_type_map
        from
            """ + f"{schema_in}.object_types"

    # Write OCEL 2.0 table
    _create_ocel2_table("object_map_type",['ocel_type VARCHAR','ocel_type_map VARCHAR'],sql_query,quack_db,schema_out)

    return None


def _get_map_types(quack_db:str="./quack.duckdb",schema_out:str="ocel2",is_event:bool=True):
    """Returns a list of all OCEL 2.0 event map types (if `is_event = True`) or object map types (if `is_event = False`)."""
    if is_event:
        sql_str = f"SELECT ocel_type_map FROM {schema_out}.event_map_type"
    else:
        sql_str = f"SELECT ocel_type_map FROM {schema_out}.object_map_type"

    with duckdb.connect(quack_db) as quack:
        map_types = quack.sql(sql_str).df()
        map_types = map_types['ocel_type_map'].tolist()

    return map_types


def _get_event_type_unpivoted(schema_in:str="main") -> str:
    """Returns a SQL string that fetches all the event type data, in unpivotted format."""

    sql_str = """--sql
        with unpivoted_table as (
            select
                events.id as ocel_id,
                events.timestamp as ocel_time,
                event_attributes.description as attribute_column_name,
                event_attribute_values.attribute_value as attribute_value,
                event_attributes.datatype as attribute_datatype,
                lower(replace(replace(event_types.description,' ','_'),'-','_')) as ocel_type_map
            from
                """ + f"{schema_in}.events as events" + """--sql
                left join """ + f"{schema_in}.event_attribute_values as event_attribute_values" + """--sql
                    on events.id = event_attribute_values.event_id
                left join """ + f"{schema_in}.event_attributes as event_attributes" + """--sql
                    on event_attributes.id = event_attribute_values.event_attribute_id
                inner join """ + f"{schema_in}.event_types as event_types" + """--sql
                    on events.event_type_id = event_types.id
        )

        select * from unpivoted_table    
    """

    return sql_str


def _get_object_type_unpivoted(schema_in:str="main") -> str:
    """Returns a SQL string that fetches all the object type data, in unpivotted format."""

    sql_str = """--sql
        with unpivoted_table as (
            select
                objects.id as ocel_id,
                case 
                    when object_attribute_values.timestamp is null then make_date(1970,1,1)::datetime -- default NULL date in ocel2
                    else object_attribute_values.timestamp
                end as ocel_time,
                object_attributes.description as attribute_column_name,
                object_attributes.description as ocel_changed_field,
                object_attribute_values.attribute_value as attribute_value,
                object_attributes.datatype as attribute_datatype,
                lower(replace(replace(object_types.description,' ','_'),'-','_')) as ocel_type_map
            from
                 """ + f"{schema_in}.objects as objects" + """--sql
                left join  """ + f"{schema_in}.object_attribute_values as object_attribute_values" + """--sql
                    on objects.id = object_attribute_values.object_id
                left join  """ + f"{schema_in}.object_attributes as object_attributes" + """--sql
                    on object_attributes.id = object_attribute_values.object_attribute_id
                inner join  """ + f"{schema_in}.object_types as object_types" + """--sql
                    on objects.object_type_id = object_types.id
        )

        select * from unpivoted_table  
    """

    return sql_str


def _get_attributes(ocel_type:str,is_event:bool,quack_db:str="./quack.duckdb",schema_in:str="main",schema_out:str="ocel2"):
    """Returns list of attribute columns."""

    if is_event:
        sql_get_unpivoted_data = _get_event_type_unpivoted(schema_in)
    else:
        sql_get_unpivoted_data = _get_object_type_unpivoted(schema_in)

    sql_str = """--sql
        select distinct 
            attribute_column_name,
            attribute_datatype
        from 
           unpivoted_data
        where 
            """ + f"ocel_type_map = '{ocel_type}'" + """--sql
            and attribute_column_name is not null 
            and attribute_datatype is not null
    """

    with duckdb.connect(quack_db) as quack:
        unpivoted_data = quack.sql(sql_get_unpivoted_data)
        attribute_columns = quack.sql(sql_str).df().values.tolist()

    return attribute_columns


def _ocel2_type_tables(is_event:bool,quack_db:str="./quack.duckdb",schema_in:str="main",schema_out:str="ocel2"):
    """Creates the OCEL 2.0 `event_<type>` tables (if `is_event = True`) or `object_<type>` tables (if `is_event = False`)
    in `schema_out` using the tables in `schema_in` of the DuckDB database `quack_db`."""

    map_types = _get_map_types(quack_db,schema_out,is_event)

    for ocel_type in map_types:
        if is_event:
            table_prefix = "event_"
            sql_get_unpivoted_data = _get_event_type_unpivoted(schema_in)
            table_columns = ['ocel_id VARCHAR','ocel_time TIMESTAMP']
        else:
            table_prefix = "object_"
            sql_get_unpivoted_data = _get_object_type_unpivoted(schema_in)
            table_columns = ['ocel_id VARCHAR','ocel_time TIMESTAMP','ocel_changed_field VARCHAR']

        table_name = table_prefix + ocel_type
        attribute_columns = _get_attributes(ocel_type,is_event,quack_db,schema_in,schema_out)

        cast_columns_str = ""
        for column_name,datatype in attribute_columns:
            table_columns.append(column_name + ' ' + datatype.upper())
            cast_columns_str = f"{cast_columns_str}\n       {column_name}::{datatype} as {column_name},"

        cast_columns_str = cast_columns_str[:-1] # remove last comma

        # Prepare OCEL 2.0 table
        sql_query = """--sql
            with unpivoted_table as (
                select 
                    * 
                from 
                    """ + f"({sql_get_unpivoted_data})" + """--sql
                where 
                    """ + f"ocel_type_map = '{ocel_type}'" + """--sql
            ),
            pivoted_table as (
                PIVOT unpivoted_table 
                on attribute_column_name
                using first(attribute_value)
                group by
                    """ + ("ocel_id, ocel_time," if is_event else "ocel_id, ocel_time, ocel_changed_field,") + """--sql
            ),
            cast_attribute_columns as (
                select 
                    """ + ("ocel_id, ocel_time," if is_event else "ocel_id, ocel_time, ocel_changed_field,") + """--sql
                    """ + cast_columns_str + """--sql
                from 
                    pivoted_table
            )

            select * from cast_attribute_columns
        """

        # Write OCEL 2.0 table
        _create_ocel2_table(table_name,table_columns,sql_query,quack_db,schema_out)


    return None
