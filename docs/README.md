# PyStack't Documentation

PyStack't (`pip install pystackt`) is a Python package that supports data preparation for object-centric process mining. It covers extraction of object-centric event data, storage of that data, and export to OCED formats.

[Source code](https://github.com/LienBosmans/pystackt) | [PyPi](https://pypi.org/project/pystackt/)


## Data Storage

PyStack't uses the Stack't relational schema to store object-centric event data. This schema was created specifically to support the data preparation stage, taking into account data engineering best practices. For more information on the design of Stack't, we recommend the paper [Dynamic and Scalable Data Preparation for Object-Centric Process Mining](https://arxiv.org/abs/2410.00596).

While any relational database can be used to store data in the Stack't relational schema, PyStack't uses [DuckDB](https://duckdb.org/) because it's open-source, fast and simple to use. (Think SQLite but for analytical workloads.)


## Data extraction

Extracting data from different systems is an important part of data preparation. While PyStack't does not support all functionality of a real data stack (incremental ingests, scheduling refreshes, monitoring data pipelines...), it aims to provide simple-to-use methods to get real-life data for your object-centric process mining adventures.

### ⛏️ List of data extraction functionality
- [`get_github_log`](extract/get_github_log.md)


## Data export

The Stack't relational schema is intended as an intermediate storage hub. PyStack't provides export functionality to export the data to specific OCED formats that can be used by process mining applications and algorithms. This decoupled set-up has as main advantage that any future data source can be exported to all supported data formats, and any future OCED format can be combined with existing data extraction functionality.

### 📤 List of data export functionality
- [`export_to_ocel2`](export/export_to_ocel2.md)
