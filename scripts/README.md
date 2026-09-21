# jira_clone_epic.py

Clones every issue under a Jira epic into another epic. Keep one "template"
epic with the standard upgrade issues and copy it for each new upgrade.

* Jira REST API v2 (`/rest/api/2`), Jira Server / Data Center.
* Authentication: Personal Access Token sent as `Authorization: Bearer`.
* Python 3.8+, standard library only.

## Setup

Credentials are read from a `.env` file:

```bash
cp scripts/.env.example scripts/.env
# edit scripts/.env and set JIRA_BASE_URL and JIRA_TOKEN
```

The script looks for `.env` in the current directory first, then next to
the script. Use `--env-file PATH` to point at another file. Variables already
present in the environment take precedence over the file, and `.env` is
listed in `.gitignore` so it is never committed. If `JIRA_TOKEN` is still
unset the script prompts for it (never echoed).

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

## Epic link detection

Jira Server/DC attaches issues to an epic through the "Epic Link" custom
field. The script finds it in this order:

1. `--epic-link-field` if given, matched against the field id
   (`customfield_10014`) or the display name (`"Epic Link"`, case-insensitive).
2. A field whose type is `com.pyxis.greenhopper.jira:gp-epic-link`.
3. A field named "Epic Link" or "Epic".
4. Otherwise the `parent` relationship is used.

The chosen field is printed at startup. To see what your Jira exposes:

```bash
python3 scripts/jira_clone_epic.py --list-fields          # fields matching "epic"
python3 scripts/jira_clone_epic.py --list-fields sprint   # any other text
python3 scripts/jira_clone_epic.py --list-fields ""       # every field
```

If the field is missing from that list, the token's user cannot see it.
Check the field's context and screen configuration in Jira, or confirm the
id from a known child issue:

```bash
curl -s -H "Authorization: Bearer $JIRA_TOKEN" \
  "$JIRA_BASE_URL/rest/api/2/issue/PROJ-101?fields=*all" | grep -o '"customfield_[0-9]*":"PROJ-100"'
```

Then pass it explicitly: `--epic-link-field customfield_10014`.

## Options

| Option | Purpose |
| --- | --- |
| `--env-file PATH` | `.env` file to load (default: `./.env`, then the script's directory) |
| `--epic-link-field ID_OR_NAME` | Field linking issues to their epic, by id or display name |
| `--epic-name-field ID_OR_NAME` | Field holding the name of a newly created epic |
| `--list-fields [TEXT]` | Print fields whose id, name or type contains TEXT (default `epic`) and exit |
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
