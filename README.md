# PyStack't (`pystackt`)
PyStack't (`pystackt`) is a Python package based on [Stack't](https://github.com/LienBosmans/stack-t) that supports data preparation for object-centric process mining.


## 📦 Installation  
PyStack't is published on [PyPi](https://pypi.org/project/pystackt/) and can be installed using pip.  

```sh
pip install pystackt
```

## 📖 Documentation

-   [Extensive documentation](https://lienbosmans.github.io/pystackt/) is available via GitHub pages. 
-   A [demo video on Youtube](https://youtu.be/AS8wI90wRM8) can walk you throught the different functionalities.
-   Our BPM 2025 demo paper [PyStack't: Real-Life Data for Object-Centric Process Mining](https://ceur-ws.org/Vol-4032/paper-28.pdf) is available on CEUR.

## 📝 Examples

### ⛏️🐙 Extract object-centric event log from GitHub repo ([`get_github_log`](https://lienbosmans.github.io/pystackt/content/reference/extract/get_github_log.html)
```python
from pystackt import *

get_github_log(
    GITHUB_ACCESS_TOKEN="insert_your_github_access_token_here",
    repo_owner="LienBosmans",
    repo_name="stack-t",
    max_issues=None, # None returns all issues, can also be set to an integer to extract a limited data set
    quack_db="./stackt.duckdb",
    schema="main"
)
```

### 📈 Interactive data exploration ([`start_visualization_app`](https://lienbosmans.github.io/pystackt/content/reference/exploration/interactive_data_visualization_app.html))

```python
from pystackt import *

prepare_graph_data( # only needed once
    quack_db="./stackt.duckdb",
    schema_in="main",
    schema_out="graph_data_prep"
)

start_visualization_app(
    quack_db="./stackt.duckdb",
    schema="graph_data_prep"
)
```

### 📤 Export to OCEL 2.0 ([`export_to_ocel2`](https://lienbosmans.github.io/pystackt/content/reference/export/export_to_ocel2.html)
```python
from pystackt import *

export_to_ocel2(
    quack_db="./stackt.duckdb",
    schema_in="main",
    schema_out="ocel2",
    sqlite_db="./ocel2_stackt.sqlite"
)
```

## 👉 Contributing to PyStack't

We welcome any improvements, big and small, as well as new functionality that supports data preparation for object-centric process mining! For more information, please read the [Contributing Guide](https://github.com/LienBosmans/pystackt/blob/main/CONTRIBUTING.md).
