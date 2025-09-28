# PyStack't Data Exporters Overview

## 📤 Export to PromG

> [!Warning]
> This feature is considered experimental. Expect significant changes to both the implementation and input parameters in future releases.

### 📝 Example
```python
from pystackt import *

export_to_promg(
    quack_db='./stackt.duckdb',
    schema_in='main',
    schema_out='promg',
    parent_folder='./promg_export',
    dataset_name="stackt"
)
```

| Parameter         | Type   | Description                                                  |
|-------------------|--------|--------------------------------------------------------------|
| `quack_db`        | `str`  | Path to the DuckDB database file containing the input data.  |
| `schema_in`       | `str`  | Name of the schema in the DuckDB file that contains the input data. Needs to be stored using in Stack't relational schema. |
| `schema_out`      | `str`  | Name of the schema where the PromG data tables will be created first. If schema already exists, it will be cleared first. |
| `parent_folder`   | `str`  | Path where a folder structure will be created to store exported data (CSV files), data structures (JSON file) and semantic header (JSON file). |
| `dataset_name`    | `str`  | Name to be used in the semantic header and folder structure of the exported PromG dataset. |

#### Input data (`quack_db`,`schema_in`)
The input data for this function needs to be stored in a DuckDB database file using the Stack't relational schema. The path to the DuckDB file is defined in `quack_db`. The schema in which the data is stored is defined by `schema_in`.

#### Output data (`schema_out`,`parent_folder`,`dataset_name`)
The output data that can be ingested by PromG will be first written to the schema `schema_out` in `quack_db`. If this schema already exists, all existing tables in the schema will be deleted first.

Afterwards all tables in `schema_out` will be copied as CSV files to a new folder structure created inside `parent_folder`. The `dataset_name` is used in the definition of the semantic header.


### ℹ️ About PromG

- PromG is an open-source tool that enables process analytics through Event Knowledge Graphs (EKG).
- Documentation, including tutorials for getting started, can be found here: https://promg-dev.github.io/promg-core/.
