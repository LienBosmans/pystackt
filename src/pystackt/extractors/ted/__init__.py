import os                                           # Used to check if directory of quack_database exists, and create it if not.
import duckdb                                       # Used to create DuckDB database file.
from datetime import datetime                       # Used to provide feedback on how long data extraction is taking.

from pystackt.utils.class_definitions import (      # defines custom classes to store data (corresponds to final tables)
    _initiate_global_id
)

from pystackt.extractors.ted.initiate_types import (    # contains pre-defined event/object/relation (attribute) types
# from initiate_types import (
    _initiate_object_types,
    _initiate_object_attributes
)

from pystackt.extractors.ted.get_data import (      # uses SPARQL queries send to the web api of ted portal to get the data
# from get_data import (
    _get_procedures
) 

from pystackt.extractors.ted.map_data import (      # maps dataframes extracted via API to custom class objects
# from map_data import (
    _new_object_procedure
)

from pystackt.utils.output_data import (   # converts custom class objects to dataframes (polars) and stores them in DuckDB database file
    _store_result
)


def get_ted_log(org_legal_names:list,
                quack_db:str="./quack.duckdb",schema:str="main"):
    """
    Uses list of legal names to extract event data related to procedures in which these organizations were involved.
    """

    # Check if DuckDB database is available first. Don't connect to the database while the script is running!
    print(f"Checking if DuckDB database file {quack_db} is available. New file will be created if it does not exist yet.")

    # Ensure directory exists
    directory = os.path.dirname(quack_db)
    os.makedirs(directory, exist_ok=True)

    con = duckdb.connect(quack_db)
    con.close()
    print(f"    IMPORTANT! Do not connect to DuckDB database file '{quack_db}' while this script is running!")
    print(f"    (Or, if you like living on the edge, at least disconnect before the script tries writing to it.)")


    # Initiate global id used to generate unique integer id's
    _initiate_global_id()

    # Initiate dictionaries to store data
    object_types = _initiate_object_types()
    object_attributes = _initiate_object_attributes(object_types)
    objects = {}
    object_attribute_values = {}

    existing_xs = {} # aditional dictionary used to check if a x already exists as an object (will probably need this for organizations, notices, etc.)

    event_types = {}
    events = {}
    event_attributes = {}
    event_attribute_values = {}

    relation_qualifiers = {} #_initiate_relation_qualifiers()
    event_to_object = {}
    object_to_object = {}
    event_to_object_attribute_value = {}

    ## Data extraction & mapping
    print(f"{datetime.now().strftime("%d-%m-%Y %H:%M")}    Starting data extraction from TED")

    # get procedure objects
    df_procedures = _get_procedures(legal_names=org_legal_names)
    procedure_dicts = df_procedures.to_dicts()

    for row in procedure_dicts:
        procedure_object = _new_object_procedure(row,object_types,objects,object_attributes,object_attribute_values)


    ## Store the result (includes print statements)
    _store_result(
        object_types=object_types,
        objects=objects,
        object_attributes=object_attributes,
        object_attribute_values=object_attribute_values,
        event_types=event_types,
        events=events,
        event_attributes=event_attributes,
        event_attribute_values=event_attribute_values,
        relation_qualifiers=relation_qualifiers,
        event_to_object=event_to_object,
        object_to_object=object_to_object,
        event_to_object_attribute_value=event_to_object_attribute_value,
        extracted_from_message="extracted from TED ",
        quack_db=quack_db,
        schema=schema
    )
        
    print(f"{datetime.now().strftime("%d-%m-%Y %H:%M")}    All done!")


# legal_names = ["Imec EU Pilot line NV", "IMEC VZW"]
# get_ted_log(org_legal_names=legal_names)
