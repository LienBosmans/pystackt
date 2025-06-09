# PyStack't Data Exporters Overview

## 📤 Export to OCEL 2.0

### 📝 Example
```python
from pystackt import *

export_to_ocel2(
    quack_db="./stackt.duckdb",
    schema_in="main",
    schema_out="ocel2",
    sqlite_db="./ocel2_stackt.sqlite"
)
```

#### Input data (`quack_db`,`schema_in`)
The input data for this function needs to be stored in a DuckDB database file using the Stack't relational schema. The path to the DuckDB file is defined in `quack_db`. The schema in which the data is stored is defined by `schema_in`.

#### Output data (`schema_out`,`sqlite_db`)
The output data in OCEL 2.0 format will be first written to the schema `schema_out` in `quack_db`. If this schema already exists, all existing tables in the schema will be deleted first.

Afterwards all tables in `schema_out` will be copied to a SQLite database file defined by `sqlite_db`. If the file does not exist yet, a new file will be created (**recommended**). Otherwise, existing tables will be overwritten. However, existing tables will not be deleted first, so if the new output uses different object/event types you should always create a new SQLite file!

### ⚠️ Information loss
Below is a list of information that is lost when exporting to OCEL 2.0.
- Since dynamic object-to-object relations are not supported by OCEL 2.0, only the first object-to-object relation qualifiers are used. Changes to object-to-object relations over time are therefore not exported.
- Since event-to-object-attribute-value relations are not supported by OCEL 2.0, they are not exported.

### ℹ️ More information on OCEL 2.0

- The OCEL 2.0 standard is defined in [OCEL (Object-Centric Event Log) 2.0 Specification](https://www.ocel-standard.org/2.0/ocel20_specification.pdf).
- To explore event logs in the **OCEL 2.0 format**, you can use [OCPQ](https://ocpq.aarkue.eu/) or [Ocelot](https://ocelot.pm/about).
