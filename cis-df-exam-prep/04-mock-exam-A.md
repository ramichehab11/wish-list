# Mock Exam A (40 questions, 50 minutes)

Weighted to the blueprint: Configuration 6 · Ingest 8 · Govern 14 · Insight 7 · CSDM 5. Key in `04-mock-exam-A-answer-key.md`.

## Configuration

**1.** A customer wants to track a "patch cycle window" value for servers only, not for all hardware. Where should the
attribute be added?
A. `cmdb_ci`  B. `cmdb_ci_hardware`  C. `cmdb_ci_server`, via CI Class Manager  D. A new standalone table

**2.** What is the naming convention for relationship types?
A. `Child::Parent`  B. `Parent descriptor::Child descriptor`  C. `Type-Name`  D. `Source->Target`

**3.** What links a CI class to an asset class so that asset-CI synchronisation works?
A. Model category  B. Suggested relationship  C. Reconciliation rule  D. CMDB Group

**4.** Which two statements about CMDB class extension are true? (Choose 2)
A. A child class inherits all fields of its parent classes
B. A record is duplicated into each ancestor table
C. A record is stored once, with `sys_class_name` set to its most specific class
D. Custom classes cannot extend base-system classes

**5.** Before creating a custom class for a vendor product, what should you do first?
A. Check the existing hierarchy and the CMDB CI Class Models Store app for a suitable class
B. Create a `u_` table in System Definition
C. Extend `cmdb_ci` directly
D. Add the product to `cmdb_ci_service`

**6.** Which CI field records which integration or discovery source last updated the record?
A. `correlation_id`  B. `discovery_source`  C. `sys_updated_by`  D. `source_id`

## Ingest

**7.** A server class identification rule has entry 1 = serial number and entry 2 = name. A payload's serial matches CI
X and its name matches a different CI Y. What happens?
A. CI X is updated; entry 2 is never evaluated because entry 1 matched
B. A de-duplication task is created for X and Y
C. A new CI is created
D. CI Y is updated

**8.** Which identifier entry option can cause false matches when a source sends empty attribute values?
A. Enforce exact count match  B. Allow null attribute  C. Active  D. Search on table

**9.** A CI exists as `cmdb_ci_linux_server`. A new source sends the same serial number classified as
`cmdb_ci_server`. To avoid a duplicate, the identifier entry should...
A. use "Search on table" pointing at a parent table so subclasses are searched
B. have a lower priority
C. be marked dependent
D. allow null attributes

**10.** What do identification inclusion rules do?
A. Define required relationships for a class
B. Restrict which existing records IRE considers as match candidates
C. Set data source precedence
D. Define which CIs are included in health scoring

**11.** A payload is sent to `/api/now/identifyreconcile` with a data source value that is not registered in the
`discovery_source` choice list. What happens?
A. The source is created automatically  B. The request is rejected with an error
C. The source is recorded as "Other"  D. The CI is created but not reconciled

**12.** Which two statements are true when comparing IntegrationHub ETL with classic Import Set transform maps? (Choose 2)
A. IH-ETL uses the Robust Transform Engine and invokes IRE
B. Classic transform maps invoke IRE automatically
C. IH-ETL supports conditional class mapping and relationship mapping in a guided UI
D. IH-ETL requires custom scripting to identify CIs

**13.** Which two statements about Service Graph Connectors are true? (Choose 2)
A. They are ServiceNow-certified integrations distributed through the Store
B. They bypass IRE for performance
C. They are built on IntegrationHub ETL
D. They always require a MID Server

**14.** A reconciliation rule for `cmdb_ci_server` allows Discovery to update all attributes and SCCM to update only
`os_version`. SCCM sends a payload with a different `owned_by`. Result?
A. `owned_by` is updated from SCCM
B. The CI is identified; `owned_by` is not updated; `os_version` may update subject to precedence
C. The payload is rejected
D. A new CI is created

## Govern

**15.** Which three are Correctness metrics? (Choose 3)
A. Duplicate  B. Orphan  C. Stale  D. Required field  E. Audit

**16.** The Compliance KPI is derived from...
A. audit results against a desired state  B. required fields  C. relationship counts  D. discovery frequency

**17.** Where do you set how much each metric contributes to the overall health score?
A. Scorecards  B. Inclusion rules  C. Data Manager  D. Reconciliation rules

**18.** Which Data Manager policy type removes related records such as relationships rather than the CI itself?
A. Delete  B. Archive  C. Delete CMDB related entry  D. Retire

**19.** What is the recommended sequence for CI retention governance?
A. Delete -> Archive -> Retire  B. Retire -> Archive -> Delete  C. Archive -> Retire -> Delete  D. Any order

**20.** Which two fields define the standardised CI lifecycle? (Choose 2)
A. `install_status`  B. `life_cycle_stage`  C. `life_cycle_stage_status`  D. `operational_status`

**21.** Retired CIs are being counted as stale and dragging down a class's health score. Best fix?
A. Delete the retired CIs
B. Add an inclusion rule for the class that excludes retired CIs
C. Disable the staleness metric
D. Lower the staleness weight in the scorecard

**22.** Who is accountable for defining CMDB policies, standards and KPIs?
A. The Configuration Manager / Configuration Management process owner  B. The MID Server administrator
C. ITIL users  D. Platform developers

**23.** Which two are Foundation data that CMDB quality depends on? (Choose 2)
A. Location  B. Company  C. Incident category  D. Change template

**24.** CMDB Health remediation actions are implemented with...
A. Flow Designer flows and subflows triggered from health results  B. business rules only
C. transform maps  D. import sets

**25.** Which older feature schedules field-by-field record verification tasks for users?
A. Data Certification  B. CMDB 360  C. Query Builder  D. Data refresh rules

**26.** Business Applications exist but none is linked to an Application Service. Where is this surfaced as a CSDM
adoption gap?
A. CSDM Data Foundations Dashboard  B. CI Class Manager  C. The Compliance KPI  D. The MID Server dashboard

**27.** A team asks to feed a new tool's inventory into the CMDB. Which sequence follows governance best practice?
A. Point the tool at the `cmdb_ci` tables directly to save time
B. Register the discovery source, define reconciliation and precedence rules, obtain governance-board approval,
   implement with a Service Graph Connector or IH-ETL, test in sub-production
C. Let the team import an Excel file each month
D. Enable Multisource CMDB and let IRE sort it out

**28.** Which two field types contribute to a CI being counted as complete? (Choose 2)
A. Required fields  B. Recommended fields  C. Relationship fields  D. Audit fields

## Insight

**29.** Saved CMDB Query Builder queries can be used for which two purposes? (Choose 2)
A. Defining CMDB Group membership  B. Multisource comparisons across data sources
C. Defining reconciliation rules  D. Creating CI classes

**30.** Which role is required to create queries in CMDB Query Builder?
A. `cmdb_query_builder`  B. `itil`  C. `asset`  D. `cmdb_read`

**31.** A change manager wants to see everything upstream and downstream of a database CI before approving a change.
Which tool?
A. Dependency Views  B. Data Manager  C. Class Manager  D. Health Dashboard

**32.** CMDB 360 is blank for every CI. Most likely reason?
A. Multisource CMDB is not enabled  B. The user lacks the Query Builder role
C. Health jobs are inactive  D. Life-cycle rules are missing

**33.** Leadership wants a month-over-month trend of CMDB health. Which is the best source?
A. Performance Analytics indicators on the health KPIs  B. The Health Dashboard, which shows the current state only
C. CI Class Manager  D. CMDB 360

**34.** Which statement is true?
A. CMDB Workspace consolidates health, Data Manager, Query Builder, Class Manager and CMDB 360 in one experience
B. The classic CMDB Dashboard is the newest interface
C. CMDB Workspace is only for ITOM licensees
D. Query Builder is only available in the classic UI

**35.** Which view is produced by Service Mapping?
A. The Application Service map  B. The health scorecard  C. The class hierarchy  D. The precedence view

## CSDM

**36.** Which two statements about Business Applications are true? (Choose 2)
A. They are related directly to servers and databases
B. They are portfolio records owned through Application Portfolio Management
C. They relate to Application Services through a `Consumes::Consumed by` relationship
D. They are the CI referenced on outage incidents

**37.** How is a Service Offering linked to its Service?
A. A `Depends on::Used by` relationship  B. The `parent` reference field  C. `model_id`  D. A CMDB Group

**38.** Which construct represents infrastructure under a Technical Service Offering?
A. Dynamic CI Group  B. CMDB Group  C. Business Capability  D. Product Model

**39.** Which domain is new in CSDM 5?
A. Foundation  B. Ideation & Strategy  C. Service Consumption  D. Manage Portfolios

**40.** Which maturity stage adds Technical Services, Technical Service Offerings and Dynamic CI Groups?
A. Crawl  B. Walk  C. Run  D. Fly
