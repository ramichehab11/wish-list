# jira_clone_epic.py

Clones every issue under a Jira epic into another epic. Keep one "template"
epic with the standard upgrade issues and copy it for each new upgrade.

* Jira REST API v2 (`/rest/api/2`), Jira Server / Data Center.
* Authentication: Personal Access Token sent as `Authorization: Bearer`.
* Python 3.8+, standard library only.

## Setup

```bash
export JIRA_BASE_URL=https://jira.example.com
export JIRA_TOKEN=<personal access token>
```

If `JIRA_TOKEN` is not set the script prompts for it (never echoed).

## Usage

Clone into a new epic, swapping the release name everywhere:

```bash
python3 scripts/jira_clone_epic.py --source-epic PROJ-100 \
    --new-epic-summary "Upgrade to Vancouver" \
    --replace "Utah=Vancouver"
```

Clone into an epic that already exists:

```bash
python3 scripts/jira_clone_epic.py --source-epic PROJ-100 --target-epic PROJ-250
```

Preview without creating anything:

```bash
python3 scripts/jira_clone_epic.py --source-epic PROJ-100 --target-epic PROJ-250 --dry-run
```

The key of the target epic is printed on stdout; progress goes to stderr.

## What is copied

Summary, description, issue type, priority, labels, components and fix
versions, plus custom fields that are on the create screen of the issue type.
Sprint, rank, epic and other agile bookkeeping fields are never copied. If Jira
rejects a clone because of a custom field, the issue is retried with the core
fields only and a warning is printed. Use `--skip-field customfield_NNNNN` to
exclude a field explicitly.

Not copied: sub-tasks, assignee, reporter, status, comments, attachments,
issue links and watchers. Clones are created in the source issue's project.

## Options

| Option | Purpose |
| --- | --- |
| `--source-epic KEY` | Epic whose child issues are cloned (required) |
| `--target-epic KEY` | Existing epic to clone into |
| `--new-epic-summary TEXT` | Create a new epic with this summary and clone into it |
| `--project KEY` | Project for the new epic (default: source epic's project) |
| `--replace OLD=NEW` | Text replacement for summaries and descriptions, repeatable |
| `--skip-field ID` | Custom field id not to copy, repeatable |
| `--jql-filter JQL` | Extra JQL to narrow the child issues, e.g. `status != Cancelled` |
| `--dry-run` | Show what would be created |
| `--ca-bundle PATH` | CA bundle for a self-signed Jira certificate |
| `--insecure` | Skip TLS verification (not advised) |

Exit code is 0 on success, 1 if some issues failed to clone, 2 on a Jira or
connection error.
