from pystackt.utils.class_definitions import *

def _initiate_object_types() -> dict:
    """Initiates the object types `procedure`."""

    descriptions = ['procedure',
                   ]
    
    object_types = {}
    for description in descriptions:
        object_types[description] = ObjectType(description)

    return object_types


def _initiate_object_attributes(object_types:dict) -> dict:
    """Initiates below object attributes, linking them to the correct object type.
    `procedure`: `id`, `internal_id`, `title`, `description`, `procedure_type`
    """

    descriptions = {'procedure':[['id','varchar'],
                                 ['internal_id','varchar'],
                                 ['title','varchar'],
                                 ['description','varchar'],
                                 ['procedure_type','varchar'],
                                ],
                    }
    object_attributes = {}
    for object_type_description,object_attribute_descriptions in descriptions.items():
        object_type = object_types.get(object_type_description)

        for description in object_attribute_descriptions:
            object_attributes[f"{object_type_description}:{description[0]}"] = ObjectAttribute(object_type,description[0],description[1])

    return object_attributes
