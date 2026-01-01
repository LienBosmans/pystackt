from pystackt.utils.class_definitions import *

def _initiate_object_types() -> dict:
    """Initiates the object types `procedure`, `notice`."""

    descriptions = ['procedure',
                    'notice'
                   ]
    
    object_types = {}
    for description in descriptions:
        object_types[description] = ObjectType(description)

    return object_types


def _initiate_object_attributes(object_types:dict) -> dict:
    """Initiates below object attributes, linking them to the correct object type.
    `procedure`: `id`, `internal_id`, `title`, `description`, `procedure_type`, `main_purpose`, `legal_basis`, `is_accelerated`.
    `notice`: `ojs_issue_number`, `publication_number`, `notice_type`, `form_type`, `official_language`.
    """

    descriptions = {'procedure':[['id','varchar'],
                                 ['internal_id','varchar'],
                                 ['title','varchar'],
                                 ['description','varchar'],
                                 ['procedure_type','varchar'],
                                 ['main_purpose','varchar'],
                                 ['legal_basis','varchar'],
                                 ['is_accelerated','boolean'],
                                ],
                     'notice':[['ojs_issue_number','varchar'],
                               ['publication_number','varchar'],
                               ['notice_type','varchar'],
                               ['form_type','varchar'],
                               ['official_language','varchar'],
                              ],
                    }
    object_attributes = {}
    for object_type_description,object_attribute_descriptions in descriptions.items():
        object_type = object_types.get(object_type_description)

        for description in object_attribute_descriptions:
            object_attributes[f"{object_type_description}:{description[0]}"] = ObjectAttribute(object_type,description[0],description[1])

    return object_attributes


def _initiate_relation_qualifiers() -> dict:
    """Initiates the relation qualifiers `dispatched`."""

    descriptions = [['dispatched','varchar'],
                    ['published','varchar']
                   ]
    
    relation_qualifiers = {}
    for description in descriptions:
        relation_qualifiers[description[0]] = RelationQualifier(description[0],description[1])

    return relation_qualifiers
