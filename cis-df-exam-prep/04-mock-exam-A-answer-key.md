# Mock Exam A - Answer Key

Score: ___ / 40 (28 = 70%). Misses by domain: Config __ Ingest __ Govern __ Insight __ CSDM __

| # | Domain | Answer | Why |
|---|---|---|---|
| 1 | Config | **C** | Add attributes at the most specific class that needs them, through Class Manager. |
| 2 | Config | **B** | e.g. `Depends on::Used by`, `Hosted on::Hosts`. |
| 3 | Config | **A** | Model categories map CI classes to asset classes. |
| 4 | Config | **A, C** | Table-per-class: inherited columns, one record, `sys_class_name` = most specific class. Custom classes can and should extend OOTB classes. |
| 5 | Config | **A** | Reuse before build. |
| 6 | Config | **B** | `discovery_source`; `correlation_id` is an external key, useful as an identifier attribute. |
| 7 | Ingest | **A** | Entries are evaluated in priority order and stop at the first match. |
| 8 | Ingest | **B** | Allow null attribute lets an empty value satisfy the entry. |
| 9 | Ingest | **A** | "Search on table" against a parent table finds the CI regardless of subclass. |
| 10 | Ingest | **B** | Inclusion rules narrow the candidate set (e.g. active CIs only). Health inclusion rules are a different thing in Health Preferences. |
| 11 | Ingest | **B** | Unregistered data sources are rejected. |
| 12 | Ingest | **A, C** | Classic transform maps bypass IRE unless scripted; IH-ETL is built around IRE. |
| 13 | Ingest | **A, C** | SGCs use IRE. A MID Server is needed only when the source is on-premises and unreachable from the instance. |
| 14 | Ingest | **B** | Identification succeeds; reconciliation blocks the unauthorised attribute. |
| 15 | Govern | **A, B, C** | Required field is Completeness; audit is Compliance. |
| 16 | Govern | **A** | Compliance = audit/desired-state results. |
| 17 | Govern | **A** | Scorecards hold the weights. |
| 18 | Govern | **C** | Delete CMDB related entry targets related records. |
| 19 | Govern | **B** | Retire, then archive, then delete, each with its own policy and retention period. |
| 20 | Govern | **B, C** | Standard lifecycle fields; install/operational status are legacy and kept in sync. |
| 21 | Govern | **B** | Inclusion rules scope which CIs are measured. Deleting data to fix a metric is never the answer. |
| 22 | Govern | **A** | Process owner / Configuration Manager. |
| 23 | Govern | **A, B** | Foundation domain data. |
| 24 | Govern | **A** | Remediation via Flow Designer. |
| 25 | Govern | **A** | Data Certification. |
| 26 | Govern | **A** | CSDM Data Foundations Dashboard reports adoption gaps per stage. |
| 27 | Govern | **B** | Register, define rules, approve, use certified tooling, test. |
| 28 | Govern | **A, B** | Completeness = required + recommended fields. |
| 29 | Insight | **A, B** | Saved queries drive CMDB Groups and multisource comparisons. |
| 30 | Insight | **A** | `cmdb_query_builder` (create/run); `cmdb_query_builder_read` runs only. |
| 31 | Insight | **A** | Dependency Views for impact. |
| 32 | Insight | **A** | No Multisource, no CMDB 360 data. |
| 33 | Insight | **A** | PA gives trends; the dashboard is a snapshot. |
| 34 | Insight | **A** | CMDB Workspace is the consolidated modern experience. |
| 35 | Insight | **A** | Service Mapping builds Application Service maps. |
| 36 | CSDM | **B, C** | Business Applications are portfolio records; infrastructure and outages attach to Application Services. |
| 37 | CSDM | **B** | Offering -> Service is the `parent` reference, not a relationship. |
| 38 | CSDM | **A** | Dynamic CI Group (query-based) under Technical Service Offerings. |
| 39 | CSDM | **B** | Ideation & Strategy. |
| 40 | CSDM | **B** | Walk = technical side; Run = business side. |
