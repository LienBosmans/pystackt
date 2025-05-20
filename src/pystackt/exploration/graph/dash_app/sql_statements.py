def _filtered_base_table(schema:str, event_types:list, object_types:list, object_ids:list):
    """Generates a select SQL statement for `filtered_base_table`."""
    
    sql_statement = """--sql
        with filtered_events as ( -- get all events for which at least one of the objects is involved
            select 
                event_id
            from 
                """ + f"{schema}.graph_base_table as bt" + """--sql
            where
                """ + f"object_id in ({",".join([f"'{x}'" for x in object_ids])})" + """--sql
            group by
                event_id
        ),
        filtered_base_table as ( -- filter on relevant events, object types and event types
            select 
                bt.* exclude (snapshot_dense_rank),
                rank_dense() OVER (PARTITION BY bt.object_id ORDER BY bt.snapshot_timestamp ASC) as snapshot_dense_rank
            from 
                """ + f"{schema}.graph_base_table as bt" + """--sql
                semi join filtered_events as ev
                    on bt.event_id = ev.event_id
            where 
                """ + f"object_type in ({",".join([f"'{x}'" for x in object_types])})" + """--sql
                """ + f"and event_type in ({",".join([f"'{x}'" for x in event_types])})" + """--sql
        )

        select * from filtered_base_table
    """

    return sql_statement


def _event_nodes(schema:str, filtered_base_table:str):
    """Generate a select SQL statement for `event_nodes`"""

    sql_statement = """--sql
        with event_nodes as (
            select 
                event_node_id,
                event_description,
                event_type,
                event_timestamp,
                event_timestamp_node_id
            from 
                """ + f"{schema}.{filtered_base_table} as bt" + """--sql
            group by all
        )

        select * from event_nodes order by event_timestamp_node_id
    """

    return sql_statement

def _object_snapshot_nodes(schema:str, filtered_base_table:str):
    """Generates a select SQL statement for `object_snapshot_nodes`.
    No object attribute updates for now, only object snapshots related to events."""

    sql_statement = """--sql
        with object_snapshot_nodes as (
            select 
                snapshot_node_id,
                object_description,
                object_type as object_type,
                snapshot_timestamp,
                snapshot_timestamp_node_id
            from 
                """ + f"{schema}.{filtered_base_table} as bt" + """--sql
            group by all
        )

        select * from object_snapshot_nodes order by snapshot_timestamp_node_id
    """

    return sql_statement


def _timestamp_nodes(schema:str, filtered_base_table:str):
    """Generates a select SQL statement for `object_snapshot_nodes`.
    No object attribute updates for now, only object snapshots related to events."""

    sql_statement = """--sql
        with snapshot_timestamp_nodes as (
            select 
                snapshot_timestamp_node_id as timestamp_node_id
            from 
                """ + f"{schema}.{filtered_base_table} as bt" + """--sql
            group by all
        ),
        event_timestamp_nodes as (
            select 
                event_timestamp_node_id as timestamp_node_id
            from 
                """ + f"{schema}.{filtered_base_table} as bt" + """--sql
            group by all
        ),
        timestamp_nodes as (
            select timestamp_node_id from snapshot_timestamp_nodes
            union all
            select timestamp_node_id from event_timestamp_nodes
        )

        select * from timestamp_nodes group by all order by timestamp_node_id
    """

    return sql_statement


def _event_to_object_snapshot_edges(schema:str, filtered_base_table:str):
    """Generate a select SQL statement for `event_to_object_snapshot_edges`"""

    sql_statement = """--sql
        with edges as (
            select 
                event_node_id as source_node_id,
                snapshot_node_id as target_node_id,
                qualifier_description,
                object_type,
                event_type
            from 
                """ + f"{schema}.{filtered_base_table} as bt" + """--sql
        )

        select * from edges
    """

    return sql_statement


def _object_snapshot_to_next_event_edges(schema:str, filtered_base_table:str):
    """Generate a select SQL statement for `object_snapshot_to_next_event_edges`"""

    sql_statement = """--sql
        with edges as (
            select 
                bt.snapshot_node_id as source_node_id,
                next_event.event_node_id as target_node_id,
                bt.object_type,
                next_event.event_type
            from 
                """ + f"{schema}.{filtered_base_table} as bt" + """--sql
                inner  join """ + f"{schema}.{filtered_base_table} as next_event" + """--sql
                    on (
                        bt.object_id = next_event.object_id
                        and bt.snapshot_dense_rank + 1 = next_event.snapshot_dense_rank
                    )
        )

        select * from edges
    """

    return sql_statement
