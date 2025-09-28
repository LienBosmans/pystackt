# PyStack't Data Exploration

## 📊 Create Statistics Views

### 📝 Example
```python
from pystackt import *

create_statistics_views(
    quack_db="./stackt.duckdb",
    schema_in="main",
    schema_out="statistics"
)
```

| Parameter     | Type   | Description                                                  |
|---------------|--------|--------------------------------------------------------------|
| `quack_db`    | `str`  | Path to the DuckDB database file containing the input data.  |
| `schema_in`   | `str`  | Name of the schema in the DuckDB file that contains the input data. Needs to be stored using in Stack't relational schema. |
| `schema_out`  | `str`  | Name of the schema where the output SQL views will be created. If schema already exists, it will be cleared first. |


#### Input data (`quack_db`, `schema_in`)
The input data must be stored in a DuckDB database file using the Stack't relational schema. `quack_db` defines the path to this file, and `schema_in` specifies the schema containing the OCED data.

#### Output views (`schema_out`)
Two SQL views are created in the schema defined by `schema_out`. They contain some simple statistics that provide an excellent starting point to get to know the data.

- `event_stats`: provides summary statistics for each event type, including:
    - `first_event_timestamp` / `last_event_timestamp`: timestamp of the earliest/latest event recorded for this type
    - `event_count`: total number of events of this type
    - `event_attribute_count`: number of distinct attributes defined for this event type
    - `event_attribute_value_update_count`: number of times a value is recorded for these attributes across all events

- `object_stats`: provides summary statistics for each object type, including:
    - `first_object_update_timestamp` / `last_object_update_timestamp`: timestamps of the earliest/latest attribute value update recorded for objects of this type
    - `object_count`: number of distinct objects of this type
    - `object_attribute_count`: number of distinct attributes defined for this object type
    - `object_attribute_value_update_count`: number of attribute value updates recorded for objects of this type

If `schema_out` already exists, it will be cleared before the new views are created.

### 🔍 Viewing Data  
PyStack't creates **DuckDB database files**. From DuckDB version 1.2.1 onwards, you can explore them using the [**UI extension**](https://duckdb.org/docs/stable/extensions/ui.html). Below code will load the UI by navigating to `http://localhost:4213` in your default browser.

```python
import duckdb

with duckdb.connect("./stackt.duckdb") as quack:
    quack.sql("CALL start_ui()")
    input("Press Enter to close the connection...")
```

Alternatively, you can use a database manager. You can follow this [DuckDB guide](https://duckdb.org/docs/guides/sql_editors/dbeaver.html) to download and install **DBeaver** for easy access.
