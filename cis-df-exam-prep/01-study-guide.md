# CIS-DF Study Guide (condensed, blueprint-weighted)

Legend: **[core]** = expect a question. *(check)* = fact I am confident about but could not verify against the official
docs from this sandbox; confirm in your PDI if you have one.

---

## 1. How the exam asks questions

Most CIS-DF questions are one of five shapes. Recognise the shape and half the answer is done.

1. **"Which tool/feature would you use to..."** -> map the need to the OOTB feature (Class Manager vs Data Manager vs
   Health Dashboard vs Query Builder vs CMDB 360 vs IRE). See `06-common-traps.md`.
2. **"Which CSDM domain / table does X belong to"** -> Business Application (Design & Planning) vs Application Service
   (Service Delivery) vs Business Service (Service Consumption) vs Product Model (Foundation).
3. **"What is the best practice / recommended approach"** -> the ServiceNow-native, IRE-respecting, least-custom answer
   is almost always right. Never "write directly to cmdb_ci", never "customise the base class", never "use a legacy
   import set transform map when a Service Graph Connector exists".
4. **"What happens when..."** (IRE payload with two matches, dependent CI without parent, policy without lifecycle
   rule) -> know the engine behaviour.
5. **"Which KPI / metric / policy type"** -> Completeness / Correctness / Compliance; Retire / Archive / Delete /
   Attestation / Delete CMDB related entry.

---

## 2. Domain: Configuration (15%)

### 2.1 CMDB table structure [core]
- `cmdb` is the root; `cmdb_ci` (Configuration Item) is the base class every CI class extends. Classes are tables;
  child tables inherit parent columns (table-per-class extension).
- Key branches: `cmdb_ci_hardware` -> `cmdb_ci_computer` -> `cmdb_ci_server` -> `cmdb_ci_win_server`, `cmdb_ci_linux_server`;
  `cmdb_ci_appl` (Application) -> `cmdb_ci_app_server`, databases; `cmdb_ci_service` (legacy "Service" parent) ->
  `cmdb_ci_service_auto` (Application Service), `cmdb_ci_service_business` (Business Service),
  `cmdb_ci_service_technical` (Technical Service), `service_offering` (Service Offering);
  `cmdb_ci_business_app` (Business Application); `cmdb_ci_business_capability`; `cmdb_ci_query_based_service`
  (Dynamic CI Group); `cmdb_ci_information_object`.
- Relationships live in `cmdb_rel_ci` (parent, child, type). Types live in `cmdb_rel_type`, named
  `Parent descriptor::Child descriptor`, e.g. `Depends on::Used by`, `Runs on::Runs`, `Hosted on::Hosts`,
  `Contains::Contained by`, `Members::Member of`, `Consumes::Consumed by`.
- Models are not CIs: `cmdb_model` (Product Model, with Hardware/Software/Application model children) sits in the
  CSDM Foundation domain. A CI points to its model via `model_id`; `model_category` links CI classes to asset classes
  for asset-CI synchronisation.
- Important CI fields: `discovery_source` (choice list, one value per data source), `install_status`,
  `operational_status`, `life_cycle_stage` + `life_cycle_stage_status` (standard lifecycle, see Govern),
  `owned_by`, `managed_by`, `support_group`, `model_id`, `serial_number`, `correlation_id`.

### 2.2 CI Class Manager [core]
Single UI (also inside CMDB Workspace) to view the class hierarchy and, per class:
- **Basic info**: label, table name, parent, icon, model category.
- **Attributes**: add/modify columns on the class (not the base class).
- **Identification Rule**: one rule per class; identifier entries with priority order (see Ingest).
- **Reconciliation Rules** and **Data source precedence**: which sources may write which attributes.
- **Health**: class-specific health preferences (inclusion rules, required/recommended fields, orphan and staleness
  settings).
- **Suggested Relationships**: relationship types recommended between this class and others; drives the picker in
  the relationship editor.
- **Dependent Relationships** (hosting and containment rules): e.g. a Network Adapter is contained by a Computer;
  used by IRE for dependent identification.
- **Metadata**: which attributes are used by CMDB features like duplicate detection or identification.
- **Class governance** *(check)*: newer releases let you require approval before class changes go live.

### 2.3 Extending the model - best practices [core]
- Extend the **most specific existing class** that fits (an in-house app -> extend `cmdb_ci_appl`, a new server OS
  -> extend `cmdb_ci_server`). Never add a new class directly under `cmdb_ci` when a closer parent exists.
- Never rename or delete base-system classes or attributes; add, don't modify.
- Create custom classes through **CI Class Manager**, not by creating a table in System Definition, so the
  identification rules, health preferences and suggested relationships get inherited and registered.
- Check the ServiceNow Store for a Service Graph Connector or an existing class before you build one; many
  "missing" classes exist in the CMDB CI Class Models Store app (continuously updated class models).
- Before adding an attribute, ask whether the data belongs on the CI, on the Model, on the Asset, or in a related
  table (avoid putting portfolio/business data on infrastructure classes).

### 2.4 Relationships [core]
- A CI with no relationships is an **orphan** (Health -> Correctness).
- Direction matters: in `Depends on::Used by`, the parent depends on the child. An Application Service *Depends on*
  the Linux server it runs on; the server is *Used by* the service.
- **Suggested relationships** are guidance; **dependent relationships** (containment/hosting) are enforced by IRE
  for dependent classes.
- Application Services get their downstream relationships from Service Mapping (top-down), tag-based rules,
  calculated rules, or manual entry.

---

## 3. Domain: Ingest (19%)

### 3.1 Data population methods - and the order of preference [core]
1. **Discovery** (horizontal, agentless via MID Server, patterns/probes, credentials, schedules) and **Agent Client
   Collector (ACC)** where agentless is not possible. Native, IRE-aware.
2. **Service Mapping** (top-down) builds Application Services and their dependency relationships; also tag-based and
   ML-based mapping.
3. **Service Graph Connectors (SGC)**: ServiceNow-certified Store apps (SCCM/MECM, Intune, Jamf, AWS, Azure, GCP,
   SolarWinds, Tanium, Qualys, CrowdStrike, ...). Built on IntegrationHub ETL, use IRE, register a discovery source
   named `SG-<Vendor>`. Preferred over anything custom.
4. **IntegrationHub ETL (IH-ETL)**: guided, low-code UI to build a **Robust Transform Engine (RTE)** map from an
   import set staging table to CMDB classes. Supports conditional class mapping, related-CI/relationship mapping,
   preview and test with sample data, and calls IRE for you. Use it when no SGC exists.
5. **Import Sets + classic Transform Maps**: legacy. Writes to target tables directly and **bypasses IRE** unless you
   script `createOrUpdateCI` in an onBefore/onAfter script. Not recommended for CMDB.
6. **IRE API directly**: `sn_cmdb.IdentificationEngine.createOrUpdateCI(source, jsonPayload)` (server script) or
   REST `POST /api/now/identifyreconcile`. Fine for integrations that must push.
7. **Direct writes to cmdb_ci tables** (GlideRecord insert, list edit, Import set without IRE): never for bulk data;
   produces duplicates and breaks reconciliation.

### 3.2 IRE - Identification [core]
- Every payload item names a class and attribute values; IRE finds the **identification rule** for that class (own
  rule, or inherited from the nearest ancestor that has one).
- An identification rule has ordered **identifier entries**. Entries are tried in priority order; the **first entry
  that finds a match wins**; if no entry matches, IRE **inserts** a new CI. If an entry finds **more than one**
  match, IRE does not guess: it flags the duplicates (creates a **de-duplication task**, `reconcile_duplicate_task`)
  and by default updates the first/oldest match *(check which one on your release)*.
- Entry types:
  - **Independent**: CI can be identified on its own attributes (server by serial number, then by name+class).
  - **Dependent**: CI only makes sense with a parent (network adapter, disk, running process, database instance on a
    host). The identifier includes a dependency on the parent's identity; the payload **must include the parent CI
    and the relationship** or IRE returns an error.
  - **Lookup-based**: matches on a related lookup table rather than a CI attribute, e.g. `cmdb_serial_number` (several
    serial numbers per hardware CI) or MAC addresses.
  - **Related-entry**: uses a related table (not a lookup) for matching *(check)*.
- Entry options: **Allow null attribute** (match even when the attribute is empty; risky), **Enforce exact count
  match** (all criterion attributes must be present), `Search on table` (match against a parent table so a CI stored
  in a different subclass is still found; prevents cross-class duplicates).
- **Identification inclusion rules** narrow which existing records are candidates (e.g. only active CIs, only CIs in
  a given domain), reducing false matches and speeding identification.
- **Identification simulation** (CMDB Workspace) lets you test a JSON payload against the rules without committing.
- **Metadata rules / class metadata** define which attributes count as identifying vs. informational.
- Test question logic: "duplicates keep appearing from source X" -> source bypasses IRE, or the class has no usable
  identifier (rule relies on attributes the source does not send), or Allow null attribute is on.

### 3.3 IRE - Reconciliation [core]
- **Reconciliation rules**: per class (and optionally per attribute list), which **data sources** are allowed to
  update. If a source is not authorised for the attribute, IRE identifies the CI but does not overwrite that field.
- **Data source precedence rules**: ordering of sources for a class/attribute set. **Lower priority number = higher
  authority** (100 beats 200). Highest-authority source that has written the attribute owns it.
- **Data refresh rules**: let a **lower-priority source overwrite** an attribute when the higher-priority source has
  **not updated it for N days**. This is the answer to "SCCM should be able to update a server that Discovery stopped
  seeing 30 days ago".
- **Staleness rules** (reconciliation) mark data from a source stale after a period; different from Health staleness
  (see Govern) *(check the exact naming on your release)*.
- **Discovery sources** must exist in the `discovery_source` choice list; a payload with an unregistered source is
  rejected. SGC and IH-ETL register theirs.
- `createOrUpdateCI` vs `identifyCI`: the second only reports what would match, no writes.

### 3.4 Multisource CMDB [core]
- Off by default; enabled via a system property in the IRE / Multisource settings *(check)*. When on, IRE stores the
  **value each source reported for each attribute** in multisource tables, in addition to the reconciled value on the
  CI.
- Enables **CMDB 360** (compare sources per CI) and the **multisource Query Builder** view ("which CIs did SCCM
  report that Discovery did not").
- Exam angle: "you need to see what each integration reported for the same CI" -> enable Multisource, use CMDB 360.

### 3.5 Discovery and Service Mapping essentials (as they appear on this exam)
- MID Server sits inside the network, runs probes/patterns, talks outbound to the instance. Credentials are stored
  on the instance (or an external vault) and used by the MID Server.
- Horizontal discovery: IP ranges -> Shazzam port scan -> classification -> identification -> exploration
  (patterns). Produces infrastructure CIs and hosting/containment relationships, not business context.
- Top-down (Service Mapping): starts from an entry point (URL, host:port) and walks the connections to build an
  Application Service with its dependency map.
- Application Service population options: Mapped (Service Mapping), Tag-based, Calculated, Manual, and Dynamic CI
  Groups for Technical Service Offerings.
- Cloud discovery uses cloud accounts/service accounts and API calls rather than agents.

---

## 4. Domain: Govern (35%) - the biggest block

### 4.1 CMDB Health Dashboard and KPIs [core]
Three KPIs, each built from metrics, each metric from per-class **Health Preferences** and **scorecards** (weights).

| KPI | Metrics | Configured by |
|---|---|---|
| **Completeness** | **Required fields** populated, **Recommended fields** populated | Health Preferences -> Required/Recommended fields per class |
| **Correctness** | **Duplicate** CIs, **Orphan** CIs (no relationships), **Stale** CIs (not updated within threshold), plus relationship correctness checks (required/recommended relationships) | Orphan rules, Staleness rules, identification rules (for duplicate detection), relationship health rules |
| **Compliance** | Results of **audits** (desired-state / certification audits) run against CIs | Audit definitions (Data Certification and Compliance) |

Key behaviours:
- Health jobs (Completeness/Correctness/Compliance score calculation, health remediation) are **disabled by
  default**; you enable them and schedule them.
- **Inclusion rules** define which CIs of a class are evaluated (e.g. exclude retired CIs).
- **Scorecards** decide the weight of each metric/KPI in the aggregated score at CI, class, group and CMDB level.
- **CMDB Groups** (`cmdb_group`; membership by manual list or a saved Query Builder query) give you health per
  business slice ("health of everything supporting Payroll").
- Health preferences cascade from `cmdb_ci` downwards; override at the class level that needs different rules.
- **Remediation**: Health dashboard -> remediation via Flow Designer flows/subflows (e.g. remediate stale CIs, retire
  orphans), the **Duplicate CI Remediator** (merge duplicates into one survivor and re-point relationships/references),
  and de-duplication tasks worked in CMDB Workspace.
- Duplicate detection uses the class **identification rule**, so a class with a weak identifier reports few duplicates
  even when data is dirty. "Fix the identifier first" is a common correct answer.

### 4.2 CMDB Data Manager [core]
Policy engine for **CI lifecycle governance**, located in CMDB Workspace.

| Policy type | What it does |
|---|---|
| **Retire** | Sets matching CIs to the Retired lifecycle stage (with proper status) on schedule |
| **Archive** | Moves matching CIs (and related data per archive rules) to archive tables |
| **Delete** | Deletes matching CIs |
| **Attestation** | Creates attestation tasks for owners to confirm the CI data is still correct |
| **Delete CMDB related entry** | Removes related records (relationships, key values, etc.) rather than the CI |

Rules of the game:
- Policies have a **condition/filter**, a **schedule**, an optional **approval** step, and a **life-cycle rule
  dependency**: Retire, Archive and Delete policies require an **active life-cycle rule for every class in scope**;
  otherwise the policy cannot run.
- Policies run in a sequence retire -> archive -> delete typical of a retention standard; each has its own policy.
- Attestation results feed governance ("owner certified in the last 90 days").

### 4.3 CI Lifecycle Management [core]
- Standardised lifecycle fields on `cmdb_ci`: **Life cycle stage** (`life_cycle_stage`: e.g. Design/Operational/
  End of Life/Retired *(check list)*) and **Life cycle stage status** (`life_cycle_stage_status`: e.g. Operational ->
  Operational/Non-operational/Repair in progress...). Replaces relying on `install_status` + `operational_status`
  alone; those legacy fields can be kept in sync.
- **Life cycle rules** per class define which stage/status combinations are valid and how legacy status values map.
- Data Manager, Health inclusion rules and CSDM adoption dashboards read these fields, which is why the exam ties
  "activate lifecycle rules" to "make Data Manager policies work".

### 4.4 Governance framework (people and process)
- **Configuration Management Process Owner / Configuration Manager**: owns the CMDB policy, standards and KPIs.
- **CMDB Governance Board / Configuration Control Board (CCB)**: approves class model changes, new data sources,
  attribute additions, and reviews health trends.
- **CI class stewards / data owners** per class or domain; **Service Owners** and **Application Owners** own CSDM
  service records (`owned_by`, `managed_by`, `support_group`).
- **Data sources register**: every integration is registered as a discovery source with an owner and reconciliation
  rules before it goes live.
- Governance cadence: health review, attestation cycle, class-change approvals, audit/compliance reporting.
- Foundation data governance (Company, Location, Department, Business Unit, Cost Center, User, Group, Vendor,
  Manufacturer, Product Model) is a prerequisite: services and CIs reference these, so their quality caps CMDB quality.
- Roles you may be asked about: `itil` (read/relate CIs in tasks), `cmdb_read`, `asset`/`model_manager` for models,
  `cmdb_query_builder` / `cmdb_query_builder_read` for Query Builder, `sn_cmdb_editor`-type roles for the Workspace
  *(check exact role names on your release)*, `admin` for Class Manager changes.

### 4.5 Data Certification and Audit
- **Data Certification**: schedules and assigns certification tasks asking users to verify records (CIs or any table)
  field by field. Older mechanism, still referenced.
- **Audit (Compliance)**: defines a desired state and reports non-compliant CIs; feeds the Compliance KPI.
- **Attestation** (Data Manager): the CMDB-Workspace-era equivalent focused on CI owners.

### 4.6 CSDM Data Foundations Dashboard [core]
- ServiceNow Store app ("CMDB and CSDM Data Foundations Dashboard"): shows **CSDM adoption/maturity indicators** per
  stage (Crawl/Walk/Run/Fly) alongside CMDB health signals, e.g. Application Services without relationships,
  Business Applications without Application Services, Service Offerings missing owners.
- Exam angle: "measure CSDM maturity" -> this dashboard, not the Health Dashboard.

---

## 5. Domain: Insight (20%)

### 5.1 CMDB Workspace [core]
- Modern (Next Experience) home for configuration managers: overview health tiles, **Health**, **Data Manager**,
  **Query Builder**, **Class Manager**, **CMDB 360**, **IRE simulation**, remediation and attestation task lists,
  data-source views. Replaces the legacy CMDB Dashboard / CMDB Home for day-to-day work.

### 5.2 CMDB 360 [core]
- Per-CI view of **what each data source reported** for each attribute versus the reconciled value; highlights
  conflicts and gaps. **Requires Multisource CMDB** to be enabled and populated.

### 5.3 CMDB Query Builder [core]
- Drag-and-drop canvas to build **multi-class, relationship-aware queries** ("all Windows servers used by
  Application Services that support Business Service X, with their owners"). Runs on demand or on schedule, results
  can be saved, exported, used for **CMDB Groups**, and for **multisource comparisons**.
- Not a report designer: use it for relationship traversal, then report on the results.

### 5.4 Dependency Views and Application Service maps
- **Dependency Views** (BSM map) show upstream/downstream relationships from any CI; **Application Service map**
  shows the mapped service topology; newer releases offer a **Unified Map** experience *(check)*.
- Used for impact analysis in Incident/Change, and to verify CSDM linkage (Service Offering -> Application Service
  -> infrastructure).

### 5.5 Reporting and analytics
- Health KPIs are available in Performance Analytics dashboards (trend over time), the Health Dashboard shows the
  current state.
- Reports on `cmdb_ci` children and `cmdb_rel_ci`; use Query Builder when the question spans classes through
  relationships. Dot-walk on `cmdb_rel_ci` for simple two-hop questions.
- CSDM Data Foundations Dashboard = maturity/adoption insight; CMDB Health Dashboard = data quality insight;
  CMDB 360 = source-level insight; Dependency Views = topology insight.

---

## 6. Domain: CSDM Fundamentals (11% officially, but its vocabulary appears across the other 89%)

### 6.1 What CSDM is
- A **standard, prescriptive data model and set of guidelines** for using the OOTB CMDB tables (and related
  non-CMDB tables) so that all ServiceNow products (ITSM, ITOM, APM, SPM, SecOps, HAM/SAM, IRM) share the same
  definitions. It is **not a product to install**; it is a way to use tables that already exist, expressed as a
  white paper + a set of Store dashboards.
- Principle: put each kind of information in the table designed for it, relate them with the prescribed relationship
  types, and adopt incrementally (**Crawl -> Walk -> Run -> Fly**).

### 6.2 Domains - CSDM 4 vs CSDM 5 [core]

| CSDM 4.0 (6 domains) | CSDM 5.0 (7 domains) | What lives there |
|---|---|---|
| Foundation | **Foundation** | Company, Business Unit, Department, Cost Center, Location, User, Group, CMDB Group, Product Model, Vendor/Manufacturer, Business Process, Contract, Value Stream, Product Feature, SBOM (new in 5) |
| - | **Ideation & Strategy** (new) | Product Idea, Planning Item (demand, project, epic), Strategic Plan, Strategic Priority, Goal, Target |
| Design | **Design & Planning** | Business Capability, **Business Application**, Information Object |
| Build | **Build & Integration** | DevOps change data model (pipelines, repositories, SDLC components), AI System digital asset |
| Manage Technical Services | **Service Delivery** | **Application Service** (and its subtypes), Service Instance, Service Delivery Network, API, Application, AI Function/AI Application, OT, infrastructure CIs, **Technology Management Service** (was Technical Service) and its **Service Offering**, **Dynamic CI Group** |
| Sell/Consume | **Service Consumption** | **Business Service**, **Business Service Offering**, Request Catalog items linked to offerings |
| Manage Portfolio | **Manage Portfolios** | Service Portfolio, Application Portfolio, Product/Technology portfolios that group the above |

CSDM 3.0 had four domains (Foundation, Design, Manage Technical Services, Sell/Consume); 4.0 added Build and Manage
Portfolio; 5.0 added Ideation & Strategy and renamed the rest. Expect at least one question on the renames and one on
which domain a table belongs to.

### 6.3 The tables you must be able to tell apart [core]

| Term | Table | Domain | One-line meaning | Used in Incident/Change? |
|---|---|---|---|---|
| **Business Application** | `cmdb_ci_business_app` | Design & Planning | The software *as a portfolio item*: "SAP ERP", "Workday". Owned by APM, has lifecycle, cost, business capability links. **Not** an operational CI, **no** infrastructure relationships. | No (impact comes via its Application Services) |
| **Application Service** | `cmdb_ci_service_auto` (subtypes: Mapped `cmdb_ci_service_discovered`, Calculated, Tag-based, Manual) | Service Delivery | A **deployed, running instance** of an application in an environment: "SAP ERP - PROD EMEA". Has a dependency map to servers/DBs. | Yes: the operational CI for impact, monitoring, change |
| **Technical / Technology Management Service** | `cmdb_ci_service_technical` | Service Delivery | An IT-provider service: "Windows Server Hosting", "Database Management". Owned by an IT team. | Via its offerings |
| **Technical Service Offering** | `service_offering` (parent = technical service) | Service Delivery | A specific level/variant of the technical service, with commitments (SLA), support group, and linked infrastructure via **Dynamic CI Groups** | Yes, in the Service offering field for infra-type work |
| **Business Service** | `cmdb_ci_service_business` | Service Consumption | A service **consumed by the business** or customers: "Email", "Payroll", "Order Management". Owned by a service owner. | Yes: Incident "Service" field |
| **Business Service Offering** | `service_offering` (parent = business service) | Service Consumption | A consumable variant with audience, SLA, hours, price: "Email - VIP", "Payroll - Germany" | Yes: Incident "Service offering" field |
| **Dynamic CI Group** | `cmdb_ci_query_based_service` | Service Delivery | Query-defined set of CIs (all PROD Oracle DBs) that stands in for infrastructure under a Technical Service Offering | Indirectly |
| **Business Capability** | `cmdb_ci_business_capability` | Design & Planning | What the business *does* ("Manage Payroll"), realised by Business Applications | No |
| **Information Object** | `cmdb_ci_information_object` | Design & Planning | Data entity an application creates/uses ("Customer record") | No |
| **Product Model** | `cmdb_model` | Foundation | The catalogue definition ("Dell R750", "Windows Server 2022"); a CI references it | No |
| **Service Portfolio** | `spm_service_portfolio` *(check)* | Manage Portfolios | Grouping of services for portfolio management | No |
| **Legacy "Business Service"** | `cmdb_ci_service` | (parent table) | Old catch-all. CSDM says: **do not create records directly here**; use the specific child classes | Avoid |

Memory hook: **Business Application = what you own; Application Service = what is running; Business Service = what
the business consumes; Technical Service = what IT provides to itself; Offerings = the levels you can pick.**

### 6.4 Prescribed relationships and references [core]
- Business Application **`Consumes::Consumed by`** Application Service *(check direction on your release; it is the
  CSDM-documented link between the portfolio record and its running instances)*.
- Application Service **`Depends on::Used by`** infrastructure CIs (servers, databases, load balancers) and other
  Application Services.
- Business Service Offering / Business Service **`Depends on::Used by`** Application Service.
- Technical Service Offering **`Depends on::Used by`** Dynamic CI Group / infrastructure; Dynamic CI Group
  membership is by query, not by relationship records.
- **Service Offering -> Service is a reference field (`parent`)**, not a relationship.
- Business Capability <-> Business Application via relationship; Business Application -> Business Capability drives
  APM heat maps.
- Product Model -> CI via **reference** (`model_id`), not a relationship.
- Task records: **Service** (`business_service`), **Service offering** (`service_offering`), **Configuration item**
  (`cmdb_ci`). CSDM guidance: Service = the Business Service or Application Service impacted; Service offering = the
  specific offering; CI = the technical CI at fault. Ideally the CI is related to the Service so the choices filter.

### 6.5 Crawl / Walk / Run / Fly [core]
Exact placement varies slightly between CSDM 4 and 5 material; this is the commonly taught version.

| Stage | Add these | Enables |
|---|---|---|
| **Crawl** | Foundation data cleaned up (Company, Location, Group, User, Product Model); **Application Services** (at least manually); Business Applications registered; infrastructure CIs with basic relationships | Incident/Change impact on application services; APM inventory |
| **Walk** | **Technical Services + Technical Service Offerings**, **Dynamic CI Groups**, **Business Capabilities**, Application Services mapped (Service Mapping / tag-based), owner fields populated | Support-team accountability, better routing, application rationalisation |
| **Run** | **Business Services + Business Service Offerings**, Service Portfolio, request catalog linked to offerings, SLAs per offering | Service-level reporting, customer-facing service catalog, SPM |
| **Fly** | Full portfolio management, Information Objects, Business Processes/Value Streams, DevOps and Ideation links, cost and demand tied to services, AI/OT/API items in CSDM 5 | Enterprise architecture, value-stream and product-centric operating model |

Rule of thumb for questions: **Crawl = Application Service and foundation; Walk = Technical side; Run = Business
(consumer) side; Fly = everything strategic.**

### 6.6 CSDM and other products (why it matters)
- **ITSM**: Incident/Problem/Change reference Services, Offerings and CIs consistently -> reporting per service.
- **APM**: Business Applications, Capabilities, Information Objects; needs Application Services to link to reality.
- **SPM/ITBM**: Service Portfolios, Demand -> Ideation & Strategy in CSDM 5.
- **ITOM**: Discovery/Service Mapping populate Service Delivery; Event Management alerts roll up to Application
  Services and then to Business Services for impact.
- **HAM/SAM**: Models and Assets in Foundation, tied to CIs.
- **SecOps/VR/IRM**: vulnerabilities on CIs roll up to services for risk-based prioritisation.
- That is why CIS-DF is a **prerequisite** for CIS-ITSM, CIS-Discovery, CIS-Service Mapping, CIS-HAM, CIS-SAM,
  CIS-SIR and CIS-VR.

### 6.7 CSDM implementation guidance the exam likes
- Start with a **use case** (impact analysis, service reporting, app rationalisation), pick the stage that delivers
  it, and stop there until the data is governed.
- **Do not customise** the model to fit old naming; map old records to the right CSDM tables (classic mistake:
  everything sitting in `cmdb_ci_service`).
- Assign **owners** to every service record; a service without an owner is a governance failure, not a modelling one.
- Use the **CSDM Data Foundations Dashboard** and CMDB Health to measure progress per stage.
- Business Applications are **not** used for outages; Application Services are. Do not relate infrastructure to
  Business Applications.
- Environment (PROD/TEST/DEV) is an attribute of the **Application Service**, not separate Business Applications.
