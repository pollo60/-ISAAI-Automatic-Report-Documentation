# Stakeholder interface questions (Nachverfolgung)

**Executive summary (EN):** Interface access, probe accounts, and production audit policies are open stakeholder decisions. This repository delivers OpenAPI v3 mocks and compliance concepts until real MCP/LLM endpoints are available.

---

## Audit trail & Nachvollziehbarkeit

**Frage:** Welche Compliance-Anforderungen existieren für Tracking von Modifikationen, Genehmigungen und Datenherkunft?

**Projektstand:** Siehe [`AUDIT-TRAIL.md`](AUDIT-TRAIL.md). SOLL-BPMN und GOAL-ArchiMate verankern `Standardized Audit Trail`. Mock-APIs liefern `X-Request-Id` und Event-Payloads als Referenz.

**Offen beim Stakeholder:** Bindende Aufbewahrungsfristen, Signaturverfahren, Integration ins produktive DMS.

---

## Pseudonymisierung vor internem LLM

**Frage:** Müssen wir etwas pseudonymisieren, bevor wir es an das interne LLM schicken?

**Projektstand:** Ja — Default in [`DATA-HANDLING.md`](DATA-HANDLING.md). Keine Roh-PII in Prompts oder CI-Logs.

**Offen beim Stakeholder:** Zentrale DLP-Policy, erlaubte Felder pro Use Case.

---

## API / Swagger / MCP agents

**Frage:** Können wir API-Zugriff / Swagger der internen MCP Agents bekommen? ChatGPT oder Claude?

**Projektstand:** **Kein Zugriff angenommen.** Spezifikationen unter [`../api/openapi/`](../api/openapi/) sind **Mocks** mit Beispiel-Auth (`Bearer`) und Fehlerfällen.

**Offen beim Stakeholder:** Welches Modell/Gateway, OpenAPI-URL, Sandbox vs. Produktion.

---

## Probeaccount

**Frage:** Könnt ihr uns einen Probeaccount einrichten?

**Vorschlag Ticket:**

```
Subject: ISAAI — sandbox access for report automation interfaces
Need: read-only sandbox for (1) XML ingest, (2) exception approval, (3) archive mock
Duration: project phase through 2026-06-16
Contact: [project team]
```

---

## OpenAPI v3 pro Schnittstelle

**Frage:** Jede Schnittstelle benötigt OpenAPI v3 inkl. Mock-Daten, Fehlerfälle, Auth-Header.

**Projektstand:** Delivered:

| Spec | File |
|------|------|
| Report ingestion | `docs/api/openapi/report-ingestion.openapi.yaml` |
| Exception governance | `docs/api/openapi/exception-governance.openapi.yaml` |
| Archive / DMS | `docs/api/openapi/archive-dms.openapi.yaml` |

**Offen beim Stakeholder:** Abgleich mit realem internen Handling und Auth-Scopes.
