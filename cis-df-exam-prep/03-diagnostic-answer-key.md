# Diagnostic Quiz - Answer Key

Score: ___ / 30. Misses by domain: Config __ Ingest __ Govern __ Insight __ CSDM __

| # | Domain | Answer | Why |
|---|---|---|---|
| 1 | Config | **B** | `cmdb_rel_ci` holds parent, child, type. `cmdb_rel_type` holds the type definitions. |
| 2 | Config | **B** | Extend the most specific fitting class through Class Manager so identification, health and suggested relationships are inherited and registered. |
| 3 | Config | **B** | In `Parent::Child` naming, the parent side descriptor applies to the parent record. |
| 4 | Config | **A, C** | Class Manager: attributes, identification/reconciliation rules, health preferences, suggested and dependent relationships. Policies live in Data Manager; health jobs are scheduled jobs. |
| 5 | Config | **B** | Model is Foundation data referenced by `model_id`; it is not a CI and not a relationship. |
| 6 | Ingest | **C** | IRE never guesses between multiple matches; it raises a de-duplication task for remediation. |
| 7 | Ingest | **B** | Dependent classes need the parent CI and the relationship in the same payload. |
| 8 | Ingest | **B** | Data refresh rules let a lower-priority source overwrite after the higher-priority source has been silent for N days. Reconciliation rules only say who may write; precedence says who wins now. |
| 9 | Ingest | **C** | Order of preference: native Discovery/Service Mapping, then Service Graph Connector, then IH-ETL, then scripted IRE, never direct writes. |
| 10 | Ingest | **C** | Lower precedence number = higher authority. |
| 11 | Ingest | **B, C** | Multisource is off by default and complements, not replaces, reconciliation. |
| 12 | Govern | **A, C, D** | Completeness, Correctness, Compliance. |
| 13 | Govern | **B** | Orphan = no relationships (per orphan rule). No owner is a Completeness (required field) problem. |
| 14 | Govern | **A, C, D** | Types: Retire, Archive, Delete, Attestation, Delete CMDB related entry. |
| 15 | Govern | **B** | Retire/Archive/Delete policies require an active life-cycle rule for every class in scope. |
| 16 | Govern | **A** | Required + recommended fields. |
| 17 | Govern | **B** | Duplicate detection reuses the identification rule. Fix the identifier, then re-run health. |
| 18 | Govern | **B** | The governance board / CCB approves model and source changes; admins execute. |
| 19 | Govern | **B** | Health score calculation jobs are inactive OOTB. |
| 20 | Govern | **B** | Attestation policy creates owner tasks. Data Certification is the older field-by-field feature. |
| 21 | Govern | **A, C** | Health Preferences: inclusion rules, required/recommended fields, orphan and staleness rules. Identifier entries and precedence are IRE settings in Class Manager. |
| 22 | Insight | **B** | Query Builder traverses classes through relationships; reports cannot walk multiple hops. |
| 23 | Insight | **A** | CMDB 360 = per-source attribute comparison (needs Multisource). |
| 24 | Insight | **B** | CSDM Data Foundations Dashboard = adoption/maturity. Health Dashboard = data quality. |
| 25 | Insight | **B** | CMDB Workspace. |
| 26 | CSDM | **B** | Application Service = running instance with an infrastructure map; the operational CI. |
| 27 | CSDM | **B** | Design & Planning (CSDM 4: Design). |
| 28 | CSDM | **B** | Manage Technical Services -> Service Delivery; Sell/Consume -> Service Consumption. |
| 29 | CSDM | **A, C** | Foundation = Product Model, Location, Company, Department, Group, User, etc. |
| 30 | CSDM | **C** | Run adds the consumer side: Business Services and Offerings, Service Portfolio, catalog links. |

## How to read your result
- 24+ correct: you are exam-ready on knowledge; spend Friday on the mock and hands-on labs, not rereading.
- 18-23: normal for someone with CMDB experience and little CSDM/governance vocabulary. Follow the plan as written.
- Under 18: prioritise Govern (35%) and the traps file; do the mock Saturday morning instead of Friday so the
  study guide sinks in first.
- Any domain with more than half missed: tell me which one and I will write a 15-question drill for it.
