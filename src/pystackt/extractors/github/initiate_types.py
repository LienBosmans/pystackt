from pystackt.extractors.github.class_definitions import *

def _initiate_object_types() -> dict:
    """Initiates the object types `issue`, `user`, `team`, `commit`."""

    descriptions = ['issue',
                    'user',
                    'team',
                    'commit'
                   ]
    
    object_types = {}
    for description in descriptions:
        object_types[description] = ObjectType(description)

    return object_types

def _initiate_object_attributes(object_types:dict) -> dict:
    """Initiates below object attributes, linking them to the correct object type.
    `issue`: `number`, `title`, `state`
    `user`: `id`, `login`, `url`, `type`
    `team`: `id`, `slug`, `name`, `privacy`, `url`
    `commit`: `sha`, `commit_message`, `url`
    """

    descriptions = {'issue':[['number','integer'],
                             ['title','varchar'],
                             ['timeline_url','varchar']
                            ],
                    'user':[['id','integer'],
                            ['login','varchar'],
                            ['url','varchar'],
                            ['type','varchar'],
                           ],
                    'team':[['id','integer'],              
                            ['slug','varchar'],
                            ['name','varchar'],
                            ['privacy','varchar'],
                            ['url','varchar']
                           ],
                    'commit':[['sha','varchar'],              
                              ['commit_message','varchar'],
                              ['url','varchar'],
                           ],
                    }
    object_attributes = {}
    for object_type_description,object_attribute_descriptions in descriptions.items():
        object_type = object_types.get(object_type_description)

        for description in object_attribute_descriptions:
            object_attributes[f"{object_type_description}:{description[0]}"] = ObjectAttribute(object_type,description[0],description[1])

    return object_attributes


def _initiate_relation_qualifiers() -> dict:
    """Initiates the relation qualifiers `created`, `timeline_event`, `actor`, `requested_reviewer`, `requested_team`, `assignee`, `committer`."""

    descriptions = [['timeline_event','varchar'],
                    ['created','varchar'],
                    ['actor','varchar'],
                    ['requested_reviewer','varchar'],
                    ['requested_team','varchar'],
                    ['assignee','varchar'],
                    ['committer','varchar'],
                   ]
    
    relation_qualifiers = {}
    for description in descriptions:
        relation_qualifiers[description[0]] = RelationQualifier(description[0],description[1])

    return relation_qualifiers
