# Audit trail and traceability

Maps to GOAL ArchiMate element **Standardized Audit Trail** (`GOAL_AUDIT_TRAIL`).

## Compliance objective

Every automated or human-governed step in the SOLL process must be reconstructable: who acted, when, on which artifact version, with what outcome.

## Minimum audit record (per event)

| Field | Description |
|-------|-------------|
| `event_id` | UUID |
| `timestamp` | ISO-8601 UTC |
| `actor` | Service account or human role (pseudonymized in logs) |
| `action` | e.g. `INGEST`, `VALIDATE`, `EXCEPTION_RAISED`, `APPROVE`, `ARCHIVE` |
| `resource_type` | `xml_report`, `exception_bundle`, `archive_package` |
| `resource_id` | Stable business key (report date + type) |
| `source_hash` | SHA-256 of inbound payload |
| `outcome` | `SUCCESS`, `FAIL`, `ESCALATED` |
| `approval_state` | `N/A`, `PENDING`, `APPROVED`, `REJECTED` |
| `parent_event_id` | Links escalation chain |

## Process alignment

| BPMN SOLL step | Required events |
|----------------|-----------------|
| Automated ingest | `INGEST` + `source_hash` |
| Rule evaluation | `VALIDATE` + rule version id |
| Exception path | `EXCEPTION_RAISED` + `approval_state=PENDING` |
| Supervisor decision | `APPROVE` or `REJECT` with `actor` |
| Archive | `ARCHIVE` + DMS mock reference |

## Implementation status

- **Concept:** documented (this file + OpenAPI mocks)
- **Production:** pending stakeholder DMS/API access
