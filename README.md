# PyStack't (`pystackt`)
PyStack't (`pystackt`) is a Python package based on [Stack't](https://github.com/LienBosmans/stack-t) that supports data preparation for object-centric process mining.

While Stack't is a proof-of-concept on how to embed the data transformations needed for object-centric process mining into an (existing) data stack, it's not very user-friendly for ad-hoc use. PyStack't aims to fill that gap by exposing some functionality in a Python package.


## 📦 Installation  
You can install `pystackt` using pip:  

```sh
pip install pystackt
```

## 📖 Documentation  

Detailled documentation can be found here: [View PyStack't Documentation](https://lienbosmans.github.io/pystackt/)  


## ⛏️🐙 Extracting object-centric event logs from Github

### 📝 Example
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

### 🔑 Generating a GitHub Access Token  
To generate a GitHub access token, go to [GitHub Developer Settings](https://github.com/settings/tokens), click **"Generate new token (classic)"**, and proceed without selecting any scopes (leave all checkboxes unchecked). Copy the token and store it securely, as it won’t be shown again.

### 🔍 Viewing Data  
This function creates a **DuckDB database file**. To explore the data, you'll need a database manager. 
You can follow this [DuckDB guide](https://duckdb.org/docs/guides/sql_editors/dbeaver.html) to download and install **DBeaver** for easy access.  

### 📜 Data Usage Policies
Please ensure that you use the extracted data in **compliance with GitHub policies**, including [Information Usage Restrictions](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies#7-information-usage-restrictions) and [API Terms](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service#h-api-terms).


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

### ℹ️ More information 

- The OCEL 2.0 standard is defined in [OCEL (Object-Centric Event Log) 2.0 Specification](https://www.ocel-standard.org/2.0/ocel20_specification.pdf).
- To explore event logs in the **OCEL 2.0 format**, you can use [Ocelot](https://ocelot.pm/about).
