# PyStack't Data Extractors Overview

## ⛏️🐙 Extracting object-centric event logs from Github (`get_github_log`)

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

#### Generating a GitHub Access Token (`GITHUB_ACCESS_TOKEN`)
To generate a GitHub access token, go to [GitHub Developer Settings](https://github.com/settings/tokens), click **"Generate new token (classic)"**, and proceed without selecting any scopes (leave all checkboxes unchecked). Copy the token and store it securely, as it won’t be shown again.

#### RepoOwner/RepoName (`repo_owner`/`repo_name`)
These values are used to identify the GitHub repository from which the activity data will be extracted. You don't need to own or fork the repository. Permission to view the repository is sufficient, which is always the case for public repositories. If you want to extract data from a private repository, you'll need to create a different access token with a scope that includes read-only access to that repo.

#### Maximum number of issues to return (`max_issues`)
Because of API rate limits, fetching all activity data from a repo can take a long time. This parameter controls the number of issues for which data will be collected. Setting it to a positive integer `n` will return data from the `n` most recent issues with status "closed". Setting it to `None` will return the activity data for all closed issues.

#### Output database file (`quack_db`)
The extracted data will be stored in a DuckDB database using the Stack't relational schema. If the file does not exist yet, a new file will be created. Otherwise, existing tables in the `main` schema will be overwritten. (Currently data will always be written to the `main` schema. We plan to make the schema a parameter in a future release.)

To explore the data, you'll need a database manager. You can follow this [DuckDB guide](https://duckdb.org/docs/guides/sql_editors/dbeaver.html) to download and install **DBeaver** for easy access.  

### 📜 Data Usage Policies
Please ensure that you extract and use the data in **compliance with GitHub policies**, including [Information Usage Restrictions](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies#7-information-usage-restrictions) and [API Terms](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service#h-api-terms).
