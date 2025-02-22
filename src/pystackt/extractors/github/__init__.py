import time     # Used to provide user feedback on how long data extraction is taking.                        
import os       # Used to check if directory of quack_database exists, and create it if not.
import duckdb   # Used to create DuckDB database file.                   


from pystackt.extractors.github.get_data import (  # uses the PyGithub Python library to access the GitHub REST API to get the data
    _connect_to_github_repo,
    _get_issues,
    _get_events
)

from pystackt.extractors.github.class_definitions import ( # defines custom classes to store data (corresponds to final tables)
    _initiate_global_id
)

from pystackt.extractors.github.initiate_types import (    # contains pre-defined event/object/relation (attribute) types
    _initiate_object_types,
    _initiate_object_attributes,
    _initiate_relation_qualifiers
)

from pystackt.extractors.github.map_data import (  # maps the data extracted via API to custom class objects
    _new_object_issue,
    _new_event_created,
    _link_event_to_object,
    _get_object_user, 
    _link_object_to_object, 
    _new_timeline_event,
    _new_object_commit
)

from pystackt.extractors.github.output_data import (   # converts custom class objects to dataframes (polars)
    _dataframe_to_persistent_duckdb,
    _extract_dataframe
)

def get_github_log(GITHUB_ACCESS_TOKEN:str,repo_owner:str,repo_name:str,max_issues:int,quack_db:str="./quack.duckdb"):
    """
    Uses Github access token to extract event data related from issues in specified GitHub repository (`repo_owner`/`repo_name`),
    and store it in a DuckDB database file (`quack_db`). Returns the `max_issues` most recent issues that are currently closed.
    If max_issues is None, all issues are returned.
    """

    # Check if DuckDB database is available first. Don't connect to the database while the script is running!
    print(f"Checking if DuckDB database file {quack_db} is available. New file will be created if it does not exist yet.")

    # Ensure directory exists
    directory = os.path.dirname(quack_db)
    os.makedirs(directory, exist_ok=True)

    con = duckdb.connect(quack_db)
    con.close()
    print(f"    IMPORTANT! Do not connect to DuckDB database file '{quack_db}' while this script is running!")
    print(f"    (Or, if you like living on the edge, at least disconnect before all issues are extracted and the script tries writing to it.)")


    # Connect to repository
    repo = _connect_to_github_repo(GITHUB_ACCESS_TOKEN,repo_owner,repo_name)

    # Initiate global id used to generate unique integer id's
    _initiate_global_id()

    # Initiate dictionaries to store data
    object_types = _initiate_object_types()
    object_attributes = _initiate_object_attributes(object_types)
    objects = {}
    object_attribute_values = {}

    existing_users = {} # aditional dictionary used to check if a user already exists as an object

    event_types = {}
    events = {}
    event_attributes = {}
    event_attribute_values = {}

    relation_qualifiers = _initiate_relation_qualifiers()
    event_to_object = {}
    object_to_object = {}
    event_to_object_attribute_value = {}

    ## Data extraction & mapping        (can be slow because of REST API rate limits)
    print(f"Starting extraction of object-centric event data from {max_issues} issues of repository {repo_owner}/{repo_name} using GitHub REST API via PyGitHub library.")
    print("While you wait, you can read about GitHub API rate limits here: https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api")

    # get list of issues
    issues = _get_issues(repo,num_issues=max_issues)
    num_issues = issues.totalCount # get actual number of issues

    print_counter = 0
    start_time = time.time()
    for issue in issues:
        issue_data = issue.raw_data
        issue_number = issue_data.get('number')

        # new "issue" object with attributes
        issue_object = _new_object_issue(issue_data,object_types,objects,object_attributes,object_attribute_values)

        # new "created" event
        created_event = _new_event_created(issue_data,event_types,events,event_attributes,event_attribute_values)

        # link "issue" object to "created" event
        link_create_to_issue = _link_event_to_object(created_event,issue_object,'created',"new issue created",relation_qualifiers,event_to_object)

        # get (or create) "user" object
        user_object = _get_object_user(issue_data.get("user"),existing_users,object_types,objects,object_attributes,object_attribute_values,GITHUB_ACCESS_TOKEN)

        # link "user" object to "created" event
        link_create_to_user = _link_event_to_object(created_event,user_object,'created',"new issue created by",relation_qualifiers,event_to_object)

        # link "user" object to "issue" object
        link_user_to_issue = _link_object_to_object(issue_object,user_object,created_event.timestamp,'created',"created by",relation_qualifiers,object_to_object)

        # get list of timeline events
        timeline = _get_events(issue)

        for timeline_event in timeline:
            timeline_event_data = timeline_event.raw_data

            # new event (type determined by timeline_event_data) and user data related to the event
            new_event,event_user_data = _new_timeline_event(issue_object,timeline_event_data,event_types,events,event_attributes,event_attribute_values,return_user_data=True)

            if new_event is not None:
                # link "issue" object to new event
                _link_event_to_object(new_event,issue_object,'timeline_event',new_event.event_type_description,relation_qualifiers,event_to_object)

                if new_event.event_type_description == "committed":
                    # create new commit object
                    commit_object = _new_object_commit(timeline_event_data,object_types,objects,object_attributes,object_attribute_values)

                    # link "commit" object to new event
                    _link_event_to_object(new_event,commit_object,'timeline_event',new_event.event_type_description,relation_qualifiers,event_to_object)

            for key,value in event_user_data.items():
                if value is not None:
                    if key in ('requested_team'): # user and team are different object types, but used similarly which is why they are lumped together as users here
                        event_user_object = _get_object_user(value,existing_users,object_types,objects,object_attributes,object_attribute_values,GITHUB_ACCESS_TOKEN,is_team=True)
                    else:
                        event_user_object = _get_object_user(value,existing_users,object_types,objects,object_attributes,object_attribute_values,GITHUB_ACCESS_TOKEN,is_team=False)
                    
                    if event_user_object is not None:
                        # link "event" to "user", using "key" as relation qualifier
                        _link_event_to_object(new_event,event_user_object,key,key,relation_qualifiers,event_to_object)

                        if key in ('requested_reviewer','requested_team') and new_event.event_type_description == 'review_requested':
                            # link "issue" to "user" as requested_reviewer/requested_team
                            _link_object_to_object(issue_object,event_user_object,new_event.timestamp,key,key,relation_qualifiers,object_to_object)
                        elif key in ('requested_reviewer','requested_team') and new_event.event_type_description == 'review_request_removed':
                            # remove "requested_reviewer"/"requested_team" link between "issue" and "user"
                            _link_object_to_object(issue_object,event_user_object,new_event.timestamp,key,None,relation_qualifiers,object_to_object)
                        elif key == 'assignee' and new_event.event_type_description == 'assigned':
                            # link "issue" to "user" as assignee
                            _link_object_to_object(issue_object,event_user_object,new_event.timestamp,key,key,relation_qualifiers,object_to_object)
                        elif key == 'assignee' and new_event.event_type_description == 'unassigned':
                            # remove "assignee" link between "issue" and "user"
                            _link_object_to_object(issue_object,event_user_object,new_event.timestamp,key,None,relation_qualifiers,object_to_object)


        # keep user informed about progress
        print_counter += 1
        perc_done = print_counter/num_issues
        seconds_done = time.time() - start_time
        print(f"    Extracting and mapping data for issue #{issue_number} done ...{round(100*perc_done,1)}% (about {round(seconds_done/perc_done - seconds_done,1)}s remaining)")

    ## Store the result
    print(f"Saving object-centric event data extracted from {repo_owner}/{repo_name} to DuckDB database file {quack_db}.")
    tables_to_store = [['object_types',object_types],
                    ['object_attributes',object_attributes],
                    ['objects',objects],
                    ['object_attribute_values',object_attribute_values],
                    ['event_types',event_types],
                    ['events',events],
                    ['event_attributes',event_attributes],
                    ['event_attribute_values',event_attribute_values],
                    ['relation_qualifiers',relation_qualifiers],
                    ['event_to_object',event_to_object],
                    ['object_to_object',object_to_object],
                    ['event_to_object_attribute_value',event_to_object_attribute_value],
                    ]

    for tbl in tables_to_store:
        _dataframe_to_persistent_duckdb(
            df_records=_extract_dataframe(tbl[1]),
            table_name=tbl[0],
            duckdb_file_name=quack_db
            )
        print(f"    Table {tbl[0]} ({len(tbl[1])} records) done.")
        
    print("All done!")
    return None
