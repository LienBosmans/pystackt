import os                                           # Used to check if directory of quack_database exists, and create it if not.
import duckdb                                       # Used to create DuckDB database file.
from datetime import datetime                       # Used to provide feedback on how long data extraction is taking.
import time, math                                   # Used to provide feedback on how long data extraction is taking.

from pystackt.utils.class_definitions import (      # defines custom classes to store data (corresponds to final tables)
    _initiate_global_id
)

from pystackt.extractors.ted.initiate_types import (    # contains pre-defined event/object/relation (attribute) types
# from initiate_types import (
    _initiate_object_types,
    _initiate_object_attributes,
    _initiate_relation_qualifiers
)

from pystackt.extractors.ted.get_data import (      # uses SPARQL queries send to the web api of ted portal to get the data
# from get_data import (
    _get_procedures,
    _get_notices,
    _get_lots,
    _get_organizations
) 

from pystackt.extractors.ted.map_data import (      # maps dataframes extracted via API to custom class objects
# from map_data import (
    _new_object_procedure,
    _new_object_notice,
    _new_object_lot,
    _new_object_organization,
    _new_event_eform,
    _new_event_notice,
    _new_event_lot_deadline
)

from pystackt.utils.map_data import ( # maps the data extracted via API to custom class objects
    _link_event_to_object,
    _link_object_to_object
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

    all_organizations = {}
    all_notices = {}
    existing_procedures = {}

    event_types = {}
    events = {}
    event_attributes = {}
    event_attribute_values = {}

    relation_qualifiers = _initiate_relation_qualifiers()
    event_to_object = {}
    object_to_object = {}
    event_to_object_attribute_value = {}

    ## Data extraction & mapping
    print(f"{datetime.now().strftime("%d-%m-%Y %H:%M")}    Starting data extraction from TED")

    # get procedure objects
    df_procedures = _get_procedures(legal_names=org_legal_names)
    procedure_dicts = df_procedures.to_dicts()
    num_procedures = df_procedures.height

    print(f"{datetime.now().strftime("%d-%m-%Y %H:%M")}    Starting data extraction for {num_procedures} procedures ...")

    print_counter = 0
    perc_done = 0
    seconds_done = 0
    start_time = time.time()

    # first create all procedures, so that relations to other procedures can be created if needed
    for row in procedure_dicts:
        # create procedure object with attributes
        procedure_object = _new_object_procedure(row,object_types,objects,object_attributes,object_attribute_values)
        procedureId = row.get("procedureId")

        # add it to dictionary to fetch later
        existing_procedures[procedureId] = procedure_object

    # next, go over all procedures and get other data to create objects, events and relations
    for row in procedure_dicts:
        # fetch procedure object
        procedureId = row.get("procedureId")
        procedure_object = existing_procedures.get(procedureId)

        procedureInternalId = row.get("procedureInternalId")
        procedureFirstTimestamp = row.get("earliestNoticeTimestamp")

        # get all lots linked to procedure
        df_lots = _get_lots([procedureId])
        lot_dicts = df_lots.to_dicts()

        procedure_lot_objects = {}
        procedure_org_objects = {}

        for row in lot_dicts:
            row["timestamp"] = procedureFirstTimestamp
            lot_object = _new_object_lot(row,object_types,objects,object_attributes,object_attribute_values)

            procedure_lot_objects[row.get("lotId")] = lot_object # for creating object-to-object and event-to-object relations

            _link_object_to_object(
                from_object=procedure_object,
                to_object=lot_object,
                timestamp=procedureFirstTimestamp,
                qualifier_name='divided_into',
                description='procedure divided into lots',
                relation_qualifiers=relation_qualifiers,
                object_to_object=object_to_object
            )

            lot_deadline_event = _new_event_lot_deadline(row,event_types,events,event_attributes,event_attribute_values)

            _link_event_to_object(
                event=lot_deadline_event,
                object=lot_object,
                qualifier_name='deadline',
                description='participation deadline for lot',
                relation_qualifiers=relation_qualifiers,
                event_to_object=event_to_object
            )


        # get all notices linked to procedure
        df_notices = _get_notices([procedureId])
        notice_dicts = df_notices.to_dicts()

        for row in notice_dicts:
            notice_object = _new_object_notice(row,object_types,objects,object_attributes,object_attribute_values)
            all_notices[f"object:{row.get("noticeUri")}"] = notice_object # for creating object-to-object relations

            transmit_eform_event = _new_event_eform(row,event_types,events,event_attributes,event_attribute_values)
            notice_event = _new_event_notice(row,event_types,events,event_attributes,event_attribute_values)
            all_notices[f"event:{row.get("noticeUri")}"] = notice_event # for creating event-to-object relations

            # create event-to-object relation from transmit e-form event to notice object
            _link_event_to_object(
                event=transmit_eform_event,
                object=notice_object,
                qualifier_name='dispatched',
                description='notice transmitted electronically by eSender',
                relation_qualifiers=relation_qualifiers,
                event_to_object=event_to_object
            )

            # create event-to-object relation from publish notice event to notice object
            _link_event_to_object(
                event=notice_event,
                object=notice_object,
                qualifier_name='published',
                description='notice issued publicly',
                relation_qualifiers=relation_qualifiers,
                event_to_object=event_to_object
            )

            # create event-to-object relations from publish notice event to lot object
            for lot in row.get("announcesLotIds").split(','):
                lot_object = procedure_lot_objects.get(lot.strip('"'))
                if lot_object:
                    _link_event_to_object(
                        event=notice_event,
                        object=lot_object,
                        qualifier_name='announces',
                        description='notice announces lot',
                        relation_qualifiers=relation_qualifiers,
                        event_to_object=event_to_object
                    )
            
            # create object-to-object relations from notice object to lot object
            for lot in row.get("refersLotIds").split(','):
                lot_object = procedure_lot_objects.get(lot.strip('"'))
                if lot_object:
                    _link_object_to_object(
                        from_object=notice_object,
                        to_object=lot_object,
                        timestamp=transmit_eform_event.timestamp,
                        qualifier_name='refers_to',
                        description='notice refers to lot',
                        relation_qualifiers=relation_qualifiers,
                        object_to_object=object_to_object
                    )

            # create event-to-object relations from publish notice event to procedure object
            for proc in row.get("announcesProcedureIds").split(','):
                proc_object = existing_procedures.get(proc.strip('"'))
                if proc_object:
                    _link_event_to_object(
                        event=notice_event,
                        object=proc_object,
                        qualifier_name='announces',
                        description='notice announces procedure',
                        relation_qualifiers=relation_qualifiers,
                        event_to_object=event_to_object
                    )
            
            # create object-to-object relations from notice object to procedure object
            for proc in row.get("refersProcedureIds").split(','):
                proc_object = existing_procedures.get(proc.strip('"'))
                if proc_object:
                    _link_object_to_object(
                        from_object=notice_object,
                        to_object=proc_object,
                        timestamp=transmit_eform_event.timestamp,
                        qualifier_name='refers_to',
                        description='notice refers to procedure',
                        relation_qualifiers=relation_qualifiers,
                        object_to_object=object_to_object
                    )

        # get all organizations linked to notices and their role & relations
        notice_uris = df_notices["noticeUri"].to_list()
        df_organizations = _get_organizations(notice_uris)
        organization_dicts = df_organizations.to_dicts()

        # first, create all organization objects so they can be used for relations later
        for row in organization_dicts:
            legal_id = row.get("legalIdentifier")
            legal_name = row.get("legalName")
            org_id = row.get("orgId")
            
            # get organization object, create it if it doesn't exist yet
            organization_object = all_organizations.get((legal_id,legal_name))
            if not organization_object:
                organization_object = _new_object_organization(row,object_types,objects,object_attributes,object_attribute_values)
                all_organizations[(legal_id,legal_name)] = organization_object
            
            procedure_org_objects[org_id] = organization_object # for creating object-to-object relations

        # next, create relations
        for row in organization_dicts:
            legal_id = row.get("legalIdentifier")
            legal_name = row.get("legalName")
            timestamp = row.get("noticeESenderDispatchDate")
            role = row.get("role")
            org_id = row.get("orgId")
            on_behalf_of_org_id = row.get("actsOnBehalfOfOrgId")

            organization_object = all_organizations.get((legal_id,legal_name))

            # create object-to-object relation from notice object to organization object
            notice_object = all_notices.get(f"object:{row.get("noticeUri")}")
            if notice_object:
                _link_object_to_object(
                    from_object=notice_object,
                    to_object=organization_object,
                    timestamp=timestamp,
                    qualifier_name='refers_to_role',
                    description=f'notice refers to {role}',
                    relation_qualifiers=relation_qualifiers,
                    object_to_object=object_to_object
                )

            # create event-to-object relations from publish notice event to organization object
            notice_event = all_notices.get(f"event:{row.get("noticeUri")}")
            if row.get("isAnnounced"):
                _link_event_to_object(
                    event=notice_event,
                    object=organization_object,
                    qualifier_name=f'announces_role',
                    description=f'notice announces {role}',
                    relation_qualifiers=relation_qualifiers,
                    event_to_object=event_to_object
                )
            
            # create object-to-object relation from organization object to organization object
            if on_behalf_of_org_id:
                on_behalf_of_org_object = procedure_org_objects.get(on_behalf_of_org_id)
                if on_behalf_of_org_object:
                    _link_object_to_object(
                        from_object=organization_object,
                        to_object=on_behalf_of_org_object,
                        timestamp=timestamp,
                        qualifier_name='acts_on_behalf_of',
                        description=f'acts as {role} on behalf of for procedure {procedureInternalId}',
                        relation_qualifiers=relation_qualifiers,
                        object_to_object=object_to_object
                    )

            # create object-to-object relations from organization object to lot object
            for lot in row.get("lotIds").split(','):
                lot_object = procedure_lot_objects.get(lot.strip('"'))
                if lot_object:
                    _link_object_to_object(
                        from_object=organization_object,
                        to_object=lot_object,
                        timestamp=timestamp,
                        qualifier_name='role_context',
                        description=f'acts as {role} for',
                        relation_qualifiers=relation_qualifiers,
                        object_to_object=object_to_object
                    )

        # keep user informed about progress
        print_counter += 1
        prev_perc_done = perc_done
        perc_done = print_counter/num_procedures

        prev_seconds_done = seconds_done
        seconds_done = time.time() - start_time

        bool_print = (
            print_counter == 1 # always print first time
            or math.floor(perc_done*100) > math.floor(prev_perc_done*100) # print every 1% progress
            or math.floor(seconds_done/(60*5)) > math.floor(prev_seconds_done/(60*5)) # print every 5 minutes
        )
        
        if bool_print: 
            print(f"{datetime.now().strftime("%d-%m-%Y %H:%M")}    Extracting and mapping data for procedure {procedureInternalId} done ...{round(100*perc_done,1)}% (about {round(seconds_done/perc_done - seconds_done,1)}s remaining)")

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


# legal_names = ['"Imec EU Pilot line NV"@en', '"IMEC VZW"@en']
# legal_names = ['"Intercommunale Ontwikkelingsorganisatie voor de Kempen"@nl']
# get_ted_log(org_legal_names=legal_names)
