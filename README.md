# ISAAI — Automatic Report Documentation

**Project Report for the ISA (Information Systems Architecture) and A+I (Architecture & Integration) Modules**

> Frankfurt University of Applied Sciences — Summer Semester 2026

---

## 1. Project Objective

The ISAAI system automates the daily processing of structured financial reports (Report Type A and Report Type B), which arrive as XML files in ZIP archives via email. The manual process — extraction, compliance checking, evidence archiving, and supervisor escalation — is replaced by a fully automated Microsoft Power Automate flow.

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

Two report types are processed daily, each using a distinct compliance marker:

| Attribute | Report Type A (Daily) | Report Type B (Monthly) |
|---|---|---|
| **Coverage period** | Previous business day (trade-level detail) | Month-to-date cumulative trader summary |
| **Delivery frequency** | Daily, at agreed processing time | Daily, alongside Report Type A |
| **Violation marker** | `<DayViol>` | `<MonthViol>` |
| **Purpose** | Detects same-day trade exceptions | Tracks monthly cumulative trader breach trend |

### XML Structure — Report A (Daily Trades)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<XetraReport type="ReportTypeA" date="20260610">
  <Metadata>
    <ReportID>XETRA-DA-20260610</ReportID>
    <GeneratedAt>2026-06-10T18:30:00</GeneratedAt>
    <ReportType>Daily</ReportType>
    <CoveragePeriod>2026-06-10</CoveragePeriod>
    <TradingVenue>XETR</TradingVenue>
    <MemberID>FRAUAS01</MemberID>
  </Metadata>
  <Trades>
    <Trade>
      <TradeID>XTR-20260610-00147</TradeID>
      <ExecutionTime>09:02:31</ExecutionTime>
      <ISIN>DE0007164600</ISIN>
      <Instrument>SAP SE</Instrument>
      <Side>Buy</Side>
      <Quantity>250</Quantity>
      <Price>198.45</Price>
      <Currency>EUR</Currency>
      <OrderType>Limit</OrderType>
      <TraderID>T-1042</TraderID>
      <DayViol>No</DayViol>
      <ViolationDetails/>
      <Status>Pass</Status>
    </Trade>
    <Trade>
      <TradeID>XTR-20260610-00312</TradeID>
      <ExecutionTime>10:15:44</ExecutionTime>
      <ISIN>DE0007236101</ISIN>
      <Instrument>Siemens AG</Instrument>
      <Side>Sell</Side>
      <Quantity>500</Quantity>
      <Price>176.20</Price>
      <Currency>EUR</Currency>
      <OrderType>Market</OrderType>
      <TraderID>T-2087</TraderID>
      <DayViol>Yes</DayViol>
      <ViolationDetails>Position limit exceeded — net short exposure beyond approved threshold</ViolationDetails>
      <Status>Violation</Status>
    </Trade>
  </Trades>
  <Summary>
    <TotalTrades>2</TotalTrades>
    <TotalVolume>137672.50</TotalVolume>
    <ViolationsFound>1</ViolationsFound>
    <OverallStatus>Violation</OverallStatus>
    <ExceptionFlag>Yes</ExceptionFlag>
  </Summary>
</XetraReport>
```

### XML Structure — Report B (Monthly Trader Summaries)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<XetraReport type="ReportTypeB" date="20260610">
  <Metadata>
    <ReportID>XETRA-MA-202606</ReportID>
    <GeneratedAt>2026-06-10T18:30:00</GeneratedAt>
    <ReportType>Monthly</ReportType>
    <CoveragePeriod>2026-06-01 to 2026-06-10</CoveragePeriod>
    <TradingVenue>XETR</TradingVenue>
    <MemberID>FRAUAS01</MemberID>
  </Metadata>
  <TraderSummaries>
    <Trader>
      <TraderID>T-1042</TraderID>
      <TraderName>Weber, Lukas</TraderName>
      <Desk>Equities</Desk>
      <TotalTrades>312</TotalTrades>
      <TotalVolume>4850000.00</TotalVolume>
      <AvgTradeSize>15544.87</AvgTradeSize>
      <TopInstrument>SAP SE (DE0007164600)</TopInstrument>
      <MonthViol>No</MonthViol>
      <ViolationCount>0</ViolationCount>
      <ViolationDetails/>
      <ComplianceRating>A</ComplianceRating>
      <Status>Pass</Status>
    </Trader>
  </TraderSummaries>
  <Summary>
    <TotalTraders>1</TotalTraders>
    <TotalTrades>312</TotalTrades>
    <TotalVolume>4850000.00</TotalVolume>
    <ViolationsFound>0</ViolationsFound>
    <OverallStatus>Pass</OverallStatus>
    <ExceptionFlag>No</ExceptionFlag>
  </Summary>
</XetraReport>
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

### Phase D: Status Evaluation
- **Report A (Daily):** XPath query checks `/XetraReport/Summary/OverallStatus` value
- **Report B (Monthly):** XPath query checks `/XetraReport/Summary/OverallStatus` value
- If either report has a status of `Violation`, the corresponding result is flagged

### Phase E: Evidence Storage
- XLSX evidence files are saved to `/Evidence Archive/Evidence/` (Report A and B separately)
- Original XML files are archived to `/Evidence Archive/XML Archive/`
- The raw XML content is written to the respective evidence spreadsheet for audit review

### Phase F: Exception Gate & Completion
- **Violation detected:** SharePoint → `Exception`, email to supervisor (priority: High)
- **No violation:** SharePoint → `Completed`, confirmation email to standard distribution

### Flow Validation & Routing Logic

```
┌──────────────────────────────────────────────────────────────────┐
│  Read Status:                                                    │
│  - Report A: /XetraReport/Summary/OverallStatus                  │
│  - Report B: /XetraReport/Summary/OverallStatus                  │
│                                                                  │
│  Evaluate:                                                       │
│  - If A or B == "Violation" → OverallStatus = Exception          │
│  - Else                     → OverallStatus = Completed          │
└──────────────────────────────────────────────────────────────────┘
```

---

## 5. Test Data & Simulations

The repository contains scripts for a complete offline simulation of the Power Automate flow.

### Running the Simulation

```bash
# 1. Install dependencies
pip install python-pptx openpyxl

# 2. Generate Xetra test runs (30 days, reproducible)
python3 scripts/simulate_runs.py --count 30 --seed 42

# 3. Local processing (simulates the Power Automate flow, outputs XLSX)
python3 scripts/local_flow_processor.py

# 4. Generate consolidated findings presentation
python3 scripts/generate_findings_presentation.py

# 5. Run the visual walkthrough video recorder
python3 scripts/demo_flow.py --run 1
```

### Evidence Output

Each run generates:
- `evidence_ReportTypeA.xlsx` — Professional, styled trade compliance spreadsheet
- `evidence_ReportTypeB.xlsx` — Professional, styled monthly trader summary spreadsheet
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
│   ├── build_boardroom_deck.py        ← Creates the boardroom deck
│   └── demo_flow.py                   ← Interactive flow preview demo script
│
├── tests/
│   ├── runs/                          ← Generated test runs (run_1..run_30)
│   │   └── run_N/
│   │       ├── YYYYMMDD_ReportTypeA.xml
│   │       ├── YYYYMMDD_ReportTypeB.xml
│   │       ├── YYYYMMDD_Reports.zip
│   │       ├── evidence_ReportTypeA.xlsx  ← XLSX trade evidence
│   │       ├── evidence_ReportTypeB.xlsx  ← XLSX trader summary evidence
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

- **Project Team ISAAI** — Frankfurt University of Applied Sciences
- Modules: ISA (Information Systems Architecture) & A+I (Architecture & Integration)
- Semester: Summer Semester 2026
