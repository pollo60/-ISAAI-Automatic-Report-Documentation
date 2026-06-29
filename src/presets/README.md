# Report XML Presets

These are the reference XML templates for the two report types processed by the ISAAI system.

## Report Type A — Daily Record

- **File**: `ReportTypeA_Daily_Template.xml`
- **Coverage**: Previous business day (daily snapshot)
- **Frequency**: Daily, at agreed processing time
- **Violation Marker**: `<DayViol>` — checks for value `"V"`
- **Purpose**: Detects same-day threshold breaches

## Report Type B — Monthly Record

- **File**: `ReportTypeB_Monthly_Template.xml`
- **Coverage**: Month-to-date cumulative
- **Frequency**: Daily, alongside Report Type A
- **Violation Marker**: `<MonthViol>` — checks for value `"V"`
- **Purpose**: Tracks cumulative monthly threshold breach trend

## Validation Rules

Both reports follow a **two-step check**:

1. **Step 1 — Marker Check**: Is the violation marker (`DayViol` / `MonthViol`) equal to `"V"`?
   - If **no** → Status: **Pass** (Happy Path)
2. **Step 2 — Threshold Check** (only if Step 1 = `"V"`): Are any of `Threshold1`–`Threshold4` below **50**?
   - If **yes** → Status: **Violation** (Exception / Escalation required)
   - If **no** → Status: **Pass** (No Escalation — marker present but thresholds healthy)

## Status Dropdown Values

These values match the SharePoint list schema (`Email_Report_Schema.xlsx`):

| Column | Allowed Values |
|--------|---------------|
| `ReportA_Status` / `ReportB_Status` | **Pass**, **Violation**, **Error**, **Pending** |
| `OverallStatus` | **Completed**, **Exception**, **Processing**, **Failed** |
| `ExceptionFlag` | **Yes**, **No** |

## File Naming Convention

Inbound XML files follow: `YYYYMMDD_ReportTypeA.xml` / `YYYYMMDD_ReportTypeB.xml`

Both reports are packaged together in a single ZIP file: `YYYYMMDD_Reports.zip`
