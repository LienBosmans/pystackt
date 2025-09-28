# 🗺️ Overview of `get_github_log` output

## Object Types  

| Object Type   | Description                               |
|---------------|-------------------------------------------|
| **Issue**     | Includes both pull requests and issues.   |
| **User**      | GitHub user accounts and commit authors.  |
| **Team**      | Represents GitHub teams.                  |
| **Commit**    | Represents individual commits.            |

> **Note:** Commits are often not linked to a GitHub user account. In such cases, the committer's name is used instead of an unique user ID, which may result in multiple user objects for the same person.  

## Object Attributes  

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

## Event Types  

| Event Type    | Description       |
|---------------|-------------------|
| **All GitHub timeline events** (except `line-commented`)  | [See GithHub documentation for more details.](https://docs.github.com/en/rest/using-the-rest-api/issue-event-types) |
| **Created**   | For new issues.   |

## Event Attributes  

| Event Type        | Attribute                 | Description                           |
|-------------------|---------------------------|---------------------------------------|
| Timeline event    | **author_association**    | Only when available in API response.  |

## Event-to-Object Relations  

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

## Object-to-Object Relations  

| Object    | Related Object    | Relation                  | Description                                           |
|-----------|-------------------|---------------------------|-------------------------------------------------------|
| Issue     | User              | **created by**            |                                                       |
| Issue     | User              | **requested_reviewer**    | dynamic, set to `null` when 'Review Request Removed'  |
| Issue     | Team              | **requested_team**        | dynamic, set to `null` when 'Review Request Removed'  |


For implementation details, you can check the documentation of the code itself in the [GitHub repository](https://github.com/LienBosmans/pystackt/tree/main/src/pystackt/extractors/github).
