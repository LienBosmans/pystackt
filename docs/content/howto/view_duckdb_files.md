# How to view DuckDB files?

When working with PyStack’t, event data is stored in a DuckDB file (e.g. `stackt.duckdb`) using the Stack’t relational schema.  
If you want to inspect the contents of such a file — for example to check tables, run queries, or verify data extraction — you have a few options.

## Option 1: Use the DuckDB UI extension

From DuckDB version 1.2.1 onwards, a [**UI extension**](https://duckdb.org/docs/stable/extensions/ui.html) is included. You can launch th extension by running below Python code.

```python
import duckdb

with duckdb.connect("./stackt.duckdb") as quack:
    quack.sql("CALL start_ui()")
    input("Press Enter to close the connection...")
```

This opens a web UI at http://localhost:4213 where you can browse tables and run SQL queries interactively.
Press Enter in your terminal to stop the session when you’re done.

## Option 2: Use a database manager

Follow this [DuckDB guide](https://duckdb.org/docs/guides/sql_editors/dbeaver.html) to download and install [DBeaver](https://dbeaver.io/about/) and use it to connect to your DuckDB file.
