from pystackt.utils.class_definitions import *

def _link_event_to_object(event:Event,object:Object,qualifier_name,description,relation_qualifiers:dict,event_to_object:dict) -> EventToObjectRelation:
    '''Returns a new event-to-object link and adds it to the event_to_object dictionary.'''
    
    new_link = EventToObjectRelation(event,object,relation_qualifiers.get(qualifier_name),description)
    event_to_object[new_link.id] = new_link

    return  new_link

def _link_object_to_object(from_object:Object,to_object:Object,timestamp,qualifier_name,description,relation_qualifiers:dict,object_to_object:dict) -> ObjectToObjectRelation:
    '''Returns a new object-to-object link and adds it to the event_to_object dictionary.'''
    
    new_link = ObjectToObjectRelation(from_object,to_object,relation_qualifiers.get(qualifier_name),timestamp,description)
    object_to_object[new_link.id] = new_link

    return  new_link

def _get_or_create_event_type(description:str,event_types:dict) -> EventType:
    """Use `description` as key to retrieve item from `event_types`.
     If item does not exist, create new EventType object and add it to `event_types`."""
    event_type = event_types.get(description)

    if event_type is None:
        event_type = EventType(description)
        event_types[description] = event_type

    return event_type
