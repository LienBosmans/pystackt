# PyStack't Documentation

PyStack't (`pip install pystackt`) is a Python package that supports data preparation for object-centric process mining. It covers extraction of object-centric event data, storage of that data, (visual) data exploration, and export to OCED formats.

[Source code](https://github.com/LienBosmans/pystackt) | [PyPi](https://pypi.org/project/pystackt/)


## Data Storage

PyStack't uses the Stack't relational schema to store object-centric event data. This schema was created specifically to support the data preparation stage, taking into account data engineering best practices. For more information on the design of Stack't, we recommend the paper [Dynamic and Scalable Data Preparation for Object-Centric Process Mining](https://arxiv.org/abs/2410.00596).

While any relational database can be used to store data in the Stack't relational schema, PyStack't uses [DuckDB](https://duckdb.org/) because it's open-source, fast and simple to use. (Think SQLite but for analytical workloads.)


## Data extraction

Extracting data from different systems is an important part of data preparation. While PyStack't does not include all functionality that a data stack offers (incremental ingests, scheduling refreshes, monitoring data pipelines...), it aims to provide simple-to-use methods to get real-life data for your object-centric process mining adventures.

### ⛏️ List of data extraction functionality
- [`get_github_log`](extract/get_github_log.md)


## Data export

The Stack't relational schema is intended as an intermediate storage hub. PyStack't provides export functionality to export the data to specific OCED formats that can be used by process mining applications and algorithms. This decoupled set-up has as main advantage that any future data source can be exported to all supported data formats, and any future OCED format can be combined with existing data extraction functionality.

### 📤 List of data export functionality
- [`export_to_ocel2`](export/export_to_ocel2.md)
- [`export_to_promg`](export/export_to_promg.md)


## Data exploration

Dispersing process data across multiple tables makes exploring object-centric event data less straightforward compared to traditional process mining. PyStack't aims to bridge this gap by providing dedicated data exploration functionality. Notably, the latest release includes an interactive data exploration app that runs locally and works out-of-the-box with any OCED data structured in the Stack't relational schema.

### 📈 List of data exploration functionality
- [`create_statistics_views`](exploration/create_statistics_views.md)
- [`interactive data visualization app`](exploration/interactive_data_visualization_app.md)
