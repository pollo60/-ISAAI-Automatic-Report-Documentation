# Report Processing Procedure

**Scope:** Daily structured report control workflow covering two report types received as XML files.  
**Context:** Column-level identifiers and internal system names are abstracted throughout this document.

---

## 1. Report Type Overview

| Attribute | Report Type A | Report Type B |
|---|---|---|
| **Coverage period** | Previous business day (daily snapshot) | Month-to-date cumulative |
| **Delivery frequency** | Daily, at agreed processing time | Daily, alongside Report Type A |
| **Format** | XML | XML |
| **Role in process** | Detects same-day threshold breaches | Tracks cumulative monthly threshold breach trend |

---

## 2. File Naming Convention

Inbound files follow a date-prefixed naming pattern:

```
YYYYMMDD_ReportTypeA
YYYYMMDD_ReportTypeB
```

- `YYYYMMDD` = reference date of the report (typically previous business day for both types)
- Evidence files stored in SharePoint are renamed using the same convention

---

## 3. Validation Procedure

Each report type is validated independently using a **two-step check**:

### Step 1 — Primary Violation Marker Check

For **each row** in the report:

- **Report Type A:** Check the designated primary violation marker column for the value `"V"` (violation flag)  
- **Report Type B:** Check the designated primary violation marker column for the value `"V"` (violation flag)

If no row is marked with `"V"`, the report is clean → proceed to evidence filing.

### Step 2 — Secondary Threshold Check (triggered only if Step 1 = `"V"`)

If a violation marker is found, evaluate the **four secondary threshold columns** for that row:

| | Report Type A | Report Type B |
|---|---|---|
| **Number of threshold columns** | 4 | 4 |
| **Pass condition per column** | Value ≥ defined threshold | Value ≥ defined threshold |
| **Fail condition per column** | Value < defined threshold | Value < defined threshold |

The specific column positions and threshold values are defined in the operational rule set and are not repeated here.

---

## 4. Escalation Decision Table

| Step 1 Result | Step 2 Result | Action |
|---|---|---|
| No violation marker (`"V"` not found) | — (not evaluated) | **No Exception** → proceed to evidence filing and summary email |
| Violation marker found | All threshold columns ≥ limit | **No Escalation** → flag in result, proceed normally |
| Violation marker found | At least one threshold column < limit | **Escalate** → create exception case, notify supervisor, hold standard sign-off |

The escalation logic is identical for both Report Type A and Report Type B. Each report type is evaluated independently; an exception in one does not block the other.

---

## 5. Process Flow Summary

```
Receive ZIP/XML mail
  └─ Extract attachments
       └─ Import XML into working sheet
            ├─ Report Type A: Step 1 → (V?) → Step 2 → Escalate / No Exception
            └─ Report Type B: Step 1 → (V?) → Step 2 → Escalate / No Exception
                 └─ Store evidence (YYYYMMDD naming)
                      └─ Send summary email
                           └─ Archive in DMS + sign-off
```

In the **IST (manual) state**, Steps 1–2 and the escalation decision are performed by the Operations Analyst in Excel.  
In the **SOLL (automated) target state**, the rule evaluator component executes both steps programmatically and produces a structured validation result used by downstream notification and reporting modules.

---

*Document version: 1.0 — 07.05.2026*
