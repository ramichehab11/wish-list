#!/usr/bin/env python3
"""Clone every issue under a Jira epic into another (new or existing) epic.

Typical use: each product upgrade needs the same set of tracking issues, so a
"template" epic is kept and copied for every upgrade.

Talks to the Jira REST API v2 (``/rest/api/2``) and authenticates with a
Personal Access Token sent as ``Authorization: Bearer <token>``. Runs on
Python 3.8+ with the standard library only.

Examples
--------
Clone into a brand new epic, replacing the version string in summaries and
descriptions::

    export JIRA_BASE_URL=https://jira.example.com
    export JIRA_TOKEN=xxxxxxxx
    ./jira_clone_epic.py --source-epic PROJ-100 \
        --new-epic-summary "Upgrade to Vancouver" \
        --replace "Utah=Vancouver"

Clone into an epic that already exists::

    ./jira_clone_epic.py --source-epic PROJ-100 --target-epic PROJ-250

See what would happen without creating anything::

    ./jira_clone_epic.py --source-epic PROJ-100 --target-epic PROJ-250 --dry-run
"""

import argparse
import getpass
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

# Fields copied from every source issue (in addition to project/epic link).
CORE_FIELDS = ("summary", "description", "issuetype", "priority", "labels",
               "components", "fixVersions")

# Custom field types that must never be copied to a clone.
SKIPPED_CUSTOM_TYPES = (
    "com.pyxis.greenhopper.jira:gp-epic-link",
    "com.pyxis.greenhopper.jira:gp-epic-label",
    "com.pyxis.greenhopper.jira:gp-epic-status",
    "com.pyxis.greenhopper.jira:gp-epic-color",
    "com.pyxis.greenhopper.jira:gp-sprint",
    "com.pyxis.greenhopper.jira:gp-lexo-rank",
    "com.atlassian.jira.plugin.system.customfieldtypes:readonlyfield",
    "com.atlassian.jira.ext.charting:firstresponsedate",
    "com.atlassian.jira.ext.charting:timeinstatus",
    "com.atlassian.servicedesk:sd-request-participants",
    "com.atlassian.servicedesk:sd-sla-field",
)

SEARCH_PAGE_SIZE = 100


class JiraError(Exception):
    """Raised when Jira answers with an HTTP error."""

    def __init__(self, status, body, url):
        super().__init__("HTTP %s from %s: %s" % (status, url, body))
        self.status = status
        self.body = body


class Jira:
    """Minimal Jira REST API v2 client using a bearer token."""

    def __init__(self, base_url, token, ca_bundle=None, insecure=False):
        self.base_url = base_url.rstrip("/")
        self.token = token
        if insecure:
            self.ctx = ssl._create_unverified_context()  # noqa: SLF001
        elif ca_bundle:
            self.ctx = ssl.create_default_context(cafile=ca_bundle)
        else:
            self.ctx = ssl.create_default_context()

    def request(self, method, path, params=None, body=None):
        url = self.base_url + "/rest/api/2/" + path.lstrip("/")
        if params:
            url += "?" + urllib.parse.urlencode(params, doseq=True)
        data = None
        headers = {
            "Authorization": "Bearer " + self.token,
            "Accept": "application/json",
        }
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, context=self.ctx) as resp:
                raw = resp.read()
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", "replace")
            raise JiraError(exc.code, raw, url) from None
        if not raw:
            return None
        return json.loads(raw.decode("utf-8"))

    def get(self, path, params=None):
        return self.request("GET", path, params=params)

    def post(self, path, body):
        return self.request("POST", path, body=body)

    # -- higher level helpers -------------------------------------------------

    def myself(self):
        return self.get("myself")

    def get_issue(self, key, fields="*all"):
        return self.get("issue/" + key, params={"fields": fields})

    def search_all(self, jql, fields):
        """Yield every issue matching ``jql`` (handles pagination)."""
        start = 0
        while True:
            page = self.post("search", {
                "jql": jql,
                "startAt": start,
                "maxResults": SEARCH_PAGE_SIZE,
                "fields": fields,
            })
            issues = page.get("issues", [])
            for issue in issues:
                yield issue
            start += len(issues)
            if not issues or start >= page.get("total", 0):
                return

    def fields(self):
        return self.get("field")

    def create_meta_fields(self, project_key, issue_type_id):
        meta = self.get("issue/createmeta", params={
            "projectKeys": project_key,
            "issuetypeIds": issue_type_id,
            "expand": "projects.issuetypes.fields",
        })
        for project in meta.get("projects", []):
            for itype in project.get("issuetypes", []):
                if str(itype.get("id")) == str(issue_type_id):
                    return itype.get("fields", {})
        return {}

    def project_issue_types(self, project_key):
        return self.get("project/" + project_key).get("issueTypes", [])

    def create_issue(self, fields):
        return self.post("issue", {"fields": fields})


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def parse_replace(pairs):
    """Turn ``["old=new", ...]`` into a list of (old, new) tuples."""
    result = []
    for pair in pairs or []:
        if "=" not in pair:
            raise SystemExit("--replace expects OLD=NEW, got: %r" % pair)
        old, new = pair.split("=", 1)
        if not old:
            raise SystemExit("--replace OLD part must not be empty: %r" % pair)
        result.append((old, new))
    return result


def rewrite(text, replacements):
    if not text:
        return text
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def find_custom_fields(all_fields):
    """Locate Epic Link / Epic Name field ids and build id -> custom type map."""
    epic_link = epic_name = None
    custom_types = {}
    for field in all_fields:
        schema = field.get("schema") or {}
        custom = schema.get("custom")
        if custom:
            custom_types[field["id"]] = custom
        if custom == "com.pyxis.greenhopper.jira:gp-epic-link":
            epic_link = field["id"]
        elif custom == "com.pyxis.greenhopper.jira:gp-epic-label":
            epic_name = field["id"]
    return epic_link, epic_name, custom_types


def as_ref(value, keys=("id",)):
    """Reduce a Jira object (priority, component, ...) to its identifier."""
    if isinstance(value, dict):
        for key in keys:
            if key in value:
                return {key: value[key]}
    return value


def build_clone_fields(issue, target, epic_link_field, custom_types,
                       create_meta, replacements, skip_fields):
    """Build the create payload for a clone of ``issue`` under ``target``."""
    src = issue["fields"]
    project_key = src["project"]["key"]
    out = {
        "project": {"key": project_key},
        "issuetype": {"id": src["issuetype"]["id"]},
        "summary": rewrite(src.get("summary"), replacements),
    }
    if src.get("description"):
        out["description"] = rewrite(src["description"], replacements)
    if src.get("priority") and "priority" in create_meta:
        out["priority"] = as_ref(src["priority"])
    if src.get("labels") and "labels" in create_meta:
        out["labels"] = list(src["labels"])
    if src.get("components") and "components" in create_meta:
        out["components"] = [as_ref(c) for c in src["components"]]
    if src.get("fixVersions") and "fixVersions" in create_meta:
        out["fixVersions"] = [as_ref(v) for v in src["fixVersions"]]

    # Custom fields: only those present on the create screen, non-empty,
    # not agile/system bookkeeping fields and not explicitly skipped.
    extras = {}
    for field_id, value in src.items():
        if not field_id.startswith("customfield_") or value in (None, [], ""):
            continue
        if field_id in skip_fields or field_id not in create_meta:
            continue
        if custom_types.get(field_id) in SKIPPED_CUSTOM_TYPES:
            continue
        extras[field_id] = value

    # Attach to the epic: classic "Epic Link" if available, else parent.
    if epic_link_field:
        out[epic_link_field] = target
    else:
        out["parent"] = {"key": target}
    return out, extras


def create_with_fallback(jira, core, extras, key, log):
    """Create the issue with custom fields; on a 400 retry with core only."""
    if extras:
        try:
            return jira.create_issue(dict(core, **extras))
        except JiraError as exc:
            if exc.status != 400:
                raise
            log("  ! %s: Jira rejected custom fields (%s); retrying with core "
                "fields only" % (key, exc.body.strip()))
    return jira.create_issue(core)


def create_epic(jira, source_epic, summary, epic_name_field, replacements,
                project_key):
    """Create a new epic in ``project_key`` modelled on ``source_epic``."""
    epic_type = None
    for itype in jira.project_issue_types(project_key):
        if itype.get("name", "").lower() == "epic":
            epic_type = itype["id"]
            break
    if epic_type is None:
        raise SystemExit("Project %s has no 'Epic' issue type" % project_key)
    fields = {
        "project": {"key": project_key},
        "issuetype": {"id": epic_type},
        "summary": summary,
    }
    if epic_name_field:
        fields[epic_name_field] = summary
    description = source_epic["fields"].get("description")
    if description:
        fields["description"] = rewrite(description, replacements)
    return jira.create_issue(fields)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def parse_args(argv):
    p = argparse.ArgumentParser(
        description="Clone all issues under a Jira epic into another epic.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Examples")[1] if "Examples" in __doc__ else None,
    )
    p.add_argument("--base-url", default=os.environ.get("JIRA_BASE_URL"),
                   help="Jira base URL, e.g. https://jira.example.com "
                        "(env: JIRA_BASE_URL)")
    p.add_argument("--token", default=os.environ.get("JIRA_TOKEN"),
                   help="Personal Access Token (env: JIRA_TOKEN). If neither "
                        "is set you will be prompted.")
    p.add_argument("--source-epic", required=True, metavar="KEY",
                   help="Epic whose child issues are cloned")
    target = p.add_mutually_exclusive_group(required=True)
    target.add_argument("--target-epic", metavar="KEY",
                        help="Existing epic to clone the issues into")
    target.add_argument("--new-epic-summary", metavar="TEXT",
                        help="Create a new epic with this summary and clone "
                             "the issues into it")
    p.add_argument("--project", metavar="KEY",
                   help="Project for the new epic (default: source epic's "
                        "project)")
    p.add_argument("--replace", action="append", metavar="OLD=NEW",
                   help="Text replacement applied to summaries and "
                        "descriptions; may be given several times")
    p.add_argument("--skip-field", action="append", default=[],
                   metavar="customfield_NNNNN",
                   help="Custom field id that must not be copied; may be "
                        "given several times")
    p.add_argument("--jql-filter", metavar="JQL",
                   help="Extra JQL AND-ed to the child issue query, e.g. "
                        "'status != Cancelled'")
    p.add_argument("--dry-run", action="store_true",
                   help="Show what would be created without creating anything")
    p.add_argument("--ca-bundle", metavar="PATH",
                   help="CA certificate bundle for a self-signed Jira")
    p.add_argument("--insecure", action="store_true",
                   help="Disable TLS certificate verification (not advised)")
    args = p.parse_args(argv)
    if not args.base_url:
        p.error("--base-url or JIRA_BASE_URL is required")
    if not args.token:
        args.token = getpass.getpass("Jira personal access token: ")
    return args


def main(argv=None):
    args = parse_args(argv)
    replacements = parse_replace(args.replace)
    log = lambda msg: print(msg, file=sys.stderr)  # noqa: E731

    jira = Jira(args.base_url, args.token, args.ca_bundle, args.insecure)
    me = jira.myself()
    log("Authenticated as %s (%s)" % (me.get("displayName"), me.get("name")))

    epic_link_field, epic_name_field, custom_types = find_custom_fields(jira.fields())
    if epic_link_field:
        jql = '"Epic Link" = %s' % args.source_epic
    else:
        log("No 'Epic Link' field found; using parent relationship")
        jql = "parent = %s" % args.source_epic
    jql += " AND issuetype not in subTaskIssueTypes()"
    if args.jql_filter:
        jql += " AND (%s)" % args.jql_filter
    jql += " ORDER BY created ASC"

    source_epic = jira.get_issue(args.source_epic, fields="summary,description,project,issuetype")
    if source_epic["fields"]["issuetype"].get("name", "").lower() != "epic":
        log("Warning: %s is a %s, not an Epic" % (
            args.source_epic, source_epic["fields"]["issuetype"].get("name")))

    issues = list(jira.search_all(jql, ["*all"]))
    log("Found %d issue(s) under %s" % (len(issues), args.source_epic))
    if not issues:
        return 0

    # Resolve / create target epic.
    if args.target_epic:
        target_key = args.target_epic
        jira.get_issue(target_key, fields="summary")  # fail early if missing
    else:
        project_key = args.project or source_epic["fields"]["project"]["key"]
        summary = rewrite(args.new_epic_summary, replacements)
        if args.dry_run:
            target_key = "<new epic '%s' in %s>" % (summary, project_key)
            log("[dry-run] Would create epic %s" % target_key)
        else:
            created = create_epic(jira, source_epic, summary, epic_name_field,
                                  replacements, project_key)
            target_key = created["key"]
            log("Created epic %s: %s" % (target_key, summary))

    meta_cache = {}
    created_keys = []
    failures = 0
    for issue in issues:
        key = issue["key"]
        fields = issue["fields"]
        meta_key = (fields["project"]["key"], fields["issuetype"]["id"])
        if meta_key not in meta_cache:
            meta_cache[meta_key] = jira.create_meta_fields(*meta_key)
        core, extras = build_clone_fields(
            issue, target_key, epic_link_field, custom_types,
            meta_cache[meta_key], replacements, set(args.skip_field))
        if args.dry_run:
            log("[dry-run] %s -> %s: %s%s" % (
                key, fields["issuetype"]["name"], core["summary"],
                "  (+%d custom field(s))" % len(extras) if extras else ""))
            continue
        try:
            new = create_with_fallback(jira, core, extras, key, log)
        except JiraError as exc:
            failures += 1
            log("  x %s failed: HTTP %s %s" % (key, exc.status, exc.body.strip()))
            continue
        created_keys.append(new["key"])
        log("  %s -> %s: %s" % (key, new["key"], core["summary"]))

    if args.dry_run:
        log("[dry-run] %d issue(s) would be cloned into %s" % (len(issues), target_key))
        return 0
    log("Cloned %d issue(s) into %s%s" % (
        len(created_keys), target_key,
        "; %d failed" % failures if failures else ""))
    print(target_key)
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except JiraError as err:
        print("Error: %s" % err, file=sys.stderr)
        sys.exit(2)
    except (urllib.error.URLError, OSError) as err:
        print("Error: could not reach Jira: %s" % err, file=sys.stderr)
        sys.exit(2)
