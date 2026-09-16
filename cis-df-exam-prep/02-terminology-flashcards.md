# CIS-DF Terminology Flashcards

Cover the right column. Say the definition out loud. Move fast; mark misses with `x` in the first column and redo
only those on the next pass.

## Block A - CSDM vocabulary

| | Term | Definition |
|---|---|---|
| | CSDM | Common Service Data Model: ServiceNow's prescriptive standard for which OOTB tables to use for services, applications and their relationships. Guidance, not a plugin. |
| | CSDM 5 domains | Foundation; Ideation & Strategy; Design & Planning; Build & Integration; Service Delivery; Service Consumption; Manage Portfolios. |
| | CSDM 4 domains | Foundation; Design; Build; Manage Technical Services; Sell/Consume; Manage Portfolio. |
| | Ideation & Strategy | New in CSDM 5: product ideas, planning items (demand/project/epic), strategic priorities, goals, targets. |
| | Foundation domain | Reference data everything else points to: Company, Business Unit, Department, Cost Center, Location, User, Group, CMDB Group, Product Model, Vendor, Manufacturer, Business Process, Contract, SBOM. |
| | Business Application | `cmdb_ci_business_app`. Portfolio record for software the organisation owns (APM). Not operational; no infrastructure relationships. Design & Planning domain. |
| | Application Service | `cmdb_ci_service_auto`. A running, deployed instance of an application in an environment, with a dependency map to infrastructure. Service Delivery domain. The operational CI for impact. |
| | Mapped Application Service | Application Service whose map is built by Service Mapping (top-down). |
| | Tag-based Application Service | Application Service whose members are CIs carrying specific tags (key/value). |
| | Calculated Application Service | Application Service whose members are derived from relationship rules/calculations. |
| | Manual Application Service | Application Service whose members are added by hand in the map editor. |
| | Technical Service (CSDM 4) / Technology Management Service (CSDM 5) | `cmdb_ci_service_technical`. A service IT provides to itself or other IT teams, e.g. Database Hosting. |
| | Technical Service Offering | `service_offering` with a technical service as parent; carries commitments, support group, and infrastructure via Dynamic CI Groups. |
| | Business Service | `cmdb_ci_service_business`. Service consumed by the business/customers, e.g. Payroll, Email. Service Consumption domain. |
| | Business Service Offering | `service_offering` with a business service as parent; audience, SLA, hours, price. What the Incident "Service offering" field should point to. |
| | Service Offering | Generic term for a variant/level of a Business or Technical Service; table `service_offering`, linked by the `parent` reference. |
| | Dynamic CI Group | `cmdb_ci_query_based_service`. Query-defined set of CIs used under Technical Service Offerings instead of thousands of individual relationships. |
| | Business Capability | `cmdb_ci_business_capability`. What the business does; realised by Business Applications; APM heat maps. |
| | Information Object | `cmdb_ci_information_object`. Data entity created/used by an application. Design & Planning. |
| | Product Model | `cmdb_model`. Catalogue definition of hardware/software/application; a CI references it via model_id. Foundation. |
| | Service Portfolio | Manage Portfolios domain grouping of services (SPM). |
| | Service Instance | CSDM 5 Service Delivery concept: an individual instance of a delivered service (e.g. a tenant/subscription). |
| | Legacy `cmdb_ci_service` | Old catch-all "Business Service" parent table. CSDM: do not create records here; use the specific child classes. |
| | Crawl | Foundation data + Application Services (manual OK) + Business Applications registered. |
| | Walk | Technical Services and Offerings, Dynamic CI Groups, Business Capabilities, mapped Application Services. |
| | Run | Business Services and Offerings, Service Portfolio, catalog linked to offerings, SLAs per offering. |
| | Fly | Full portfolio/value stream/product operating model; Information Objects, Processes, DevOps, Ideation, AI/OT/API. |
| | Consumes::Consumed by | Relationship from Business Application to its Application Services (check direction). |
| | Depends on::Used by | Relationship from a service to what it depends on (Application Service -> server; Business Service Offering -> Application Service). |
| | Incident "Service" field | `business_service`: the Business Service or Application Service impacted. |
| | Incident "Service offering" field | `service_offering`: the specific offering impacted. |
| | Incident "Configuration item" field | `cmdb_ci`: the technical CI at fault. |
| | Environment | Attribute of the Application Service (PROD/TEST), never a reason for a second Business Application. |
| | CSDM Data Foundations Dashboard | Store app showing CSDM adoption/maturity indicators per stage plus CMDB health signals. |

## Block B - CMDB structure and Configuration

| | Term | Definition |
|---|---|---|
| | `cmdb_ci` | Base Configuration Item table; every CI class extends it. |
| | Table-per-class extension | Child class table inherits all parent columns; a record exists once, in its most specific class. |
| | `cmdb_rel_ci` | Relationship table: parent, child, type. |
| | `cmdb_rel_type` | Relationship types, named `Parent descriptor::Child descriptor`. |
| | Suggested relationship | Class Manager setting listing relationship types recommended between two classes. |
| | Dependent relationship / containment rule | Class Manager rule stating a class must be hosted by/contained in another; used by IRE dependent identification. |
| | CI Class Manager | Single UI for class hierarchy: attributes, identification rule, reconciliation rules, health preferences, suggested and dependent relationships, model category. |
| | Model category | Links a CI class to an asset class so asset-CI synchronisation works. |
| | `discovery_source` | Choice field on CI naming which source last updated it; every data source must be registered here. |
| | `correlation_id` | External system identifier field on CI, frequently used as an identifier attribute for integrations. |
| | `install_status` / `operational_status` | Legacy status fields; still used, now backed by lifecycle stage/status. |
| | Life cycle stage / stage status | Standardised lifecycle fields on cmdb_ci; valid combinations defined by per-class life cycle rules. |
| | Orphan CI | CI with no relationships to any other CI (as defined by orphan rules). |
| | Stale CI | CI not updated within the staleness threshold for its class. |
| | Duplicate CI | More than one CI matching the class identification rule. |
| | CMDB Group | `cmdb_group`: set of CIs by manual list or saved Query Builder query; used for health slicing and scoping. |
| | CMDB CI Class Models (Store) | Continuously updated class model content; check before creating custom classes. |

## Block C - Ingest and IRE

| | Term | Definition |
|---|---|---|
| | IRE | Identification and Reconciliation Engine: central framework that decides whether a payload matches an existing CI (identification) and which source may update which attribute (reconciliation). |
| | Identification rule | One per class (inherited if absent); ordered identifier entries; first matching entry wins; no match = insert. |
| | Identifier entry | A set of criterion attributes (or a lookup table) tried in priority order. |
| | Independent identifier | CI identifiable by its own attributes (serial number, name). |
| | Dependent identifier | CI identified only in the context of a parent CI (network adapter on a computer); payload must include parent + relationship. |
| | Lookup-based identifier | Match on a related lookup table such as `cmdb_serial_number` or network adapter MACs. |
| | Allow null attribute | Entry option that allows a match when the attribute is empty; source of false matches. |
| | Enforce exact count match | Entry option requiring all criterion attributes to be present. |
| | Identification inclusion rule | Narrows the candidate records IRE searches (e.g. only active CIs). |
| | De-duplication task | `reconcile_duplicate_task`; created when an identifier entry finds more than one match; worked in CMDB Workspace. |
| | Duplicate CI Remediator | Tool that merges duplicate CIs into a survivor and re-points relationships/references. |
| | Reconciliation rule | Declares which data sources may update a class (optionally specific attributes). |
| | Data source precedence rule | Orders sources per class/attributes; lower number = higher priority. |
| | Data refresh rule | Allows a lower-priority source to update after the higher-priority source has been silent for N days. |
| | Multisource CMDB | Optional mode storing per-source attribute values; enables CMDB 360 and multisource queries. |
| | `createOrUpdateCI` | `sn_cmdb.IdentificationEngine` API to push a payload through IRE from a script. |
| | `/api/now/identifyreconcile` | REST endpoint to push a payload through IRE from outside. |
| | `identifyCI` | IRE API that only reports what would match, without writing. |
| | Identification simulation | CMDB Workspace tool to test a payload against rules without committing. |
| | Service Graph Connector (SGC) | Certified Store integration built on IntegrationHub ETL; registers discovery source `SG-<Vendor>`; preferred over custom imports. |
| | IntegrationHub ETL | Guided low-code builder for Robust Transform Engine maps that load import set data into CMDB classes through IRE. |
| | Robust Transform Engine (RTE) | Transform framework used by IH-ETL and SGCs: entity mapping, conditional class selection, relationship mapping. |
| | Import Set + Transform Map | Classic import path; writes directly to target tables and bypasses IRE unless scripted. |
| | Discovery | Agentless horizontal discovery via MID Server: scan -> classify -> identify -> explore with patterns. |
| | MID Server | Java service inside the customer network executing probes/patterns and integrations; outbound-only to the instance. |
| | Pattern | Step-based discovery/mapping logic (Pattern Designer) replacing classic probes/sensors. |
| | Service Mapping | Top-down discovery from an entry point that builds Application Service maps. |
| | Agent Client Collector (ACC) | Agent-based collection for hosts where agentless is impossible; feeds Discovery and monitoring. |
| | Entry point | URL/host:port from which Service Mapping starts traversing an application service. |

## Block D - Govern and Insight

| | Term | Definition |
|---|---|---|
| | CMDB Health Dashboard | OOTB dashboard scoring Completeness, Correctness and Compliance at CMDB, class, group and CI level. |
| | Completeness | Required and Recommended fields populated. |
| | Correctness | Duplicates, Orphans, Staleness, relationship correctness. |
| | Compliance | Results of audits against desired state / certification. |
| | Health Preferences | Per-class settings: inclusion rules, required/recommended fields, orphan rules, staleness rules. |
| | Inclusion rule | Which CIs of a class are evaluated for health. |
| | Scorecard | Weights that decide how metrics/KPIs aggregate into the score. |
| | Health jobs | Scheduled score calculations and remediation jobs; disabled by default. |
| | Health remediation | Flow Designer flows/subflows triggered from health results (e.g. retire stale CIs). |
| | CMDB Data Manager | Policy engine in CMDB Workspace for CI lifecycle: Retire, Archive, Delete, Attestation, Delete CMDB related entry. |
| | Life cycle rule | Per-class definition of valid lifecycle stage/status combos; must be active for Retire/Archive/Delete policies. |
| | Attestation | Data Manager policy creating tasks for CI owners to confirm data is still correct. |
| | Data Certification | Older feature scheduling record-verification tasks field by field. |
| | Audit (Compliance) | Desired-state checks that report non-compliant CIs into the Compliance KPI. |
| | CMDB Workspace | Next Experience workspace: health, data manager, query builder, class manager, CMDB 360, IRE simulation, task queues. |
| | CMDB 360 | Per-CI comparison of each source's reported values; needs Multisource CMDB. |
| | CMDB Query Builder | Visual multi-class, relationship-aware query tool; saved queries feed CMDB Groups and reports. |
| | Dependency Views | Upstream/downstream relationship map from any CI (BSM map); impact analysis. |
| | Configuration Control Board | Governance body approving class changes, new sources, attribute additions; reviews health. |
| | Configuration Manager / Process Owner | Owns CMDB policy, standards, KPIs and the governance cadence. |
| | Class steward / data owner | Accountable for a class or data domain's quality and definitions. |
| | Service owner / Application owner | Accountable for service records (owned_by / managed_by / support_group). |
| | `cmdb_query_builder` | Role to create and run Query Builder queries (`_read` variant to run only). |

## Block E - added from the official blueprint

| | Term | Definition |
|---|---|---|
| | Six health metrics | Required fields, Recommended fields, Duplicate, Orphan, Stale, Audit. |
| | CSF vs KPI | Critical Success Factor = outcome the CMDB must deliver; KPI = the measured proxy from the Health Dashboard. |
| | Principal class | A class your organisation designates as important; health dashboards, Data Foundations Dashboard and Workspace focus on principal classes by default. |
| | De-duplication wizard | Duplicate CI Remediator: pick the survivor CI, merge attributes, move relationships and references, retire the rest. |
| | Playbook (Data Foundations Dashboard) | Guided fix per indicator: Summary of indicator -> Overview of problem -> Importance of addressing issue -> Fix or Improve. |
| | Indicator (Data Foundations Dashboard) | A measured data-quality or CSDM-adoption condition, each with a playbook. |
| | Model category | Maps a CI class to an asset class; drives asset-CI auto-creation and synchronisation. |
| | Asset State -> CI | Changing Asset State updates CI Install status and Hardware status. |
| | `SNAssetManagement` | Discovery source value on CIs created from an asset record. |
| | `ServiceNow` discovery source | Discovery source value on CIs created manually in the UI or by script. |
| | Unified Map | Single map experience replacing Dependency Views and the Application Service map; levels, filters, legend, details panel, impact. |
| | Natural Language Query | Type a question in Query Builder; it builds the relationship query for you to refine. |
| | CMDB saved query | Stored Query Builder query; scheduled runs and persisted results feed reports, including CMDB 360 data. |
| | Key-value tags (`cmdb_key_value`) | Tag pairs on CIs used for compliance identifiers, tag-based services and grouping. |
| | Non-discoverable CI | CI no tool can discover (business application, business service, contract, facility); populated manually or by import through IRE and kept current by attestation. |
| | Technical debt (CMDB) | Customisations that block upgrades: base-table changes, IRE bypass, scripted transforms, custom relationship types, non-CSDM naming. |
| | CMDB Librarian / Data Steward | Day-to-day data quality role: remediation tasks, attestation follow-up, stewardship of a data domain. |
| | CI Class Owner | Accountable for a class's definition, attributes and data quality. |
| | Cut score | Predetermined pass mark ServiceNow does not publish; not always 70%. |
