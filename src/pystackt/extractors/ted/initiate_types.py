from pystackt.utils.class_definitions import *

def _initiate_object_types() -> dict:
    """Initiates the object types `procedure`, `notice`, `lot`, `organization`."""

    descriptions = ['procedure',
                    'notice',
                    'lot',
                    'role',
                    'organization',
                   ]
    
    object_types = {}
    for description in descriptions:
        object_types[description] = ObjectType(description)

    return object_types


def _initiate_object_attributes(object_types:dict) -> dict:
    """Initiates object attributes, linking them to the correct object type."""

    descriptions = {'procedure':[['procedure_id','varchar'],
                                 ['internal_procedure_id','varchar'],
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
                               ['notice_type_description','varchar'],
                               ['form_type','varchar'],
                               ['official_language','varchar'],
                              ],
                     'lot':[['lot_id','varchar'],
                            ['internal_lot_id','varchar'],
                            ['title','varchar'],
                            ['description','varchar'],
                            ['main_purpose','varchar'],
                           ],
                     'role':[['role','varchar'],
                             ['org_id','varchar']
                            ],
                     'organization':[['legal_name','varchar'],
                                     ['legal_identifier','varchar'],
                                    ],
                    }
    object_attributes = {}
    for object_type_description,object_attribute_descriptions in descriptions.items():
        object_type = object_types.get(object_type_description)

        for description in object_attribute_descriptions:
            object_attributes[f"{object_type_description}:{description[0]}"] = ObjectAttribute(object_type,description[0],description[1])

    return object_attributes


def _initiate_relation_qualifiers() -> dict:
    """Initiates the relation qualifiers."""

    descriptions = [['dispatched','varchar'],
                    ['published','varchar'],
                    ['refers_to','varchar'],
                    ['divided_into','varchar'],
                    ['announces_lot','varchar'],
                    ['announces_procedure','varchar'],
                    ['deadline','varchar'],
                    ['announces_role','varchar'],
                    ['played_by','varchar'],
                    ['acts_on_behalf_of','varchar'],
                    ['role_context','varchar'],
                    ['refers_to_role','varchar'],
                   ]
    
    relation_qualifiers = {}
    for description in descriptions:
        relation_qualifiers[description[0]] = RelationQualifier(description[0],description[1])

    return relation_qualifiers
