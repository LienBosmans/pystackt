# ⛏️🐙 Extracting object-centric event logs from GitHub (`get_github_log`)

## 📝 Example
```python
from pystackt import *

get_github_log(
    GITHUB_ACCESS_TOKEN="insert_your_github_access_token_here",
    repo_owner="LienBosmans",
    repo_name="stack-t",
    max_issues=None,
    save_after_num_issues=1000,
    quack_db="./stackt.duckdb",
    schema="main"
)
```

| Parameter              | Type     | Description   |
|------------------------|----------|---------------|
| `GITHUB_ACCESS_TOKEN`  | `str`    | Personal GitHub personal access token for API authentication. |
| `repo_owner`           | `str`    | Owner of the GitHub repository from which to extract issue activity data. |
| `repo_name`            | `str`    | Name of the repository from which to extract issue activity data. |
| `max_issues`           | `int`    | Limits the number of issues to extract. If `None`, data for all closed issues will be collected. |
| `save_after_num_issues`| `int`    | Enables intermediate saving after processing this many issues. Prevents data loss from interruptions. Defaults to 5000. |
| `quack_db`             | `str`    | Path to the DuckDB file where data will be stored using the Stack’t relational schema. A new file is created if it doesn't exist yet. |
| `schema`               | `str`    | Name of the schema in the DuckDB database file where data will be written. If schema already exists, it will be cleared first. |


### Generating a GitHub Access Token (`GITHUB_ACCESS_TOKEN`)
To generate a GitHub access token, go to [GitHub Developer Settings](https://github.com/settings/tokens), click **"Generate new token (classic)"**, and proceed without selecting any scopes (leave all checkboxes unchecked). Copy the token and store it securely, as it won’t be shown again.

### GithHub Repository (`repo_owner`/`repo_name`)
These values are used to identify the GitHub repository from which the activity data will be extracted. You don't need to own or fork the repository. Permission to view the repository is sufficient, which is always the case for public repositories. If you want to extract data from a private repository, you'll need to create a different access token with a scope that includes read-only access to that repo.

### Maximum number of issues to return (`max_issues`)
Because of API rate limits, fetching all activity data from a repo can take a long time. This parameter controls the number of issues for which data will be collected. Setting it to a positive integer `n` will return data from the `n` most recent issues with status "closed". Setting it to `None` will return the activity data for all closed issues.

### Intermediate save functionality (`save_after_num_issues`)
To mitigate the risk of forced system restarts and GitHub API outages, intermediate save functionality was added. Setting it to a reasonable number such as 500 or 1000 does not impact total extraction times and greatly decreases potential disappointment. The default value is 5000.

### Output database file (`quack_db`) and schema (`schema`)
The extracted data will be stored in a DuckDB database using the Stack't relational schema. The tables will be stored in the given `schema`; the default schema is main. If the file does not exist yet, a new file will be created. Existing tables in `schema` will be overwritten.

To explore the data, you'll need a database manager. You can follow this [DuckDB guide](https://duckdb.org/docs/guides/sql_editors/dbeaver.html) to download and install **DBeaver** for easy access.  

## 🗺️ Extracted Data Overview

### Object Types  

| Object Type   | Description                               |
|---------------|-------------------------------------------|
| **Issue**     | Includes both pull requests and issues.   |
| **User**      | GitHub user accounts and commit authors.  |
| **Team**      | Represents GitHub teams.                  |
| **Commit**    | Represents individual commits.            |

> **Note:** Commits are often not linked to a GitHub user account. In such cases, the committer's name is used instead of an unique user ID, which may result in multiple user objects for the same person.  

### Object Attributes  

### Object Attributes  

| Object  | Attribute           | Description                                           |
|---------|---------------------|-------------------------------------------------------|
| Issue   | **number**          | Unique identifier for the issue or pull request.      |
| Issue   | **title**           | Title of the issue or pull request.                   |
| Issue   | **timeline_url**    | URL to the timeline of events related to the issue.   |
| User    | **id**              | Unique identifier for the user.                       |
| User    | **login**           | GitHub username of the user.                          |
| User    | **type**            | Type of user (e.g., "User" or "Bot").                 |
| User    | **url**             | URL to the user’s GitHub profile.                     |
| Team    | **slug**            | Unique team identifier (short name).                  |
| Team    | **name**            | Display name of the team.                             |
| Team    | **privacy**         | Team visibility setting (e.g., "secret" or "visible").|
| Team    | **url**             | URL to the team's GitHub page.                        |
| Commit  | **sha**             | Unique identifier (hash) of the commit.               |
| Commit  | **commit_message**  | Commit message describing the changes.                |
| Commit  | **url**             | URL to view the commit on GitHub.                     |



> **Note:** "Committers" do not have user attributes.  

### Event Types  

| Event Type    | Description       |
|---------------|-------------------|
| **All GitHub timeline events** (except `line-commented`)  | [See GithHub documentation for more details.](https://docs.github.com/en/rest/using-the-rest-api/issue-event-types) |
| **Created**   | For new issues.   |

### Event Attributes  

| Event Type        | Attribute                 | Description                           |
|-------------------|---------------------------|---------------------------------------|
| Timeline event    | **author_association**    | Only when available in API response.  |

### Event-to-Object Relations  

| Event                                         | Related Object    | Relation                  | Description                                           |
|-----------------------------------------------|-------------------|---------------------------|-------------------------------------------------------|
| Created                                       | Issue             | **created**               | An issue or pull request was created.                 | 
| Created                                       | User              | **created by**            | The user who created the issue or pull request.       |
| Timeline Event                                | User              | **actor**                 | The user who performed the action.                    |
| Review Requested, Review Request Removed      | User              | **requested_reviewer**    | A user was added or removed as a reviewer.            |
| Review Requested, Review Request Removed      | Team              | **requested_team**        | A team was added or removed as a reviewer.            |
| Assigned, Unassigned                          | User              | **assignee**              | A user was assigned to or unassigned from an issue.   |
| Committed                                     | Commit            | **committed**             | A commit was created.                                 |

> **Note:** actor is not available for the event type `committed`.  

### Object-to-Object Relations  

| Object    | Related Object    | Relation                  | Description                                           |
|-----------|-------------------|---------------------------|-------------------------------------------------------|
| Issue     | User              | **created by**            |                                                       |
| Issue     | User              | **requested_reviewer**    | dynamic, set to `null` when 'Review Request Removed'  |
| Issue     | Team              | **requested_team**        | dynamic, set to `null` when 'Review Request Removed'  |


For implementation details, you can check the documentation of the code itself in the [GitHub repository](https://github.com/LienBosmans/pystackt/tree/main/src/pystackt/extractors/github).

## 📜 Data Usage Policies
Please ensure that you extract and use the data in **compliance with GitHub policies**, including [Information Usage Restrictions](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies#7-information-usage-restrictions) and [API Terms](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service#h-api-terms).
