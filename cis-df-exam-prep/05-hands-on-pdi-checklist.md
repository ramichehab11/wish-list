# Hands-on PDI Checklist (60-90 minutes)

Get a free Personal Developer Instance at developer.servicenow.com. Tick each item; the point is to have *seen* each
screen the exam names, not to build anything.

## Configuration (15 min)
- [ ] All > Configuration > CI Class Manager. Open **Server**: view Attributes, Identification Rule (note entry
      priorities and independent/dependent), Reconciliation Rules, Health, Suggested Relationships, Dependent
      Relationships, Model Category.
- [ ] Open **Network Adapter**: confirm its identification rule is dependent on Computer.
- [ ] Add a child class under Application via Class Manager (any name). Note what gets inherited.
- [ ] Open `cmdb_rel_type.list`: find `Depends on::Used by`, `Hosted on::Hosts`, `Consumes::Consumed by`.

## Ingest / IRE (20 min)
- [ ] CMDB Workspace > **IRE simulation** (or Scripts - Background) with this payload, run twice; second run should
      update, not insert:
      ```json
      {"items":[{"className":"cmdb_ci_linux_server","values":{"name":"cisdf-test-01","serial_number":"CISDF0001","os":"Linux Red Hat"}}]}
      ```
      Script form: `var r = new sn_cmdb.IdentificationEngine().createOrUpdateCI('ServiceNow', JSON.stringify(payload)); gs.info(r);`
- [ ] Send a Network Adapter item with no parent and read the error text (dependent identification).
- [ ] Configuration > Identification/Reconciliation > **Reconciliation Definitions**, **Data Source Precedences**,
      **Data Refresh Rules**: open one of each and read the fields.
- [ ] `sys_choice.list`, filter `element=discovery_source`: see the registered sources and the `SG-` prefix pattern.
- [ ] IntegrationHub ETL: open All > IntegrationHub ETL, start a new ETL definition against any import set table just
      to see the guided steps (Entities, Class mapping, Relationships, Test and rollback).

## Govern (25 min)
- [ ] Configuration > **Health Preference** (or CMDB Workspace > Health > Preferences): open Inclusion Rules,
      Required Fields, Recommended Fields, Orphan Rules, Staleness Rules, Scorecards.
- [ ] System Scheduler > Scheduled Jobs, search "CMDB Health": note they are inactive by default; activate the
      Completeness/Correctness/Compliance score calculations and run one.
- [ ] CMDB Workspace > **Data Manager**: create a Retire policy on a test class; observe the life-cycle rule
      requirement. Open **Life Cycle Rules** and activate one for the class, then re-save the policy.
- [ ] Open a CI and find **Life cycle stage** and **Life cycle stage status** on the form.
- [ ] CMDB Workspace > Health > look at duplicates and the remediation options (Duplicate CI Remediator).
- [ ] Create a CMDB Group from a saved Query Builder query and view health for it.

## Insight (15 min)
- [ ] CMDB Workspace > **Query Builder**: build "Application Service -> Depends on -> Linux Server", run it, save it.
- [ ] CMDB Workspace > **CMDB 360**: note it is empty; find the Multisource CMDB setting under
      Identification/Reconciliation properties and read its description.
- [ ] Open any server > Related Links > **Dependency Views** (or the map icon on the form).
- [ ] If the Store app is installable on your PDI, install "CMDB and CSDM Data Foundations Dashboard" and open it.

## CSDM (15 min)
- [ ] Create one Business Application, one Application Service (manual), one Business Service, one Business Service
      Offering (parent = the Business Service), one Technical Service, one Technical Service Offering.
- [ ] Relate Business Application -> Application Service (`Consumes::Consumed by`), Application Service -> a server
      (`Depends on::Used by`), Business Service Offering -> Application Service (`Depends on::Used by`).
- [ ] Open an Incident: set Service, Service offering and Configuration item and watch the reference qualifiers.
- [ ] Look at the class of each record you created and match it to the study guide table in section 6.3.
