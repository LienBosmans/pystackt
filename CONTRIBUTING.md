# PyStack't (`pystackt`) Contributing Guide

First of all, thank you for considering to contribute to PyStack't! PyStack't is a Python package that supports data preparation for object-centric process mining. You can read about the different functionalities in the [documentation](https://lienbosmans.github.io/pystackt/). PyStack't is open source under the permissive [Apache-2.0 license](/LICENSE). Please note that any contributions you make to this [GitHub repository](https://github.com/LienBosmans/pystackt) will use the same license.

## Improve PyStack't

We welcome any improvements, big and small! This includes
-   Improving documentation: 
    -   fixing typos
    -   including links to compatible tools, methods, use-cases, ...
    -   adding more examples
    -   rewriting parts that are confusing, incomplete or unclear
    -   ...
-   Improving code: 
    -   code refactors that improve performance, readability  and/or re-usability
    -   code refactors that remove unnecessary external dependencies
    -   adding more and/or better error handling
    -   documentation: improving doc strings, adding useful in-line comments, ...
    -   adding extra data mapping for existing data sources, so richer datasets can be extracted
    -   ...


## Adding new functionality to PyStack't

Do you have an idea to extend PyStack't with extra functionality? Awesome! Please read below guidelines before creating that pull request.
-   We kindly ask to keep PyStack't focused on **data preparation** for **object-centric** process mining. For functionality that does not fit that purpose, we encourage you to create your own tool (software, application, Python package, script, ...) instead.
    -   When your tool is compatible with the Stack't relational schema or one of the data formats that PyStack't can export to, we welcome you to include a link in our documentation.
    -   When your tool uses a different **object-centric** data format that is not yet supported, we encourage you to contribute export functionality to that format. A link to your tool can then be included in the documentation of that function.
-   We try to limit the number of external dependencies.
    -   For performant data transformations, please use [DuckDB](https://duckdb.org/docs/stable/) (SQL) or [Polars](https://docs.pola.rs/) (DataFrame).
    -   For (interactive) visualizations, please use [Matplotlib](https://matplotlib.org/) or [Dash](https://dash.plotly.com/).
-   Every PyStack't function reads from or writes to a DuckDB database file that uses the Stack't relational schema. (more info below)
    -   New functionality must also be compatible with DuckDB files with the Stack't relational schema.
    -   If the Stack't relational schema does not fit your use-case, and you want to propose an improvement, please reach out to [Lien Bosmans](mailto:lienbosmans@live.com) before creating a pull request.


### Stack't relational schema

The Stack't relational schema describes how to store object-centric event data in a relational database using a fixed set of tables and table columns. This absence of any schema changes makes the format well-suited to act as a central data hub, enabling the modular design of PyStack't.

An overview of the tables and columns is included here. For more information on the design choices and the proof-of-concept implementation [Stack't](https://github.com/LienBosmans/stack-t), we recommend reading the paper [Dynamic and Scalable Data Preparation for Object-Centric Process Mining](https://arxiv.org/abs/2410.00596).

![PyStack't has a modular design.](/docs/pystackt_architecture.png)

**Event-related tables**. To maintain flexibility and support dynamic changes, event types and their attribute definitions are stored in rows rather than as table and column headers. This approach enables the use of the exact same tables across all processes, reducing the impact of schema modifications. Changing an event type involves updating foreign keys rather than moving data to different tables, and attributes can be added or removed without altering the schema.
- `event_types` contains an entry for each unique event type \
    Columns: 
    -   `id` is the primary key.
    -   `description` should be human-readable.
-   `event_attributes` stores entries for each unique event attribute. \
    Columns:
    -   `id` is the primary key.
    -   `event_type_id` is a foreign key referencing table `event_types`.
    -   `description` should be human-readable.
    -   `datatype` of the attribute (integer, varchar, timestamp, ...). of the attribute (integer, varchar, timestamp, ...).
-   `events` records details for each event \
    Columns:
    -   `id` is the primary key.
    -   `event_type_id` is a foreign key referencing table `event_types`.
    -   `timestamp`, preferably using UTC time zone.
    -   `description` should be human-readable.
-   `event_attribute_values` stores all attribute values for different events. This setup decouples events and their attributes by storing each attribute value in a new row, facilitating support for late-arriving data points. \
    Columns:
    -   `id` is the primary key.
    -   `event_id` is a foreign key referencing table `events`.
    -   `event_attribute_id` is a foreign key referencing table `event_attributes`.
    -   `attribute_value` is the value of the attribute that matches the datatype of the attribute.

**Object-related tables** also leverage row-based storage to manage attributes independently. This approach reduces the number of duplicate or NULL values significantly when attributes are updated asynchronously and frequently.
-   `object_types` records entries for each unique object type.\
    Columns:
    -   `id` is the primary key.
    -   `description` should be human-readable
-   `object_attributes` contains entries for each unique object attribute \
    Columns:
    -   `id` is the primary key.
    -   `object_type_id` is a foreign key referencing table `object_types`.
    -   `description` should be human-readable.
    -   `datatype` of the attribute (integer, varchar, timestamp, ...).
-   `object` stores details for each object.\
    Columns:
    -   `id` is the primary key.
    -   `object_type_id` is a foreign key referencing table `object_types`.
    -   `description` should be human-readable.
-   `object_attribute_values` records attribute values for objects.\
    Columns: 
    -   `id` is the primary key.
    -   `object_id` is a foreign key referencing table `objects`.
    -   `object_attribute_id` is a foreign key referencing table `object_attributes`.
    -   `timestamp` indicating when attribute updates, preferably using UTC time zone.
    -   `attribute_value` containing the updated value of the attribute. Should match the datatype of the attribute.

**Relation-related tables** serve as bridging tables to manage the different many-to-many relations between events and objects. The qualifier definitions are stored separately to minimize the impact of renaming them in case of changing business requirements 
-   `relation_qualifiers` stores qualifier definitions. In cases where relation qualifiers are not available in the source data, a dummy qualifier can be introduced.\ 
    Columns
    -   `id` is the primary key.
    -   `description` should be human-readable
    -   `datatype` of the attribute (integer, varchar, timestamp, ...).
-   `object_to_object` stores (dynamic) relations between objects.\
    Columns:
    -   `id` is the primary key.
    -   `source_object_id` is a foreign key referencing table `objects`.
    -   `target_object_id` is a foreign key referencing table `objects`.
    -   `timestamp` indicating the start when the relationship became active. To signify the end of an object-to-object relationship, a NULL value is used for the qualifier value, rather than an end timestamp. This design choice facilitates append-only data ingestion. Preferably using UTC time zone.
    -   `qualifier_id` is a foreign key referencing table `qualifiers`.
    -   `qualifier_value` provides additional relationship details.  Should match the datatype of the qualifier.
-   `event_to_object` stores relations between events and objects.\ 
    Columns:
    -   `id` is the primary key.
    -   `event_id` is a foreign key referencing table `events`.
    -   `object_id` is a foreign key referencing table `objects`.
    -   `qualifier_id` is a foreign key referencing table `qualifiers`.
    -   `qualifier_value` provides additional relationship details.  Should match the datatype of the qualifier.
-   `event_to_object_attribute_value` stores relations between events and changes to object attributes.\
    Columns:
    -   `id` is the primary key.
    -   `event_id` is a foreign key referencing table `events`.
    -   `object_attribute_value_id` is a foreign key referencing table `object_attribute_values`.
    -   `qualifier_id` is a foreign key referencing table `qualifiers`.
    -   `qualifier_value` provides additional relationship details. Should match the datatype of the qualifier.

### Data extractors

Example: GitHub extractor [ [code](/src/pystackt/extractors/github/) | [docs](/docs/extract/get_github_log.md) ]

1.  Choose a publicly available data source that contains real-life event data.
1.  Figure out how the source data is structured, how the API works, ...
1.  Map the data to the Stack't relational schema.
1.  Clean up your code. Save it in a new subfolder of [extractors](/src/pystackt/extractors/).
    -   Re-use existing functionality when possible.
    -   Write modular functions.
    -   Include error handling. 
    -   Use doc strings and in-line comments.
1.  Test your code.
1.  Write end-user documentation. Add it as a markdown file in the folder [extract](/docs/extract/). The documentation should include
    -   code snippet with example
    -   table that explains all parameters of the function
    -   how to generate credentials to connect to the data source
    -   description of which data will be extracted
    -   (link to) description of how the extracted data is allowed to be used


### Data exporters

Example: OCEL 2.0 [ [code](/src/pystackt/exporters/ocel2/) | [docs](/docs/export/export_to_ocel2.md) ]

Please note that the exported data format should be **object-centric** and **supported by at least one tool** (software, application, Python package, script, ...) that is open-source (*preferred*) or offers a free developper / student / personal license.

1.  Choose an object-centric event data format.
1.  Map the Stack't relational schema to your chosen data format.
1.  Clean up your code. Save it in a new subfolder of [exporters](/src/pystackt/exporters/).
    -   Re-use existing functionality when possible.
    -   Write modular functions.
    -   Include error handling. 
    -   Use doc strings and in-line comments.
1.  Test your code.
1.  Write end-user documentation. Add it as a markdown file in the folder [export](/docs/export/). The documentation should include
    -   code snippet with example
    -   table that explains all parameters of the function
    -   how to generate credentials to connect to the data source
    -   overview of any information loss that happens when exporting to this format
    -   link to additional information on the extracted format, tools that support it, ...

### Other functionality (data visualization, data manipulation, ...)

Data preparation is definitely more than simply extracting and exporting data, so we also welcome additional functionality that support things like data exploration, data cleaning, data filtering, ...

The previously discussed items still apply:
1.  Start from the Stack't relational schema in a DuckDB file.
    -   If the Stack't relational schema does not work with the application you have in mind, include a function to prepare the data first. ([example](/src/pystackt/exploration/graph/data_prep/))
1.  Clean up your code. Document your code. Test your code.
1.  Write end-user documentation.

## How to contribute?

Simply create a pull request (PR)! Some good practices to consider:
-   Give your PR a title and a description
-   If you make multiple unrelated changes, please create multiple PRs.
    -   Okay to combine: 
        -   new functionality and its documentation
        -   improved documentation for different functions
        -   code improvements (performance, readability) for different functions
    -   Should be split up: 
        -   new functionality + code improvements for existing functionality
        -   documentation of one function + code improvements of another function
-   Write meaningful commit messages. 
-   Don't combine unrelated changes in the same commit.
