# PyStack't (`pystackt`)
PyStack't (`pystackt`) is a Python package based on [Stack't](https://github.com/LienBosmans/stack-t) that supports data preparation for object-centric process mining.


## 📦 Installation  
You can install `pystackt` using pip:  

```sh
pip install pystackt
```

## 📖 Documentation  

Detailled documentation can be found here: [View PyStack't Documentation](https://lienbosmans.github.io/pystackt/)  

## 🔍 Viewing Data  
PyStack't creates **DuckDB database files**. To explore the data, you'll need a database manager. 
You can follow this [DuckDB guide](https://duckdb.org/docs/guides/sql_editors/dbeaver.html) to download and install **DBeaver** for easy access.


## 📝 Examples

### ⛏️🐙 Extract object-centric event log from GitHub repo ([`get_github_log`](docs/extract/get_github_log.md))
```python
from pystackt import *

get_github_log(
    GITHUB_ACCESS_TOKEN="insert_your_github_access_token_here",
    repo_owner="LienBosmans",
    repo_name="stack-t",
    max_issues=None, # None returns all issues, can also be set to an integer to extract a limited data set
    quack_db="./stackt.duckdb"
)
```

### 📤 Export to OCEL 2.0 ([`export_to_ocel2`](docs/export/export_to_ocel2.md))
```python
from pystackt import *

export_to_ocel2(
    quack_db="./stackt.duckdb",
    schema_in="main",
    schema_out="ocel2",
    sqlite_db="./ocel2_stackt.sqlite"
)
```
