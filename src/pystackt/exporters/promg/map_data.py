import duckdb

def _create_event_log_table(quack_db:str="./quack.duckdb",schema_in:str="main",schema_out:str="promg") -> None:
    """Creates intermediatary table ``, based on data from `main` schema, inside `promg` schema."""

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
                left join """ + f"{schema_in}..objects" + """--sql
                    on event_to_object.object_id = objects.id
                left join """ + f"{schema_in}..object_types" + """--sql
                    on objects.object_type_id = object_types.id
            order by 
                column_header
        ),
        activities_pivoted_objects as (
            pivot activities_unpivoted_objects
            on column_header
            -- using first(object_id)
            using first([cast(object_id as string),object_description,event_to_object_qualifier])
        ),
        activities_unpivoted_attributes as (
            select
                activities.*,
                event_attribute_values.attribute_value as event_attribute_value,
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