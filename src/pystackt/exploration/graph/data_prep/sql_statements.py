def _graph_base_table(schema_in:str,schema_out:str):
    """Generates a select SQL statement for `events_by_object`."""
    
    sql_statement = """--sql
        with events_by_object as (
            select
                -- event nodes:
                concat('event_', events.id::varchar) as event_node_id,
                events.id as event_id,
                events.description as event_description,
                event_types.id as event_type_id,
                event_types.description as event_type,
                events.timestamp as event_timestamp,
                strftime(events.timestamp,'%c') as event_timestamp_node_id,
                -- object snapshot nodes:
                concat('object_', object_id::varchar, '_', strftime(events.timestamp,'%c')) as snapshot_node_id,
                objects.id as object_id,
                objects.description as object_description,
                object_types.id as object_type_id,
                object_types.description as object_type,
                events.timestamp as snapshot_timestamp,
                strftime(events.timestamp,'%c') as snapshot_timestamp_node_id,
                -- relation between event nodes and object snapshot nodes:
                relation_qualifiers.id as qualifier_id,
                relation_qualifiers.description as qualifier_description,
                -- link to find previous/next event node(s) linked to this object snapshot node:
                rank_dense() OVER (PARTITION BY objects.id ORDER BY events.timestamp ASC) as snapshot_dense_rank
            from
                """ + f"{schema_in}.objects" + """--sql
                inner join """ + f"{schema_in}.event_to_object" + """--sql
                    on event_to_object.object_id = objects.id
                left join """ + f"{schema_in}.relation_qualifiers" + """--sql
                    on event_to_object.qualifier_id = relation_qualifiers.id
                inner join """ + f"{schema_in}.events" + """--sql
                    on event_to_object.event_id = events.id
                inner join """ + f"{schema_in}.object_types" + """--sql
                    on objects.object_type_id = object_types.id
                inner join """ + f"{schema_in}.event_types" + """--sql
                    on events.event_type_id = event_types.id
        )

        select * from events_by_object
    """

    return sql_statement
