# Test Runs

This directory stores the generated test data used to simulate and validate the ISAAI flow offline.

## Directory Structure

```
tests/
├── runs/                              ← One directory per simulated run
│   └── run_N/
│       ├── YYYYMMDD_ReportTypeA.xml   ← Daily report (DayViol marker)
│       ├── YYYYMMDD_ReportTypeB.xml   ← Monthly report (MonthViol marker)
│       ├── YYYYMMDD_Reports.zip       ← ZIP package (both reports)
│       ├── evidence_ReportTypeA.xlsx   ← XLSX evidence file (daily)
│       ├── evidence_ReportTypeB.xlsx   ← XLSX evidence file (monthly)
│       └── summary.txt                ← Validation results summary
├── Report_Processing_Log_Local.csv    ← Local equivalent of SharePoint list
└── Email_Report_Schema (1).xlsx       ← SharePoint list column definitions
```

## Report Types

| Report | Marker | Coverage | XML Element |
|--------|--------|----------|-------------|
| Type A (Daily) | `<DayViol>` | Previous business day | `DayViol` → `V` or `N` |
| Type B (Monthly) | `<MonthViol>` | Month-to-date cumulative | `MonthViol` → `V` or `N` |

## Validation Rules

1. **Step 1**: Check the violation marker (`DayViol` / `MonthViol`) for value `"V"`
   - If `"N"` → **Pass** (clean — no marker)
2. **Step 2** (only if Step 1 = `"V"`): Check all 4 thresholds against limit of 50
   - All ≥ 50 → **Pass** (marker present but thresholds healthy)
   - At least one < 50 → **Violation** (exception / escalation required)

## Status Values (SharePoint Dropdown)

| Column | Allowed Values |
|--------|---------------|
| `ReportA_Status` / `ReportB_Status` | Pass, Violation, Error, Pending |
| `OverallStatus` | Completed, Exception, Processing, Failed |
| `ExceptionFlag` | Yes, No |

## Regenerating Test Data

```bash
# Generate 30 reproducible test runs
python scripts/simulate_runs.py --count 30 --seed 42

# Process all runs locally (generates XLSX evidence files)
python scripts/local_flow_processor.py

# Generate consolidated findings presentation
python scripts/generate_findings_presentation.py
```