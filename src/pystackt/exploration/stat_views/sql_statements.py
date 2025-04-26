def _event_stats(schema_in:str):
    """Returns sql statement giving statistics on events."""

    sql_statement = """--sql
        with overview as (
            select
                event_types.id as event_type_id,
                event_types.description as event_type_description,
                min(events.timestamp) as first_event_timestamp,
                max(events.timestamp) as last_event_timestamp,
                count(distinct events.id) as event_count,
                count(distinct event_attributes.id) as event_attribute_count,
                count(distinct event_attribute_values.id) as event_attribute_value_update_count
            from
                """ + f"{schema_in}.event_types" + """--sql
                left join """ + f"{schema_in}.events" + """--sql
                    on events.event_type_id = event_types.id
                left join """ + f"{schema_in}.event_attributes" + """--sql
                    on event_attributes.event_type_id = event_types.id
                left join """ + f"{schema_in}.event_attribute_values" + """--sql
                    on event_attribute_values.event_id = events.id
            group by
                event_types.id,
                event_types.description
        )

        select
            event_type_description as event_type,
            first_event_timestamp,
            last_event_timestamp,
            event_count,
            event_attribute_count,
            event_attribute_value_update_count
        from 
            overview
        order by
            event_count desc 
    """

    return sql_statement


def _object_stats(schema_in:str):
    """Returns sql statement giving statistics on objects."""

    sql_statement = """--sql
        with overview as(
            select
                object_types.id as object_type_id,
                object_types.description as object_type_description,
                min(object_attribute_values.timestamp) as first_object_update_timestamp,
                max(object_attribute_values.timestamp) as last_object_update_timestamp,
                count(distinct objects.id) as object_count,
                count(distinct object_attributes.id) as object_attribute_count,
                count(distinct object_attribute_values.id) as object_attribute_value_update_count
            from
                """ + f"{schema_in}.object_types" + """--sql
                left join """ + f"{schema_in}.objects" + """--sql
                    on objects.object_type_id = object_types.id
                left join """ + f"{schema_in}.object_attributes" + """--sql
                    on object_attributes.object_type_id = object_types.id
                left join """ + f"{schema_in}.object_attribute_values" + """--sql
                    on object_attribute_values.object_id = objects.id
            group by
                object_types.id,
                object_types.description
        )

        select
            object_type_description as object_type,
            first_object_update_timestamp,
            last_object_update_timestamp,
            object_count,
            object_attribute_count,
            object_attribute_value_update_count
        from 
            overview
        order by
            object_count desc
    """

    return sql_statement
