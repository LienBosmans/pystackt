# PyStack't (`pystackt`)
PyStack't (`pystackt`) is a Python package based on [Stack't](https://github.com/LienBosmans/stack-t). 

While Stack't is a proof-of-concept on how to embed the data transformations needed for object-centric process mining into an (existing) data stack, it's not very user-friendly for ad-hoc use. PyStack't aims to fill that gap by exposing some functionality in a Python package.

- In this first release, only the Github log extractor is included. The log will be written to a database (DuckDB) using the Stack't relational schema.
- In next releases, data exporters to OCED formats (f.e. OCEL 2.0) will be added.

## 📦 Installation  
You can install `pystackt` using pip:  

```sh
pip install pystackt
```


## ⛏️🐙 Extracting object-centric event log from Github

### 📝 Example
```python
from pystackt import *

get_github_log(
    GITHUB_ACCESS_TOKEN="insert_your_github_access_token_here",
    repo_owner="LienBosmans",
    repo_name="stack-t",
    max_issues=None,
    quack_db="./stack-t.duckdb"
)
```

### 🔑 Generating a GitHub Access Token  
To generate a GitHub access token, go to [GitHub Developer Settings](https://github.com/settings/tokens), click **"Generate new token (classic)"**, and proceed without selecting any scopes (leave all checkboxes unchecked). Copy the token and store it securely, as it won’t be shown again.

### 🔍 Viewing Data  
This function creates a **DuckDB database file**. To explore the data, you'll need a database manager.  

You can follow this [DuckDB guide](https://duckdb.org/docs/guides/sql_editors/dbeaver.html) to download and install **DBeaver** for easy access.  
