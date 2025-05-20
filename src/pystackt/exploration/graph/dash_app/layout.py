# Contains app layout

from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import polars as pl

external_stylesheets = [dbc.themes.FLATLY]
cyto.load_extra_layouts()
from pystackt.exploration.graph.dash_app.stylesheets import graph_stylesheet

def _assign_layout(app, event_types, object_types, objects_df):
    app.layout = dbc.Container([
        dcc.Store(id='stored-event-types', data=[]),
        dcc.Store(id='stored-object-types', data=[]),
        dcc.Store(id='stored-event-color-map', data={}),
        dcc.Store(id='stored-object-color-map', data={}),
        dcc.Store(id='duckdb-file-path', data=""),

        dbc.Row([
            html.Div(
                'Interactive data exploration for object-centric event data', 
                className="text-primary text-center fs-3"),

            dbc.Card([
                dbc.CardHeader("Select objects to explore. (Note that selecting too many object might result in freezing the app.)"),
                dbc.CardBody([
                    dash_table.DataTable(
                        id="object-table",
                        columns=[
                            {"name": "Object Type", "id": "object_type"},
                            {"name": "Object", "id": "object_description"},
                            {"name": "ID", "id": "object_id"}, # needed to pass to callback
                        ],
                        data=objects_df.to_dicts(),
                        filter_action="native",
                        sort_action="native",
                        page_action="none",
                        page_size=10,
                        row_selectable="multi",
                        selected_rows=[],
                        style_table={"overflowX": "auto", "border": "1px solid #dee2e6", "maxHeight": "250px"},
                        style_cell={"textAlign": "left", "padding": "0.75rem", "border": "1px solid #dee2e6", "fontFamily": "'Helvetica Neue', Helvetica, Arial, sans-serif", "fontSize": "0.875rem", "color": "#212529"},
                        style_header = {"backgroundColor": "#2C3E50", "color": "white", "fontWeight": "600", "border": "1px solid #dee2e6", "textAlign": "left", "padding": "0.75rem", "fontFamily": "'Helvetica Neue', Helvetica, Arial, sans-serif", "fontSize": "0.875rem"},
                        style_cell_conditional=[{"if": {"column_id": "object_id"},"display": "none"}],
                    ),
                    html.P(id="selected-object-ids", className="fst-italic small"),
                ]),
            ], class_name="card border-primary mb-3"),
        ], style={"marginBottom": "1rem"}),

        dbc.Row([       
            dbc.Col([

                dbc.Card([
                    dbc.CardHeader("Event types"),
                    dbc.CardBody([
                        dbc.Checklist(
                            id="event-types-checklist",
                            options=[{"label": x, "value": x} for x in event_types],
                            value=event_types,
                        ),
                        html.P(id="selected-event-types", className="fst-italic small")
                    ]),
                ], class_name="card border-primary mb-3"),

                dbc.Card([
                    dbc.CardHeader("Object types"),
                    dbc.CardBody([
                        dbc.Checklist(
                            id="object-types-checklist",
                            options=[{"label": x, "value": x} for x in object_types],
                            value=object_types,
                        ),
                        html.P(id="selected-object-types", className="fst-italic small")
                    ]),
                ], class_name="card border-primary mb-3"),

            ], width = 4),

            dbc.Col([
                cyto.Cytoscape(
                    id='cytoscape-event-flow',
                    layout={'name': 'dagre'},
                    # style={'width': '100%', 'height': '100%'}, #gives errors when using multiple columns
                    stylesheet=graph_stylesheet,
                    elements=[],
                    style={
                        'width': '100%',
                        'height': '100%',
                        'border': '1px solid #2c3e50',
                        'borderRadius': '0.4rem',
                        # 'backgroundColor': '#f8f9fa'
                    }            
                )
            ])

        ],style={"marginBottom": "1rem", "height":"90vh"})
    ], fluid=False)
