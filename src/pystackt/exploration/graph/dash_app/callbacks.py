# Contains app callbacks that provide the interactivity

from dash import Dash, html, Input, Output, dcc, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import duckdb
import polars as pl
import os

from pystackt.exploration.graph.dash_app.sql_statements import (
    _filtered_base_table, 
    _event_nodes, 
    _object_snapshot_nodes, 
    _timestamp_nodes, 
    _event_to_object_snapshot_edges, 
    _object_snapshot_to_next_event_edges
)

def _register_callbacks(app, quack_db:str, schema:str, event_color_map:dict, object_color_map:dict):

    @app.callback( # update cytoscape based on selected objects, object types, and event types
        Output("cytoscape-event-flow","elements"),
        [
            Input("event-types-checklist","value"),
            Input("object-types-checklist","value"),
            Input("object-table", "selected_rows"),
            Input("object-table", "data")
        ]
    )
    def update_graph(selected_event_types, selected_object_types, selected_rows, table_data):
        if (not selected_event_types) or (not selected_object_types) or (not selected_rows):
            return []
        
        selected_object_ids = [table_data[i]["object_id"] for i in selected_rows]

        # print("Selected rows:", selected_rows)
        # print("Selected object IDs:", selected_object_ids)

        # print("Selected object types:", selected_object_types)
        # print("Selected event types:", selected_event_types)
        
        with duckdb.connect(quack_db) as quack:
            # print(_filtered_base_table(schema, selected_event_types, selected_object_types, selected_object_ids))
            filtered_base_table = quack.sql(_filtered_base_table(schema, selected_event_types, selected_object_types, selected_object_ids)) #.show() #show for debug

            timestamp_parent_nodes = quack.sql(_timestamp_nodes(schema, "filtered_base_table")).pl()
            event_nodes = quack.sql(_event_nodes(schema, "filtered_base_table")).pl()
            object_snapshot_nodes = quack.sql(_object_snapshot_nodes(schema, "filtered_base_table")).pl()
            event_to_object_snapshot_edges = quack.sql(_event_to_object_snapshot_edges(schema, "filtered_base_table")).pl()
            object_snapshot_to_next_event_edges = quack.sql(_object_snapshot_to_next_event_edges(schema, "filtered_base_table")).pl()

        elements = [ # parent nodes
            {
                'data': {
                    'id': x['timestamp_node_id'],
                    'label': x['timestamp_node_id']
                },
                'classes': 'timestamp'
            } for x in timestamp_parent_nodes.sort('timestamp_node_id').to_dicts()
        ] + [ # event nodes
            {
                'data': {
                    'id': x['event_node_id'], 
                    'label': x['event_type'], 
                    'parent': x['event_timestamp_node_id'], 
                    'color': event_color_map[x['event_type']]
                },
                'classes': 'event'
            } for x in event_nodes.to_dicts()
        ] + [ # object snapshot nodes
            {
                'data': {
                    'id': x['snapshot_node_id'], 
                    'label': x['object_description'], 
                    'parent': x['snapshot_timestamp_node_id'],
                    'color': object_color_map[x['object_type']]
                }, 
                'classes': 'object'
            } for x in object_snapshot_nodes.to_dicts()
        ] + [ # event to object snapshot edges
            {
                'data': {
                    'source': x['source_node_id'], 
                    'target': x['target_node_id'], 
                    'label': x['qualifier_description'],
                    'color': object_color_map[x['object_type']]
                }, 
                'classes': 'linked'
            } for x in event_to_object_snapshot_edges.to_dicts()
        ] + [ # object snapshot to next event edges
            {
                'data': {
                    'source': x['source_node_id'], 
                    'target': x['target_node_id'],
                    'color': object_color_map[x['object_type']]
                }, 
                'classes': 'follows'
            } for x in object_snapshot_to_next_event_edges.to_dicts()
        ]

        return elements
