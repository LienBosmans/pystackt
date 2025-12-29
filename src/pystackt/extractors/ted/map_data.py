from pystackt.utils.class_definitions import *

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
    attributes = [['procedure:id','procedureId'],    
                  ['procedure:internal_id','procedureInternalId'],
                  ['procedure:title','procedureTitle'],
                  ['procedure:description','procedureDescription'],
                  ['procedure:procedure_type','procedureType']
                  ]

    timestamp = data.get('earliestNoticeTimestamp')

    for attribute_def in attributes:
        object_attribute = object_attributes.get(attribute_def[0])  # get object_attribute with attribute_name
        attribute_value = data.get(attribute_def[1])          # extract attribute_value from issue_data with defined key

        new_object_attribute_value = ObjectAttributeValue(object,object_attribute,timestamp,attribute_value)

        object_attribute_values[new_object_attribute_value.id] = new_object_attribute_value

    return None
