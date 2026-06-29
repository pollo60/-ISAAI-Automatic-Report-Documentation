# ISAAI — Automatic Report Documentation

**Project Report for the ISA (Information Systems Architecture) and A+I (Architecture & Integration) Modules**

> Frankfurt University of Applied Sciences — Summer Semester 2026

---

## 1. Project Objective

The ISAAI system automates the daily processing of structured financial reports (Report Type A and Report Type B), which arrive as XML files in ZIP archives via email. The manual process — extraction, threshold validation, evidence archiving, and supervisor escalation — is replaced by a fully automated Microsoft Power Automate flow.

**Dual-Module Approach:**

| Module | Focus | Technology |
|--------|-------|------------|
| **ISA** | Enterprise architecture, ArchiMate modeling, invoice OCR, chart automation | ArchiMate, PDF/OCR, PowerPoint |
| **A+I** | Operative process automation, XML/GOAL validation, exception governance | Power Automate, SharePoint, BPMN |

---

## 2. Architecture — From CURRENT via VISION to GOAL

The project follows the ArchiMate three-step approach **CURRENT → VISION → GOAL** to systematically document the transformation from the manual as-is state to the automated to-be state.

### 2.1 CURRENT (As-Is State)

In the as-is state, daily financial reports are processed entirely by hand. An employee opens incoming emails, extracts ZIP attachments, imports the XML data into a spreadsheet, visually checks threshold values, and manually creates evidence documents.

**ArchiMate CURRENT — Manual Daily Flow:**

![CURRENT — Manual Daily Flow](docs/Documentation/Architecture/CURRENT%20Architecture/CURRENT%20-%20Manual%20Daily%20Flow.png)

**ArchiMate CURRENT — Workplace and Evidence Landscape:**

![CURRENT — Workplace and Evidence Landscape](docs/Documentation/Architecture/CURRENT%20Architecture/CURRENT%20-%20Workplace%20and%20Evidence%20Landscape.png)

**BPMN CURRENT — Operative Process View (Lanes):**

![BPMN CURRENT — Validation Process with Lanes](docs/Documentation/Process%20Modeling/CURRENT%20Process/daily_financial_report_validation_lanes_CURRENT.png)

**Identified Weaknesses:**
- **30–40 minutes** of daily manual effort
- Media break between collaboration storage and document repository
- Missing system enforcement of the upload → sign-off process
- Risk: wrong fields, inconsistent outputs, forgotten archiving steps

---

### 2.2 VISION (Target Architecture)

The VISION describes the planned architecture after automation: email ingestion, rule-based validation, automatic evidence generation, and supervisor escalation only on exceptions (human-in-the-loop).

**ArchiMate VISION — Automated Target Architecture:**

![VISION — Automated Architecture](docs/Documentation/Architecture/VISION%20Architecture/Bildschirmfoto%202026-06-26%20um%2017.51.07.png)

**BPMN VISION — Operative Process View (Lanes):**

![BPMN VISION — Operative Automation Flow](docs/Documentation/Process%20Modeling/VISION%20Process/daily_financial_report_validation_lanes_OPERATION%20VISION.png)

**BPMN VISION — Strategic Governance:**

![BPMN VISION — Strategic Governance](docs/Documentation/Process%20Modeling/VISION%20Process/Strategic_Governance_Process.png)

---

### 2.3 GOAL (Realized State)

The GOAL state represents the actually implemented solution — the completed Power Automate flow with SharePoint integration, parallel XML validation, and automatic XLSX evidence file generation.

**ArchiMate GOAL — Realized Architecture:**

![GOAL — Realized Architecture](docs/Documentation/Architecture/GOAL%20Architecture/Bildschirmfoto%202026-06-26%20um%2017.56.03.png)

**BPMN GOAL — Strategic Validation Process (Lanes):**

![BPMN GOAL — Strategic Validation Process](docs/Documentation/Process%20Modeling/GOAL%20Process/daily_financial_report_validation_lanes_Strategic%20GOAL%20Kopie.bpmn.png)

---

## 3. Report Types & XML Presets

Two report types are processed daily, each using a distinct violation marker:

| Attribute | Report Type A (Daily) | Report Type B (Monthly) |
|---|---|---|
| **Coverage period** | Previous business day (daily snapshot) | Month-to-date cumulative |
| **Delivery frequency** | Daily, at agreed processing time | Daily, alongside Report Type A |
| **Violation marker** | `<DayViol>` | `<MonthViol>` |
| **Purpose** | Detects same-day threshold breaches | Tracks cumulative monthly breach trend |

### XML Structure — Report A (Daily)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Report type="ReportTypeA" date="20260610">
  <Metadata>
    <ReportID>RPT-651910</ReportID>
    <GeneratedAt>2026-06-25T13:52:06</GeneratedAt>
    <Description>Daily financial report — previous business day snapshot</Description>
    <CoveragePeriod>Daily</CoveragePeriod>
  </Metadata>
  <Data>
    <Row>
      <RowID>1</RowID>
      <DayViol>N</DayViol>
      <Threshold1>77</Threshold1>
      <Threshold2>92</Threshold2>
      <Threshold3>72</Threshold3>
      <Threshold4>89</Threshold4>
    </Row>
  </Data>
</Report>
```

### XML Structure — Report B (Monthly)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Report type="ReportTypeB" date="20260610">
  <Metadata>
    <ReportID>RPT-834215</ReportID>
    <GeneratedAt>2026-06-25T13:52:06</GeneratedAt>
    <Description>Monthly financial report — month-to-date cumulative</Description>
    <CoveragePeriod>Monthly</CoveragePeriod>
  </Metadata>
  <Data>
    <Row>
      <RowID>1</RowID>
      <MonthViol>V</MonthViol>
      <Threshold1>88</Threshold1>
      <Threshold2>42</Threshold2>
      <Threshold3>95</Threshold3>
      <Threshold4>61</Threshold4>
    </Row>
  </Data>
</Report>
```

Reference presets are provided in `src/presets/`.

---

## 4. Power Automate Flow — Technical Architecture

The flow **"ISAAI – Daily Report Processing"** is structured in six phases and is fully included as an importable Power Automate package in this repository.

```
src/flow/ISAAI–DailyReportProcessing_20260625165442.zip
```

### Phase A: Trigger & Variable Initialization
- **Trigger:** New email with subject "Financial Report" + ZIP attachment
- **Variables:** `LogItemID`, `ReportDate`, `ReportA_Result`, `ReportB_Result`, `ReportA_Details`, `ReportB_Details`

### Phase B: SharePoint List Entry
- Creates a new item in the SharePoint list **"Report Processing Log"**
- Sets `OverallStatus = Processing`

### Phase C: ZIP Extraction & XML Reading
- Extracts ZIP attachment to OneDrive `/Evidence Archive/Temp/`
- Reads `ReportTypeA.xml` and `ReportTypeB.xml` as text content

### Phase D: Parallel Validation
- **Left branch (Report A):** XPath query on `DayViol` → if `V`: threshold check (Threshold1–4 < 50 → Violation)
- **Right branch (Report B):** XPath query on `MonthViol` → identical threshold logic
- Both branches execute in parallel

### Phase E: Evidence Storage
- XLSX evidence files are saved to `/Evidence Archive/Evidence/` (Report A and B separately)
- Original XML files are archived to `/Evidence Archive/XML Archive/`
- Report A evidence includes: DayViol marker, all threshold values, validation status
- Report B evidence includes: MonthViol marker, all threshold values, validation status

### Phase F: Exception Gate & Completion
- **Violation detected:** SharePoint → `Exception`, email to supervisor (priority: High)
- **No violation:** SharePoint → `Completed`, confirmation email to standard distribution

### Two-Step Validation Logic

```
┌──────────────────────────────────────────────────────────────────┐
│  Report A: Step 1 — DayViol == "V"?                             │
│  Report B: Step 1 — MonthViol == "V"?                           │
│            No  → Pass (Clean — no marker)                       │
│            Yes → proceed to Step 2                              │
│                                                                  │
│  Step 2: Threshold1..4 < 50?                                     │
│          All ≥ 50 → Pass (Marker present but thresholds healthy) │
│          At least 1 < 50 → VIOLATION → Exception                 │
└──────────────────────────────────────────────────────────────────┘
```

---

## 5. Test Data & Simulations

The repository contains scripts for a complete offline simulation of the Power Automate flow.

### Running the Simulation

```bash
# 1. Install dependencies
pip install python-pptx openpyxl

# 2. Generate test runs (30 days, reproducible)
python scripts/simulate_runs.py --count 30 --seed 42

# 3. Local processing (simulates the Power Automate flow)
python scripts/local_flow_processor.py

# 4. Generate consolidated findings presentation
python scripts/generate_findings_presentation.py
```

### Evidence Output

Each run generates:
- `evidence_ReportTypeA.xlsx` — Styled XLSX with DayViol marker, thresholds, and breach details
- `evidence_ReportTypeB.xlsx` — Styled XLSX with MonthViol marker, thresholds, and breach details
- `summary.txt` — Human-readable validation summary

### SharePoint List Status Values

These values match the dropdown menus in the SharePoint list schema:

| Column | Allowed Values |
|--------|---------------|
| `ReportA_Status` / `ReportB_Status` | **Pass**, **Violation**, **Error**, **Pending** |
| `OverallStatus` | **Completed**, **Exception**, **Processing**, **Failed** |
| `ExceptionFlag` | **Yes**, **No** |

---

## 6. SharePoint List — Schema

The SharePoint list **"Report Processing Log"** serves as the central audit trail:

| Column | Type | Description |
|--------|------|-------------|
| `Title` | Text | Email subject |
| `ReceivedDateTime` | Date/Time | Time of receipt |
| `SenderEmail` | Text | Sender address |
| `ReportDate` | Text | Report date (from filename) |
| `ReportA_Status` | Choice | `Pass` / `Violation` / `Error` / `Pending` |
| `ReportB_Status` | Choice | `Pass` / `Violation` / `Error` / `Pending` |
| `ReportA_ViolationDetails` | Multiline Text | Details on violation |
| `ReportB_ViolationDetails` | Multiline Text | Details on violation |
| `OverallStatus` | Choice | `Completed` / `Exception` / `Processing` / `Failed` |
| `ExceptionFlag` | Yes/No | Escalation triggered? |
| `EvidenceA_Link` | Hyperlink | Link to Report A evidence (.xlsx) |
| `EvidenceB_Link` | Hyperlink | Link to Report B evidence (.xlsx) |

---

## 7. Repository Structure

```
ISAAI-Automatic-Report-Documentation/
│
├── README.md                          ← This project report
│
├── docs/
│   ├── Documentation/
│   │   ├── Architecture/
│   │   │   ├── CURRENT Architecture/  ← ArchiMate as-is state
│   │   │   ├── VISION Architecture/   ← ArchiMate target architecture
│   │   │   └── GOAL Architecture/     ← ArchiMate realized state
│   │   ├── Process Modeling/
│   │   │   ├── CURRENT Process/       ← BPMN as-is process
│   │   │   ├── VISION Process/        ← BPMN target process
│   │   │   └── GOAL Process/          ← BPMN realized process
│   │   ├── Project-Charter-ISAAI.tex  ← Project Charter (LaTeX)
│   │   ├── Project_Charter_ISAAI.pdf  ← Project Charter (PDF)
│   │   ├── roadmap.md                 ← Phase plan
│   │   └── issue-list.md              ← Task list
│   └── guides/
│       └── SHAREPOINT_FLOW_GUIDE.md   ← Step-by-step flow setup guide
│
├── src/
│   ├── flow/
│   │   ├── ISAAI–DailyReportProcessing_*.zip   ← Importable flow package
│   │   └── ISAAI–DailyReportProcessing_*/       ← Unzipped flow definition
│   │       ├── manifest.json
│   │       └── Microsoft.Flow/flows/.../
│   │           ├── definition.json              ← Complete flow logic
│   │           ├── apisMap.json
│   │           └── connectionsMap.json
│   ├── presets/
│   │   ├── ReportTypeA_Daily_Template.xml       ← Daily report XML preset
│   │   ├── ReportTypeB_Monthly_Template.xml     ← Monthly report XML preset
│   │   └── README.md                            ← Preset documentation
│   └── report_template/
│       └── Report Processing Log (1).csv        ← SharePoint CSV schema
│
├── scripts/
│   ├── simulate_runs.py               ← Generates mock XML/ZIP test data
│   ├── local_flow_processor.py        ← Simulates the flow locally (offline)
│   ├── generate_findings_presentation.py  ← Creates consolidated findings PPTX
│   └── build_boardroom_deck.py        ← Creates the boardroom deck
│
├── tests/
│   ├── runs/                          ← Generated test runs (run_1..run_30)
│   │   └── run_N/
│   │       ├── YYYYMMDD_ReportTypeA.xml
│   │       ├── YYYYMMDD_ReportTypeB.xml
│   │       ├── YYYYMMDD_Reports.zip
│   │       ├── evidence_ReportTypeA.xlsx  ← XLSX evidence (DayViol + thresholds)
│   │       ├── evidence_ReportTypeB.xlsx  ← XLSX evidence (MonthViol + thresholds)
│   │       └── summary.txt
│   ├── Report_Processing_Log_Local.csv  ← Local SharePoint equivalent
│   └── Email_Report_Schema (1).xlsx     ← SharePoint list schema definition
│
└── presentations/
    ├── ISAAI-Consolidated-Findings.pptx  ← Single consolidated findings deck
    └── Project Presentation/
        ├── praesi isa 2906.pptx.pptx     ← ISA module presentation
        └── praesi ai 2906.pptx.pptx      ← A+I module presentation
```

---

## 8. Importing the Flow — Instructions

1. Open [Power Automate](https://make.powerautomate.com/)
2. Navigate to **My Flows → Import → Import Package (Legacy)**
3. Upload the file `src/flow/ISAAI–DailyReportProcessing_20260625165442.zip`
4. The import wizard will display three connectors to configure:
   - **Office 365 Outlook** → Select or create your own connection
   - **SharePoint** → Select or create your own connection
   - **OneDrive for Business** → Select or create your own connection
5. Click **Import**
6. Update the SharePoint site URL in the flow actions to match your own site

> **Prerequisite:** A SharePoint site with the list "Report Processing Log" and the document library "Evidence Archive" must exist. See [`docs/guides/SHAREPOINT_FLOW_GUIDE.md`](docs/guides/SHAREPOINT_FLOW_GUIDE.md) for the complete setup guide.

### Testing via Power Automate

To test the flow using Microsoft's built-in testing feature:
1. Open the imported flow in the Power Automate designer
2. Click **Test** in the top-right corner
3. Select **Manually** and click **Test**
4. Send an email with subject "Financial Report" and a ZIP attachment containing the XML files from `tests/runs/`
5. Watch the flow execute in real-time in the test view

---

## 9. Technology Stack

| Component | Technology |
|-----------|------------|
| Automation | Microsoft Power Automate (Cloud Flow) |
| Data Storage | SharePoint Online (Lists + Document Library) |
| Evidence Format | XLSX (Excel) |
| Architecture Modeling | ArchiMate 3.1 (Archi) |
| Process Modeling | BPMN 2.0 |
| Local Simulation | Python 3, `openpyxl`, `python-pptx` |
| Version Control | Git / GitHub |

---

## 10. Authors

- **Altay Hennig** — Frankfurt University of Applied Sciences
- Modules: ISA (Information Systems Architecture) & A+I (Architecture & Integration)
- Semester: Summer Semester 2026
