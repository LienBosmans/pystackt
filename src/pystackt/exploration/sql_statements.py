def _event_stats(schema_in:str):
    """Returns sql statement giving statistics on events."""

    sql_statement = """--sql
        select 
            events.event_type_id,
            event_types.description as event_type_description,
            count(events.id) as number_of_events,
            """ + f"count(events.id) / (select count(*) from {schema_in}.events) as perc_of_events" + """--sql
        from
            """ + f"{schema_in}.events" + """--sql
            left join """ + f"{schema_in}.event_types" + """--sql
                on events.event_type_id = event_types.id
        group by 
            events.event_type_id,
            event_types.description
        order by 
            number_of_events desc
    """

    return sql_statement


def _object_stats(schema_in:str):
    """Returns sql statement giving statistics on objects."""

    sql_statement = """--sql
        select 
            objects.object_type_id,
            object_types.description as object_type_description,
            count(objects.id) as number_of_objects,
            """ + f"count(objects.id) / (select count(*) from {schema_in}.objects) as perc_of_objects" + """--sql
        from
            """ + f"{schema_in}.objects" + """--sql
            left join """ + f"{schema_in}.object_types" + """--sql
                on objects.object_type_id = object_types.id
        group by 
            objects.object_type_id,
            object_types.description
        order by 
            number_of_objects desc
    """

    return sql_statement
