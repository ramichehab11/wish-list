# Blueprint Addendum - official sub-topics mapped to the kit

Source: ServiceNow University KB0012913, "CIS - Data Foundations (CMDB and CSDM) Exam - Mainline Blueprint",
updated November 2025. The blueprint says its sub-topic list is not all-inclusive, so treat this as the floor.
*(check)* marks details I am confident about but could not verify against product docs from this sandbox.

## 1. Sub-topic map

| Domain | Official sub-topic | Where it is covered | Gap closed below |
|---|---|---|---|
| Configuration 15% | CI Class Manager: table, class attributes, hierarchy | Guide 2.1-2.3 | |
| | When and how to use IRE | Guide 3.2-3.3 | |
| | When and how to configure CMDB 360 / multisource CMDB | Guide 3.4, 5.2 | Section 2.6 |
| Ingest 19% | How relationships are auto or manually populated | Guide 2.4, 3.5 | Section 2.4 |
| | Automation opportunities for CMDB integration | Guide 3.1 | |
| | Which data ingestion method to use | Guide 3.1, traps table | |
| | Minimise technical debt and ensure upgradeability | partly 2.3 | Section 2.5 |
| | Populate and maintain non-discoverable/manual CIs and attributes | thin | Section 2.3 |
| | Track security and regulatory compliance identifiers against CSDM objects | missing | Section 2.7 |
| | How Asset and CI align | missing | **Section 2.1** |
| Govern 35% | Six metrics of the CMDB health score | Guide 4.1 (now names them) | Section 2.2 |
| | Purpose and requirements of Data Manager | Guide 4.2 | |
| | Goals of good CMDB governance; what is needed to govern; key roles | Guide 4.4 | Section 2.9 |
| | Health Dashboards for KPIs and Critical Success Factors | Guide 4.1 | Section 2.2 |
| | Why duplicates are created and how to remediate; **deduplication wizard** | Guide 3.2, 4.1 | Section 2.8 |
| | Operationalise the CMDB | Guide 4.4 | Section 2.9 |
| | CMDB Workspace: when, why, features | Guide 5.1 | Section 2.10 |
| | **Define principal classes** | missing | **Section 2.11** |
| | Which Data Manager policy fits the scenario | Guide 4.2 | |
| | Validate data quality/compliance in the Health Dashboard | Guide 4.1 | |
| | Improve data quality with the CMDB Data Foundations Dashboard | Guide 4.6 | Section 2.12 |
| | Manage life cycle CI attributes between CIs | Guide 4.3 | Section 2.13 |
| Insight 20% | Business value of CMDB | missing | **Section 2.14** |
| | **Natural Language Query** | missing | Section 2.15 |
| | Custom reports using CMDB 360 data (**CMDB Saved Queries**) | thin | Section 2.15 |
| | Complex relationship queries with a full result set | Guide 5.3 | Section 2.15 |
| | **Unified Map** / dependency view map components and usage | Guide 5.4 | Section 2.16 |
| | Outcomes of ServiceNow products leveraging CMDB data | Guide 6.6 | Section 2.14 |
| | Benefits of, and when to use, CMDB Foundation Dashboards and **Playbooks** | missing | **Section 2.12** |
| CSDM 11% | Map CIs to the correct CSDM domain with stakeholders across industries | Guide 6.2-6.4 | Section 2.17 |
| | Approach to abide by CSDM | Guide 6.5, 6.7 | |
| | Benefits of implementing CSDM | Guide 6.6 | Section 2.17 |

## 2. Topics added after reading the blueprint

### 2.1 Asset and CI alignment [core: two of the three official sample questions are about this]
- **Asset** (`alm_asset`, with `alm_hardware`, `alm_license`, `alm_consumable`, `alm_facility`) is the financial and
  contractual view: cost, owner, contract, depreciation, state. **CI** is the operational and technical view:
  configuration, relationships, impact. One hardware asset maps to one CI, linked by the `ci` field on the asset and
  the `asset` field on the CI.
- The link is driven by **Model Category** (`cmdb_model_category`): it maps a CI class to an asset class and holds
  the "Create asset on insert" behaviour. Creating a CI in a mapped class auto-creates the asset; creating an asset
  with a model whose category is mapped auto-creates the CI.
- **Field synchronisation** between the two runs both ways for the shared attributes: model, serial number, asset
  tag, assigned to, location, company, department, cost center, and status.
- **Status mapping**: changing the Asset **State** updates the CI **Install status** and the CI **Hardware status**
  (the hardware-specific status field on hardware CIs). Asset **Substate** maps to the CI hardware substatus.
  Official sample question #2 tests exactly this: State on the asset changes -> Install Status and Hardware Status
  on the CI.
- A CI that was **created from an asset** carries `discovery_source = SNAssetManagement`. A CI created by hand in
  the UI or by a script carries `ServiceNow`. Official sample question #1: to find CIs created from assets that were
  never discovered, report on the class where Discovery source = `SNAssetManagement` (not on an empty Last
  discovered field, which also catches manual CIs).
- Governance angle: asset managers own financial attributes, configuration managers own technical ones, so
  reconciliation rules typically give the Asset/HAM source priority on cost and ownership fields and Discovery
  priority on technical fields.
- CSDM angle: assets and models sit in the **Foundation** domain (Product Model) and link to CIs in Service Delivery.

### 2.2 The six health metrics, KPIs and CSFs
- **Six metrics**: Required fields, Recommended fields (Completeness) · Duplicate, Orphan, Stale (Correctness) ·
  Audit (Compliance). Three KPIs roll them up. Scorecards weight them. Health Preferences define them per class.
- **Critical Success Factor (CSF)** = the outcome the CMDB must deliver (e.g. "accurate impact analysis for change").
  **KPI** = the measurable proxy (e.g. "Correctness above 90% for principal classes"). The Health Dashboard supplies
  the KPIs; governance defines the CSFs and target thresholds and reviews them on a cadence.
- Health results can be scoped by **principal classes**, **CMDB Groups**, or individual classes so KPIs are reported
  on what matters rather than on every table.

### 2.3 Non-discoverable and manual CIs and attributes
- Non-discoverable CIs: Business Applications, Business Services and Offerings, Business Capabilities, contracts,
  facilities, many OT/IoT and paper/process items. Non-discoverable attributes on discoverable CIs: owner, support
  group, cost center, environment, business criticality, compliance tags.
- Populate them with: manual creation in CMDB Workspace or the form; **spreadsheet/CSV import through IH-ETL** (so
  IRE still runs); Service Catalog items and Flow Designer flows that create the record with approvals; Foundation
  data joins (assigned_to from HR, cost center from Finance); Asset records (see 2.1).
- Keep them current with: **Attestation** policies, Data Certification tasks, ownership fields with mandatory values
  (Completeness required fields), and reconciliation rules that let the manual/HR source own those attributes so a
  discovery source cannot blank them.
- Best practice statement the exam likes: manual CIs still go through IRE (use the identification rule based on
  name + class or correlation_id), still get owners, and still get lifecycle stages.

### 2.4 Auto vs manual relationship population
- **Auto**: Discovery hosting/containment relationships (Runs on, Hosted on, Contains), Service Mapping dependency
  relationships, Service Graph Connectors and IH-ETL relationship mapping, tag-based and calculated Application
  Services, Dynamic CI Group queries, suggested relationships applied by the relationship editor.
- **Manual**: CI relationship editor (form related list / Dependency Views editor), Application Service manual map
  editor, bulk import of `cmdb_rel_ci` via IH-ETL, CSDM relationships from the Business Application to the
  Application Service and from Service Offerings down.
- Governance: manual relationships need an owner and a review cadence; the Correctness KPI flags orphans.

### 2.5 Technical debt and upgradeability
Choose in this order and you stay upgrade-safe: OOTB class (or Store class model) > extend via Class Manager >
custom class in a scoped app. OOTB relationship types > new type. Service Graph Connector > IH-ETL > scripted IRE
call > never a transform map that writes to `cmdb_ci` or direct GlideRecord inserts. No changes to base tables,
no scripts in identification rules where a rule option exists, no bypassing IRE, keep CSDM naming. Document every
extension through the governance board so it survives staff turnover and upgrades.

### 2.6 When to configure CMDB 360 / multisource
Turn it on when more than one source feeds the same classes and you need to audit which source said what, to
tune precedence rules with evidence, to detect sources that stopped reporting, or to answer "why does this CI say
X". It costs storage (per-source rows per attribute), so enable it for the classes that need it, not everything
*(check the per-class scoping on your release)*. CMDB 360 in the Workspace is the viewer; the multisource Query
Builder is the reporting side.

### 2.7 Security and regulatory compliance identifiers on CSDM objects
- Compliance requirements (PCI, SOX, HIPAA, GDPR, ISO 27001, internal data classifications) are tracked on the CSDM
  objects that carry business meaning, not on random infrastructure CIs: **Business Application** (data
  classification, business criticality, regulatory attributes), **Information Object** (data class), **Application
  Service** (environment and criticality inherited for operations), and **Business Service / Offering** for
  customer-facing commitments.
- Mechanisms: dedicated attributes on those classes, **key-value tags** (`cmdb_key_value`) when many identifiers
  are needed, CMDB Groups to scope audits, and IRM/GRC controls and policies attached to the CSDM records. Audit
  results feed the Compliance KPI.
- Why on CSDM objects: the identifier then flows down through relationships to every CI that supports the service,
  which is what vulnerability response and change risk need.

### 2.8 Why duplicates happen and the de-duplication wizard
- Causes: a source bypassing IRE; an identification rule that does not use the attributes the source sends;
  sources sending different classes for the same device without "Search on table"; Allow null attribute; the same
  device reported with different serial formats; manual creation before discovery.
- Detection: IRE flags multiple matches into **de-duplication tasks**; the Correctness KPI counts duplicates using the
  identification rule; CMDB 360 shows which source created each copy.
- Remediation: the **de-duplication wizard** (Duplicate CI Remediator) from the Health dashboard or the de-dup task:
  pick the **master/survivor** CI, choose how to merge attribute values, move relationships and references (tasks,
  assets) to the survivor, then retire or delete the losers. Then fix the root cause (identifier or source) or they
  come back.

### 2.9 Operationalising the CMDB and the key roles
- Operationalise = the CMDB is used daily by other processes and is kept healthy by routine, not heroics: health
  jobs scheduled, Data Manager policies live, attestation cycles running, dashboards reviewed, new sources
  onboarded through a defined path, class changes approved.
- Roles the blueprint lists in its audience table: **CMDB Administrator** (configures Class Manager, IRE, Health,
  Data Manager), **CMDB Librarian / Data Steward** (day-to-day data quality, remediation tasks, attestation follow-
  up), **Configuration Manager** (process owner, policies, KPIs/CSFs, governance board), **CI Class Owner**
  (accountable for a class's definition and data), **Platform Architect / Owner** (upgradeability, integrations,
  scoped apps), **Technical Consultant / Developer** (implements). Add **Service Owner** and **Application Owner**
  from CSDM.
- Goals of governance: trusted data for decisions, clear accountability, controlled change to the model,
  measurable quality, compliance evidence, lower operating cost.

### 2.10 CMDB Workspace features to be able to list
Home health overview and KPIs · Health drill-down with remediation · Data Manager (policies, attestation and
remediation task queues) · Query Builder (visual and Natural Language) · Class Manager · CMDB 360 · IRE
simulation and identification inclusion rules · Data source and integration views · CI 360/record view with
relationships and lifecycle · Data Foundations indicators (with the Store dashboard installed). Use it when the
task is configuration-manager work; use classic lists/forms for ad-hoc admin.

### 2.11 Principal classes
- A **principal class** is a CI class your organisation designates as important enough to be measured and shown
  by default: health dashboards, the Data Foundations Dashboard and Workspace filters focus on principal classes
  so a few thousand unimportant CIs do not drown the score.
- The base system ships a default list (servers, applications, databases, network gear, storage, services)
  *(check the exact list)*; you maintain it from the CMDB Health / Workspace preferences by adding or removing
  classes *(check the module name on your release)*.
- Exam pattern: "the health score is dominated by a class nobody cares about" -> adjust principal classes and
  inclusion rules, not the scorecard weights.

### 2.12 CMDB and CSDM Data Foundations Dashboard and Playbooks
- Store app that measures **indicators** across CMDB health and CSDM adoption stages (Crawl/Walk/Run/Fly), e.g.
  Application Services without relationships, Business Applications without Application Services, principal-class
  CIs without owners, unregistered discovery sources.
- Every indicator ships a **Playbook**, a structured guideline with a fixed outline, tested in official sample
  question #3:
  1. **Summary of indicator**
  2. **Overview of problem**
  3. **Importance of addressing issue**
  4. **Fix or Improve**
- Use the dashboard when you want to improve data quality with guidance and to show maturity progress to
  leadership; use the Health Dashboard for the raw KPI scores. When the blueprint says "improve data quality using
  the Data Foundations Dashboard", the answer is: work the indicators with their playbooks.

### 2.13 Life-cycle attributes between CIs
- Standard fields `life_cycle_stage` and `life_cycle_stage_status` are consistent across classes so lifecycle can be
  compared and propagated. **Life cycle rules** per class define allowed combinations and the mapping to legacy
  `install_status` / `operational_status` / hardware status.
- Between related CIs: when a host is retired, hosted or contained CIs should move with it. Data Manager policies
  and lifecycle flows can target related CIs so dependents are retired with the parent *(check the exact
  mechanism on your release)*; the Asset state syncs the CI status (2.1); Service Mapping can mark disappeared
  components; orphan and stale rules catch the leftovers.
- Exam pattern: "server retired but its running applications still show Operational" -> lifecycle governance gap,
  fix with lifecycle rules plus a Data Manager retire policy scoped to the dependent classes.

### 2.14 Business value of the CMDB and product outcomes
| Consumer | Outcome enabled by CMDB + CSDM data |
|---|---|
| ITSM Incident/Problem | Correct impact and priority, routing to the right support group, faster MTTR through dependency maps |
| ITSM Change | Risk assessment from relationships and conflicts, blackout and maintenance windows per service, CAB evidence |
| ITOM Event/AIOps | Alert correlation to Application Services, business-impact ranking, root cause via topology |
| Service Portfolio / Service Owner Workspace | Service-level reporting, availability and cost per service offering |
| APM | Application rationalisation, capability heat maps, technology risk |
| HAM / SAM | Asset-CI reconciliation, licence compliance from discovered software, refresh planning |
| SecOps Vulnerability Response | Risk-based prioritisation by business criticality of the services a CI supports |
| IRM / GRC | Control scoping and audit evidence tied to CSDM objects |
| CSM / FSM | Installed base and entitlements linked to customer-facing services |
| Finance / Cloud cost | Cost allocation by service and cost center |
Value statement: one trusted source of truth that turns technical data into service and business context.

### 2.15 Natural Language Query, saved queries and complex relationship queries
- **Natural Language Query** in Query Builder (CMDB Workspace) lets you type a question such as "Windows servers
  used by application services that support Payroll" and generates the query graph, which you then refine
  *(check licensing/Now Assist dependency on your release)*.
- **CMDB saved queries**: build once, save, run on demand or on schedule; results can be persisted so ordinary
  **reports and dashboards** can be built on them, including multisource (CMDB 360) results. This is the answer to
  "build a custom report on CMDB 360 data".
- Getting a **full result set** on complex queries: model every hop explicitly (class -> relationship type ->
  class), choose the correct relationship direction, use "any relationship" or relationship levels where the type
  varies, add filters on each node rather than only at the end, and include subclasses by querying the parent
  class. Missing results usually mean a wrong direction or a too-specific relationship type.

### 2.16 Unified Map
- The **Unified Map** is the newer single map experience that replaces switching between Dependency Views (BSM map)
  and the Application Service map. Components to name: the canvas with the focus CI, upstream/downstream levels
  with configurable depth, relationship-type and class filters, the legend, the CI details side panel, saved views
  or perspectives, and the ability to open impact for Incident/Change and to edit relationships *(check exact
  labels)*.
- Use it for impact analysis, root cause, validating CSDM linkage (offering -> application service -> infra), and
  as the visual check after Service Mapping.

### 2.17 CSDM with stakeholders across industries
- Mapping discipline: ask each stakeholder what they own and consume. Enterprise architects own **Business
  Capabilities** and **Business Applications** (Design & Planning). Application and infrastructure teams own
  **Application Services** and **Technical Services/Offerings** (Service Delivery). Business relationship and service
  managers own **Business Services/Offerings** (Service Consumption). Finance and HR own **Foundation** data.
  Strategy/portfolio offices own **Ideation & Strategy** and **Manage Portfolios**.
- Industry examples: a hospital's "Patient Admission" is a Business Service, "Epic - PROD" an Application Service,
  "Epic" the Business Application, "Clinical Systems Hosting" a Technical Service. A bank's "Card Payments" is a
  Business Service with offerings per card type; "PCI scope" is a compliance identifier on the Business Application
  and Information Objects. A manufacturer's PLC line is an OT CI under Service Delivery supporting a "Line 3
  Production" Business Service.
- Benefits to state: consistent reporting across products, faster impact analysis, less rework when new products
  are adopted, clear ownership, portfolio and cost transparency, upgrade-safe because it uses OOTB tables.

## 3. Official sample questions (from the blueprint)

**1.** The Configuration Management team wants to identify which CIs have been created from an asset but have not
been discovered. They create a report on the target CI class. How do they identify these CIs?
A. All CIs with a Discovery source value of `SNAssetManagement` · B. All CIs with Updated older than a month ·
C. All CIs where Last Discovered is empty · D. All CIs with a Discovery source value of `ServiceNow`
**Answer: A.**

**2.** A State field is updated on an Asset record. Which fields are automatically synchronised on the associated CI
record? (Choose two)
A. Operational status · B. Install Status · C. Hardware Status · D. Asset tag
**Answer: B, C.**

**3.** Put the structure of a Data Foundations Dashboard Playbook in order.
**Answer: Summary of indicator -> Overview of problem -> Importance of addressing issue -> Fix or Improve.**

## 4. Drag-and-drop practice (no partial credit on the real exam)

Match each need to the tool. One tool is used twice, one is not used.

| Need | | Tool |
|---|---|---|
| 1. Compare what SCCM and Discovery reported for one server | | A. CMDB Data Manager |
| 2. Ask owners yearly whether their CIs still exist | | B. CMDB 360 |
| 3. Report CSDM maturity to the CIO with guided fixes | | C. Data Foundations Dashboard |
| 4. Retire CIs not updated in 180 days | | D. CI Class Manager |
| 5. Add an attribute to Linux servers only | | E. Query Builder |

Answer: 1-B, 2-A, 3-C, 4-A, 5-D (E unused).

Match each metric to its KPI.

| Metric | | KPI |
|---|---|---|
| 1. Orphan | | A. Completeness |
| 2. Recommended field | | B. Correctness |
| 3. Audit | | C. Compliance |
| 4. Stale | | |
| 5. Required field | | |
| 6. Duplicate | | |

Answer: 1-B, 2-A, 3-C, 4-B, 5-A, 6-B.

Match the CSDM 4 domain to its CSDM 5 name.

| CSDM 4 | | CSDM 5 |
|---|---|---|
| 1. Design | | A. Service Consumption |
| 2. Manage Technical Services | | B. Build & Integration |
| 3. Sell/Consume | | C. Design & Planning |
| 4. Build | | D. Service Delivery |
| | | E. Ideation & Strategy |

Answer: 1-C, 2-D, 3-A, 4-B (E is new in CSDM 5, no CSDM 4 equivalent).
