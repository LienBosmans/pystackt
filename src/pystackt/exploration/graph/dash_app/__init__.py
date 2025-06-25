from dash import Dash
import dash_bootstrap_components as dbc
import webbrowser
import duckdb
from collections import defaultdict

from pystackt.exploration.graph.dash_app.colormaps import _assign_colors
from pystackt.exploration.graph.dash_app.layout import _assign_layout
from pystackt.exploration.graph.dash_app.callbacks import _register_callbacks
external_stylesheets = [dbc.themes.FLATLY]


def start_visualization_app(quack_db:str,schema:str,host:str='127.0.0.1',port:int=5555):

    # Get distinct event types, object types, and objects
    with duckdb.connect(quack_db) as quack:
        event_types_raw = quack.sql(f"select event_type from graph_data_prep.graph_base_table group by event_type order by event_type").fetchall()
        event_types = [row[0] for row in event_types_raw]

        object_types_raw = quack.sql(f"select object_type from graph_data_prep.graph_base_table group by object_type order by object_type").fetchall()
        object_types = [row[0] for row in object_types_raw]

        objects_df = quack.sql(f"select object_id, object_description, object_type from graph_data_prep.graph_base_table group by all order by object_type, object_description").pl()

    # Asign colors to object types and event types
    event_color_map = _assign_colors(event_types,'magma')
    object_color_map = _assign_colors(object_types,'viridis')

    app = Dash(__name__, external_stylesheets=external_stylesheets)

    # Assign layout defined in layout.py
    _assign_layout(app, event_types, object_types, objects_df)

    # Register callbacks defined in callbacks.py
    _register_callbacks(app, quack_db, schema, event_color_map, object_color_map)

    # Run app and open it in default browser
    webbrowser.open(f"http://{host}:{port}/")   # opens app in default browser
    app.run(debug=False, host=host, port=port, use_reloader=False) # starts app
