# PyStack't (`pystackt`) Contributing Guide

First of all, thank you for considering to contribute to PyStack't! 

PyStack't is a Python package that supports data preparation for object-centric process mining. You can read about the different functionalities in its [documentation](https://lienbosmans.github.io/pystackt/). 

PyStack't is open-source under the permissive [Apache-2.0 license](/LICENSE). Please note that any contributions you make to the [PyStack't GitHub repository](https://github.com/LienBosmans/pystackt), will use the same license.

## Improving PyStack't

We welcome any improvements, big and small!
-   Improving documentation: 
    -   fixing typos
    -   including links to compatible tools, methods, use-cases, ...
    -   adding more examples
    -   rewriting parts that are confusing, incomplete or unclear
    -   ...
-   Improving code: 
    -   code refactors that improve performance, readability and/or re-usability
    -   code refactors that remove unnecessary external dependencies
    -   adding more and/or better error handling
    -   improving doc strings, adding useful in-line comments, ...
    -   adding extra data mapping for existing data sources (so richer datasets can be extracted)
    -   ...


## Adding new functionality to PyStack't

Do you have an idea to extend PyStack't with extra functionality? Awesome! Please read below guidelines before creating that pull request.
-   We kindly ask to keep PyStack't focused on **data preparation** for **object-centric** process mining. For functionality that does not fit that purpose, we encourage you to create your own tool (software, application, Python package, script, ...) instead.
    -   When your tool is compatible with the Stack't relational schema or one of the data formats that PyStack't can export to, we welcome you to add a link in our documentation.
    -   When your tool uses a different **object-centric** data format that is not yet supported, we encourage you to contribute export functionality to that format. A link to your tool can then be included in the documentation of this new function.
-   We try to limit the number of external dependencies.
    -   For performant data transformations, please use [DuckDB](https://duckdb.org/docs/stable/) (SQL) or [Polars](https://docs.pola.rs/) (DataFrame).
    -   For (interactive) visualizations, please use [Matplotlib](https://matplotlib.org/) or [Dash](https://dash.plotly.com/).
-   Every PyStack't function reads from or writes to a DuckDB database file that uses the [Stack't relational schema](/docs/content/explained/pystackt_design.md).
    -   New functionality must also be compatible with DuckDB files with the Stack't relational schema.
    -   If the Stack't relational schema does not fit your use-case, and you want to propose an improvement, please reach out directly to [Lien Bosmans](mailto:lienbosmans@live.com).


### Data extractors

Example: GitHub extractor [ [code](/src/pystackt/extractors/github/) | [docs](/docs/extract/get_github_log.md) ]

What is expected:
1.  Choose a publicly available data source that contains real-life event data.
1.  Figure out how the source data is structured, how the API works, ...
1.  Map the data to the [Stack't relational schema](/docs/content/explained/pystackt_design.md).
1.  Clean up your code. Save it in a new subfolder of [/src/pystackt/extractors/](/src/pystackt/extractors/).
    -   Re-use existing functionality when possible.
    -   Write modular functions.
    -   Include error handling. 
    -   Use doc strings and in-line comments.
1.  Test your code.
1.  Write end-user documentation. Add it as a markdown file in the folder [/docs/extract/](/docs/extract/). The documentation should include
    -   code snippet with example
    -   table that explains all parameters of the function
    -   explanation on how to generate credentials to connect to the data source (if relevant)
    -   description of which data is extracted
    -   (link to) explanation of how the extracted data is allowed to be used


### Data exporters

Example: OCEL 2.0 [ [code](/src/pystackt/exporters/ocel2/) | [docs](/docs/export/export_to_ocel2.md) ]

Please note that the exported data format should be **object-centric** and **supported by at least one tool** (software, application, Python package, script, ...) that is open-source (*preferred*) or offers a free license for developpers / students / personal use.

What is expected:
1.  Choose an object-centric event data format.
1.  Map the [Stack't relational schema](/docs/content/explained/pystackt_design.md) to your chosen data format.
1.  Clean up your code. Save it in a new subfolder of [/src/pystackt/exporters/](/src/pystackt/exporters/).
    -   Re-use existing functionality when possible.
    -   Write modular functions.
    -   Include error handling. 
    -   Use doc strings and in-line comments.
1.  Test your code.
1.  Write end-user documentation. Add it as a markdown file in the folder [/docs/export/](/docs/export/). The documentation should include
    -   code snippet with example
    -   table that explains all parameters of the function
    -   overview of any information loss that happens when exporting to this format
    -   link to additional information on the extracted format, tools that support this format, ...

### Other functionality (data visualization, data manipulation, ...)

Data preparation is definitely more than simply extracting and exporting data, so we also welcome additional functionality that support activities like data exploration, data cleaning, data filtering, ...

The previously discussed items still apply:
1.  Start from the [Stack't relational schema](/docs/content/explained/pystackt_design.md) in a DuckDB file.
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
-   Don't combine independent changes in the same commit.
