# Tutorial: Extracting your first object-centric event log from a GitHub repository

In this tutorial, you’ll extract an **object-centric event log** from a real GitHub repository. You don’t need to know much about process mining or GitHub yet — we’ll walk through it step by step.  

By the end, you will:
- Install and use **PyStack’t**, a Python library for extracting object-centric event data.
- Create a GitHub personal access token.
- Extract event data from a repository.
- Export the data into the OCEL 2.0 format.
- Load the resulting log into Ocelot, a tool for analyzing object-centric logs.

Let’s get started!

# Prerequisites

Before we begin, make sure you have the following:

-   **Python 3.12 or higher** installed on your computer.  
    You can check this by running `python --version` in your terminal.  
    If you don’t have it yet, download and install it from [python.org](https://www.python.org/downloads/).  

-   A **GitHub account**.  
    If you don’t already have one, you can create it for free at [github.com](https://github.com/).  
    We’ll need it to generate an access token later.  

With these in place, you’re ready to proceed.

# Install PyStack't

First, we need to install the library we’ll be using: **PyStack’t**.  
Open a terminal (or command prompt) and run:

```sh
pip install pystackt
```

This will download and install the package from PyPI.
If you see errors about pip not being found, try running `python -m pip install pystackt` instead.

Once installed, you can test it worked by running:

```sh
python -c "import pystackt; print('PyStackt is installed!')"
```

If you see the confirmation message, you’re ready to move on.

# Generate GitHub access token

PyStack’t needs permission to read from GitHub repositories. For this, we use a personal access token.
1.  Log in to your [GitHub account](https://github.com/).
1.  Go to [GitHub Developer Settings](https://github.com/settings/tokens).
1.  Click "Generate new token (classic)".
1.  Don’t select any scopes (leave all checkboxes unchecked).
1.  Generate the token and copy it. GitHub will only show it once, so store it somewhere safe. We’ll use this token in the next step.
    -   If you lose your token, you can always generate a new one.
    -   If you accidently share your token, for example by comitting it to Git, it's good practice to delete it and generate a new token.

# Extract object-centric event data from GitHub repository

Now let’s extract event data from a real repository.

Open a Python file (for example `extract_log.py`) or a Jupyter Notebook, and paste in the following code:

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

👉 Replace `insert_your_github_access_token_here` with the token you generated earlier.

When you run this code, PyStack’t will connect to GitHub, fetch issue and pull request data from the [stackt-t repository](https://github.com/LienBosmans/stack-t), and store it locally in a DuckDB database file called `stackt.duckdb`.

# Export to OCEL 2.0

Now that the raw data is stored, let’s export it into the OCEL 2.0 format. This is a common format for object-centric event logs.

Add the following code to your script or notebook:

```python
export_to_ocel2(
    quack_db="./stackt.duckdb",
    schema_in="main",
    schema_out="ocel2",
    sqlite_db="./ocel2_stackt.sqlite"
)
```

This will create a new SQLite database file called `ocel2_stackt.sqlite` that contains the event log in OCEL 2.0 format.
You now have a portable log that can be used in other analysis tools.

# Load OCEL 2.0 log in Ocelot

Finally, let’s open the log in the analysis tool Ocelot.
1.  Go to [https://ocelot.pm/](https://ocelot.pm/)
1.  Drag and drop `ocel2_stackt.sqlite` in the Event Log Import window.
1.  You should now see the object-centric event log extracted from the GitHub repository! 🎉
