from pystackt.utils.class_definitions import *
from pystackt.utils.map_data import (
    _get_or_create_event_type
)

def _new_object_procedure(data:dict,
        object_types:dict,objects:dict,object_attributes:dict,object_attribute_values:dict) -> Object:
    '''Returns a new object of type `procedure` and adds it to the objects dictionary.
    Next, function `_new_procedure_attributes` is called to create and store its attributes.'''

    description = data.get("procedureInternalId")
    object_type = object_types.get("procedure")

    new_object = Object(object_type,description)
    objects[new_object.id] = new_object

    _new_procedure_attributes(new_object,data,object_attributes,object_attribute_values)

    return new_object


def _new_procedure_attributes(object:Object,data:dict,object_attributes:dict,object_attribute_values:dict) -> None:
    '''Sets the attributes for a new object of type `procedure` and adds them to the object_attribute_values dictionary.'''

                 # first string is key to get attribute, second string is key to use to extract from issue_data
    attributes = [['procedure:procedure_id','procedureId'],    
                  ['procedure:internal_procedure_id','procedureInternalId'],
                  ['procedure:title','procedureTitles'],
                  ['procedure:description','procedureDescriptions'],
                  ['procedure:procedure_type','procedureType'],
                  ['procedure:main_purpose','mainPurpose'],
                  ['procedure:legal_basis','legalBasis'],
                  ['procedure:is_accelerated','isAccelerated'],
                 ]

    timestamp = data.get('earliestNoticeTimestamp')

    for attribute_def in attributes:
        object_attribute = object_attributes.get(attribute_def[0])  # get object_attribute with attribute_name
        attribute_value = data.get(attribute_def[1])          # extract attribute_value from issue_data with defined key

        new_object_attribute_value = ObjectAttributeValue(object,object_attribute,timestamp,attribute_value)

        object_attribute_values[new_object_attribute_value.id] = new_object_attribute_value

    return None


def _new_object_notice(data:dict,
        object_types:dict,objects:dict,object_attributes:dict,object_attribute_values:dict) -> Object:
    '''Returns a new object of type `notice` and adds it to the objects dictionary.
    Next, function `_new_notice_attributes` is called to create and store its attributes.'''

    description = data.get("noticePublicationNumber")
    object_type = object_types.get("notice")

    new_object = Object(object_type,description)
    objects[new_object.id] = new_object

    _new_notice_attributes(new_object,data,object_attributes,object_attribute_values)

    return new_object


def _new_notice_attributes(object:Object,data:dict,object_attributes:dict,object_attribute_values:dict) -> None:
    '''Sets the attributes for a new object of type `notice` and adds them to the object_attribute_values dictionary.'''

                 # first string is key to get attribute, second string is key to use to extract from issue_data
    attributes = [['notice:ojs_issue_number','ojsIssueNumber'],
                  ['notice:publication_number','noticePublicationNumber'],
                  ['notice:form_type','noticeFormType'],
                  ['notice:notice_type','noticeType'],
                  ['notice:notice_type_description','noticeTypeDescription'],
                #   ['notice:',''],
                #   ['notice:',''],
                #   ['notice:',''],
                 ]

    timestamp = data.get('noticeESenderDispatchDate')

    for attribute_def in attributes:
        object_attribute = object_attributes.get(attribute_def[0])  # get object_attribute with attribute_name
        attribute_value = data.get(attribute_def[1])          # extract attribute_value from issue_data with defined key

        new_object_attribute_value = ObjectAttributeValue(object,object_attribute,timestamp,attribute_value)

        object_attribute_values[new_object_attribute_value.id] = new_object_attribute_value

    return None


def _new_object_lot(data:dict,
        object_types:dict,objects:dict,object_attributes:dict,object_attribute_values:dict) -> Object:
    '''Returns a new object of type `lot` and adds it to the objects dictionary.
    Next, function `_new_lot_attributes` is called to create and store its attributes.'''

    description = data.get("lotTitles")
    object_type = object_types.get("lot")

    new_object = Object(object_type,description)
    objects[new_object.id] = new_object

    _new_lot_attributes(new_object,data,object_attributes,object_attribute_values)

    return new_object


def _new_lot_attributes(object:Object,data:dict,object_attributes:dict,object_attribute_values:dict) -> None:
    '''Sets the attributes for a new object of type `notice` and adds them to the object_attribute_values dictionary.'''

                 # first string is key to get attribute, second string is key to use to extract from issue_data
    attributes = [['lot:lot_id','lotId'],
                  ['lot:internal_lot_id','internalId'],
                  ['lot:title','lotTitles'],
                  ['lot:description','lotDescriptions'],
                  ['lot:main_purpose','mainPurpose'],
                 ]

    timestamp = data.get('timestamp')

    for attribute_def in attributes:
        object_attribute = object_attributes.get(attribute_def[0])  # get object_attribute with attribute_name
        attribute_value = data.get(attribute_def[1])          # extract attribute_value from issue_data with defined key

        new_object_attribute_value = ObjectAttributeValue(object,object_attribute,timestamp,attribute_value)

        object_attribute_values[new_object_attribute_value.id] = new_object_attribute_value

    return None


def _new_event_eform(data:dict,
                     event_types:dict,events:dict,event_attributes:dict,event_attribute_values:dict) -> Event:
    '''Returns a new event of type `transmit_eform` and adds it to the events dictionary.'''

    description = f"Transmit e-form for notice {data.get('noticePublicationNumber')}"
    timestamp = data.get('noticeESenderDispatchDate')
    event_type = _get_or_create_event_type('transmit_eform',event_types)

    new_event = Event(event_type,timestamp,description)
    events[new_event.id] = new_event

    return new_event

def _new_event_notice(data:dict,
                     event_types:dict,events:dict,event_attributes:dict,event_attribute_values:dict) -> Event:
    '''Returns a new event of type `transmit_eform` and adds it to the events dictionary.'''

    description = f"Publish notice {data.get('noticePublicationNumber')}"
    timestamp = data.get('noticePublicationDate')
    event_type = _get_or_create_event_type(f"publish_{data.get('noticeType')}",event_types)

    new_event = Event(event_type,timestamp,description)
    events[new_event.id] = new_event

    return new_event
