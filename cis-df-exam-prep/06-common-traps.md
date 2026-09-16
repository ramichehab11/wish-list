# Common Traps - read the night before

## "Which tool?" decision table

| You need to... | Use | Not |
|---|---|---|
| Add an attribute, see the class tree, set identification/reconciliation for a class | **CI Class Manager** | Data Manager, System Definition > Tables |
| Retire/archive/delete CIs on a schedule, or ask owners to attest | **CMDB Data Manager** | Health remediation flows, scheduled scripts |
| See Completeness / Correctness / Compliance scores | **CMDB Health Dashboard** | Data Foundations Dashboard |
| Measure CSDM maturity / adoption | **CSDM Data Foundations Dashboard** (Store) | CMDB Health Dashboard |
| Compare what SCCM vs Discovery reported for one CI | **CMDB 360** (requires Multisource CMDB) | Dependency Views, Query Builder |
| List CIs across classes via relationships (servers under a business service) | **CMDB Query Builder** | Report designer, list filters |
| Show upstream/downstream impact of a CI | **Dependency Views / Application Service map** | Query Builder |
| Test whether a payload would match an existing CI | **Identification simulation / identifyCI** | createOrUpdateCI on production |
| Load data from a vendor tool that has a Store connector | **Service Graph Connector** | IH-ETL, import set |
| Load data from a source with no connector | **IntegrationHub ETL (RTE)** | classic transform map |
| Let a second source update after the first goes silent | **Data refresh rule** | Reconciliation rule, staleness rule |
| Stop a source from overwriting owner fields | **Reconciliation rule** (+ precedence) | Data refresh rule |
| Merge duplicates found by health | **Duplicate CI Remediator / de-dup tasks** | Delete policy |
| Group CIs for health slicing or change scoping | **CMDB Group** (from Query Builder query) | Dynamic CI Group |
| Represent infrastructure under a Technical Service Offering | **Dynamic CI Group** | CMDB Group |

## Confusable pairs

| A | B | The difference in one line |
|---|---|---|
| Business Application | Application Service | Portfolio record you own vs running instance with infrastructure map. Outages go on the Application Service. |
| Business Service | Technical (Technology Management) Service | Consumed by the business vs provided by IT to IT. |
| Service Offering | Service | Offering = level/variant with commitments; linked to its Service by the `parent` reference, not a relationship. |
| Dynamic CI Group | CMDB Group | CSDM construct under Technical Service Offerings vs governance/health grouping tool. |
| Product Model | CI | Catalogue definition vs the instance in your estate. Model is Foundation data, not a CI class. |
| Identification rule | Reconciliation rule | Is it the same CI? vs Who may update which field? |
| Data source precedence | Data refresh rule | Who wins now vs when a loser may win after silence. |
| Independent identifier | Dependent identifier | Stands alone vs needs parent CI + relationship in the payload. |
| Orphan | Stale | No relationships vs not updated in N days. |
| Required field (Completeness) | Required relationship (Correctness) | Attribute missing vs relationship missing. |
| Attestation (Data Manager) | Data Certification | Owner confirms CI is still right vs field-by-field record verification tasks. |
| Compliance KPI | Correctness KPI | Audit against desired state vs duplicates/orphans/stale. |
| CMDB Health Dashboard | CSDM Data Foundations Dashboard | Data quality vs CSDM adoption maturity. |
| Health Preferences | Scorecards | What is measured per class vs how much each measure weighs. |
| Import Set transform map | IntegrationHub ETL | Bypasses IRE by default vs calls IRE by design. |
| Service Graph Connector | IntegrationHub ETL | Certified prebuilt (built on IH-ETL) vs build-your-own. |
| Horizontal Discovery | Service Mapping | Infrastructure inventory bottom-up vs Application Service maps top-down from an entry point. |
| `cmdb_ci_service` | `cmdb_ci_service_business` / `_technical` / `_auto` | Legacy parent you should not populate vs the CSDM classes. |
| life_cycle_stage | install_status | New standard lifecycle vs legacy status. Data Manager policies need active lifecycle rules. |
| CSDM 4 "Manage Technical Services" | CSDM 5 "Service Delivery" | Same domain, renamed. Sell/Consume -> Service Consumption. Design -> Design & Planning. Build -> Build & Integration. |
| Crawl | Walk | Application Service + foundation vs Technical Services/Offerings + Dynamic CI Groups + Capabilities. |
| Run | Fly | Business Services/Offerings + portfolio vs everything strategic (processes, information objects, DevOps, ideation). |

## Behaviours to remember cold
- IRE: entries in priority order, first match wins, no match = insert, multiple matches = de-dup task (not a guess).
- Dependent CI payload without its parent and relationship = IRE error, nothing inserted.
- Unregistered discovery source in a payload = rejected.
- Lower precedence number = higher authority.
- Health jobs are off by default. Health uses the class identification rule to find duplicates.
- Retire/Archive/Delete policies need an active life-cycle rule for every class in scope.
- Multisource is off by default; CMDB 360 is empty without it.
- Service Offering -> Service is a reference; Application Service -> infrastructure is a relationship.
- Business Application never gets infrastructure relationships.
- Govern is 35% of the exam. When in doubt on a governance question, pick the answer with owners, policies and
  a review cadence over the answer with a script.
