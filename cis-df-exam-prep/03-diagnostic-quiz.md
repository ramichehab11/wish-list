# Diagnostic Quiz (30 questions, 35 minutes, no notes)

Weighted like the exam: Configuration 5 · Ingest 6 · Govern 10 · Insight 4 · CSDM 5.
Write answers as `1-B, 2-AC, ...` and grade with `03-diagnostic-answer-key.md`. Tag each miss with its domain.

## Configuration

**1.** Which table stores the relationships between two CIs?
A. `cmdb_rel_type`  B. `cmdb_rel_ci`  C. `cmdb_ci_rel`  D. `cmdb_relationship`

**2.** A customer needs a CI class for an in-house application component that runs on servers. What is the best
approach?
A. Create a new table directly under `cmdb_ci` in System Definition > Tables
B. Use CI Class Manager to create a class that extends `cmdb_ci_appl`
C. Add the component's fields to `cmdb_ci`
D. Store the components as records in `cmdb_ci_service`

**3.** An Application Service is the parent and a Linux server is the child in a `Depends on::Used by` relationship.
Which statement is true?
A. The server depends on the Application Service
B. The Application Service depends on the server, and the server is used by the Application Service
C. That relationship type is invalid for services
D. Direction has no meaning in `cmdb_rel_ci`

**4.** Which two items are configured in CI Class Manager? (Choose 2)
A. Identification rules  B. Data Manager policies  C. Suggested relationships  D. The health score calculation schedule

**5.** How is a CI linked to its Product Model?
A. A `cmdb_rel_ci` relationship  B. The `model_id` reference field on the CI
C. Only through the model category  D. Product Models are CIs that extend `cmdb_ci`

## Ingest

**6.** During identification, an identifier entry matches two existing CIs. What does IRE do?
A. Creates a new CI  B. Updates both CIs
C. Creates a de-duplication task and does not create a new CI  D. Deletes the older CI

**7.** A payload contains a Network Adapter but no host computer and no relationship. What happens?
A. It is inserted as an independent CI
B. IRE returns an error and the adapter is not inserted, because the class uses dependent identification
C. It is inserted under a generic placeholder parent
D. It is held in a staging table for review

**8.** SCCM should be allowed to update a server's attributes only if Discovery has not updated them for 30 days.
What do you configure?
A. A reconciliation rule  B. A data refresh rule  C. A CMDB Health staleness rule  D. An identification inclusion rule

**9.** A vendor tool has a ServiceNow Store integration available. Which ingestion method should be chosen first?
A. A custom Import Set transform map  B. IntegrationHub ETL  C. The Service Graph Connector  D. A scripted GlideRecord insert

**10.** Data source precedence for an attribute is Discovery = 100, SCCM = 200, Manual = 300. All three provide a
value. Whose value remains on the CI?
A. Manual (300)  B. SCCM (200)  C. Discovery (100)  D. Whichever wrote last

**11.** Which two statements about Multisource CMDB are true? (Choose 2)
A. It is enabled by default
B. It stores the value each source reported for each attribute
C. It is required for CMDB 360 to show data
D. It replaces reconciliation rules

## Govern

**12.** Which three are CMDB Health KPIs? (Choose 3)
A. Completeness  B. Consistency  C. Correctness  D. Compliance  E. Coverage

**13.** An orphan CI is a CI that...
A. has no owner  B. has no relationships to other CIs  C. has not been updated in 30 days  D. has a duplicate

**14.** Which three are CMDB Data Manager policy types? (Choose 3)
A. Retire  B. Reconcile  C. Archive  D. Attestation  E. Discover

**15.** A Data Manager Retire policy cannot run. What is the most likely cause?
A. No reconciliation rule exists for the class
B. No active life-cycle rule exists for a class in the policy's scope
C. Multisource CMDB is disabled
D. Health jobs are disabled

**16.** The Completeness KPI measures...
A. whether required and recommended fields are populated  B. whether relationships exist
C. whether audits passed  D. how many data sources update the CI

**17.** The Health Dashboard reports zero duplicates for a class you know contains duplicates. Most likely reason?
A. Health jobs run too often
B. The class identification rule is weak or does not use attributes the sources populate
C. Scorecard weights are too low
D. The inclusion rule includes all CIs

**18.** According to governance best practice, who approves adding a new CI class or onboarding a new data source?
A. The service desk manager  B. The Configuration Control Board / CMDB governance board
C. ServiceNow Support  D. Any administrator

**19.** After a fresh implementation the Health Dashboard shows no scores. What do you check first?
A. Multisource settings  B. That the health scheduled jobs are active, since they are disabled out of the box
C. The Query Builder role  D. Life-cycle rules

**20.** Which feature periodically asks CI owners to confirm their CI data is still correct?
A. A data refresh rule  B. An Attestation policy in CMDB Data Manager
C. A reconciliation rule  D. Suggested relationships

**21.** Which two are configured per class in CMDB Health Preferences? (Choose 2)
A. Required and recommended fields  B. Identifier entries  C. Staleness and orphan rules  D. Data source precedence

## Insight

**22.** You need every Windows server that supports the Business Service "Payroll" through its Application Services,
across several relationship hops. Which tool?
A. A report on `cmdb_ci_win_server`  B. CMDB Query Builder  C. CMDB Health Dashboard  D. CMDB Data Manager

**23.** You need to see what each integration reported for the same attribute of one CI. Which tool?
A. CMDB 360  B. Dependency Views  C. CI Class Manager  D. Audit

**24.** Leadership wants to track progress through the CSDM maturity stages. Which tool?
A. CMDB Health Dashboard  B. CSDM Data Foundations Dashboard  C. CI Class Manager  D. Incident Performance Analytics

**25.** Which is the modern workspace that brings together health, Data Manager, Query Builder, Class Manager and
CMDB 360?
A. CMDB Dashboard  B. CMDB Workspace  C. Service Operations Workspace  D. Service Portfolio Workspace

## CSDM

**26.** Which record represents the deployed, running instance of an application that incidents should reference for
impact?
A. Business Application  B. Application Service  C. Business Service  D. Product Model

**27.** Which CSDM 5 domain contains Business Application and Business Capability?
A. Foundation  B. Design & Planning  C. Service Delivery  D. Service Consumption

**28.** In CSDM 5, the CSDM 4 domain "Manage Technical Services" is renamed to...
A. Build & Integration  B. Service Delivery  C. Service Consumption  D. Ideation & Strategy

**29.** Which two belong to the Foundation domain? (Choose 2)
A. Product Model  B. Application Service  C. Location  D. Business Service Offering

**30.** Which maturity stage typically introduces Business Services and Business Service Offerings?
A. Crawl  B. Walk  C. Run  D. Fly
