# ISAAI — Automatic Report Documentation

## Final Report

**Project:** ISAAI — Automated Report Processing and Documentation
**Modules:** ISA (Information Systems Architecture) and A+I (Architecture and Integration)
**University:** Frankfurt University of Applied Sciences — Faculty 2
**Semester:** Summer Semester 2026
**Project Team:** Christina Malki, Altay Hennig, Sarah Bullinger
**Supervisor:** Prof. Dr. Dominik Dietrich
**Date:** July 2026

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Management Summary](#2-management-summary)
3. [Problem Description](#3-problem-description)
4. [Solution Design](#4-solution-design)
5. [Challenges](#5-challenges)
6. [Lessons Learned and Findings](#6-lessons-learned-and-findings)
7. [Outcome and Conclusion](#7-outcome-and-conclusion)
8. [BPMN Model with Camunda](#8-bpmn-model-with-camunda)
9. [Magic Charts](#9-magic-charts)
10. [Attachments](#10-attachments)
11. [Sources](#11-sources)

---

## 1. Introduction

The **ISAAI (Information Systems Architecture and Integration)** project was conducted as part of the modules *ISA (Information Systems Architecture)* and *A+I (Architecture and Integration)* at the Frankfurt University of Applied Sciences in the summer semester of 2026. It addresses the automation of the daily processing of structured financial reports received as XML files in ZIP archives via email.

### 1.1 Project Context

In the daily business operations of a financial service provider, two types of reports (Report Type A — Daily Trades and Report Type B — Monthly Trader Summaries) are received daily from a trading platform (Xetra). These reports contain compliance-relevant trading and trader data, which must be checked for rule violations and subsequently archived.

The manual process — extraction, compliance check, evidence archiving, and supervisor escalation — is replaced by a fully automated Microsoft Power Automate Flow.

### 1.2 Dual-Module Approach

The project pursues a dual-module approach that integrates the requirements of both courses:

| Module | Focus | Technology |
|-------|-------|-------------|
| **ISA** | Enterprise Architecture, ArchiMate Modeling, Invoice OCR, Chart Automation | ArchiMate 3.1, PDF/OCR, PowerPoint |
| **A+I** | Operative Process Automation, XML/GOAL Validation, Exception Governance | Power Automate, SharePoint, BPMN 2.0 |

### 1.3 Project Goal (SMART)

| S | M | A | R | T |
|---|---|---|---|---|
| Report A/B XML Pipeline + parallel ISA Invoice Pipeline | End-to-End Automation for the standard path; Exceptions measurable | GitHub CI/CD, Mock APIs, existing BPMN/ArchiMate models | White-box interfaces; Audit Trail; 30–40 min/day time savings | Deadline June 30, 2026 |

### 1.4 Project Organization

| Role | Person / Unit |
|-------|-----------------|
| Sponsor and Academic Lead | Prof. Dr. Dominik Dietrich — FRA UAS / FB2 |
| Architecture and Software Engineering | Christina Malki, Altay Hennig — Modules ISA and A+I |
| Operative Owner | Sarah Bullinger — Project Management Operations |

---

## 2. Management Summary

### Initial Situation

The existing process for the daily processing of financial reports (Report Type A and Report Type B) requires **30–40 minutes of manual effort** every day. An employee opens incoming emails, extracts ZIP attachments, imports XML data into a spreadsheet, visually checks thresholds, and manually creates evidence documents. This process carries significant risks: incorrect field selection, inconsistent results, forgotten archiving steps, and a lack of system-enforced upload-to-sign-off processes.

### Solution

The ISAAI system replaces the entire manual process with a fully automated **Microsoft Power Automate Cloud Flow**, which covers the following steps:

1. **Email Trigger:** Automatic detection of incoming emails with the subject "Financial Report" and a ZIP attachment.
2. **ZIP Extraction and XML Parsing:** Automatic unpacking and parallel validation of both report types.
3. **Rule-Based Compliance Check:** XPath-based evaluation of violation markers (DayViol and MonthViol).
4. **Evidence Generation:** Automatic creation of professional XLSX evidence documents.
5. **Exception Governance:** Supervisor escalation only when violations are detected (Human-in-the-Loop).
6. **SharePoint Audit Trail:** Seamless documentation of all processing steps.

### Result

Full automation eliminates daily manual effort while ensuring full auditability and human control for exceptions. The architecture was systematically documented according to the ArchiMate three-stage model **CURRENT → VISION → GOAL** and underpinned with BPMN 2.0 process models.

### Core Question of the Project

> *Can the daily manual effort of 30–40 minutes be eliminated while maintaining full auditability and human control for exceptions?*

**Answer: Yes.** The implemented solution fully automates the entire standard path. Human intervention is only required for compliance violations — in the sense of a human-in-the-loop governance model.

---

## 3. Problem Description

### 3.1 As-Is State (CURRENT State)

In the current state, daily financial reports are processed entirely manually. The process includes the following steps:

1. **Email Receipt:** An employee daily receives emails with ZIP attachments containing XML reports.
2. **Manual Extraction:** ZIP archives are manually unpacked and the contained XML files are reviewed.
3. **Table Import:** The XML data is manually imported into a spreadsheet.
4. **Visual Check:** Thresholds and violation markers are checked visually.
5. **Evidence Creation:** Evidence documents are manually created and formatted.
6. **Archiving:** Documents are filed and approved in the document management system.

#### ArchiMate CURRENT — Manual Daily Flow

![CURRENT — Manual Daily Flow](Architecture/CURRENT%20Architecture/CURRENT%20-%20Manual%20Daily%20Flow.png)

#### ArchiMate CURRENT — Workplace and Evidence Landscape

![CURRENT — Workplace and Evidence Landscape](Architecture/CURRENT%20Architecture/CURRENT%20-%20Workplace%20and%20Evidence%20Landscape.png)

### 3.2 Identified Weaknesses

| Weakness | Description | Impact |
|---------------|-------------|------------|
| **High Time Expenditure** | 30–40 minutes of daily manual effort | Loss of productivity, resource binding |
| **Media Break** | Switching between Collaboration Storage and Document Repository | Susceptibility to errors, loss of information |
| **Lack of System Enforcement** | No system-supported upload-to-sign-off process | Compliance risk, lack of traceability |
| **Human Errors** | Incorrect fields, inconsistent outputs, forgotten steps | Quality defects, audit risks |
| **Scaling Problem** | Manual process does not scale with increasing report volume | Capacity bottlenecks during peak loads |

### 3.3 Risk and Control Gap

Manual processing multiplies traceability gaps and increases the risk of unauthorized changes or overlooked violations. The lack of automation and a non-standardized audit trail exacerbate this problem.

### 3.4 Report Types

Two report types are processed daily, each with a specific compliance marker:

| Attribute | Report Type A (Daily) | Report Type B (Monthly) |
|----------|----------------------|------------------------|
| **Coverage Period** | Previous business day (Trade-Level Detail) | Month-to-Date cumulative trader summary |
| **Delivery Frequency** | Daily, at the agreed processing time | Daily, together with Report Type A |
| **Violation Marker** | DayViol | MonthViol |
| **Purpose** | Detection of same-day trade exceptions | Tracking monthly cumulative trader breach trends |

---

## 4. Solution Design

### 4.1 Architecture Evolution: CURRENT → VISION → GOAL

The project follows the ArchiMate three-stage approach to systematically document the transformation from the manual as-is state to the automated target state.

#### 4.1.1 VISION (Target Architecture)

The VISION describes the planned architecture after automation: email ingestion, rule-based validation, automatic evidence generation, and supervisor escalation only for exceptions (Human-in-the-Loop). A DMS integration via UI scraping was additionally planned in the VISION.

**ArchiMate VISION — Automated Target Architecture:**

![VISION — Automated Architecture](Architecture/VISION%20Architecture/Bildschirmfoto%202026-06-26%20um%2017.51.07.png)

#### 4.1.2 GOAL (Realized State)

The GOAL state represents the actually implemented solution — the full Power Automate Flow with SharePoint integration, parallel XML validation, and automatic XLSX evidence file generation. The DMS integration was deliberately removed from the scope; SharePoint serves as the sole Evidence Repository.

**ArchiMate GOAL — Realized Architecture:**

![GOAL — Realized Architecture](Architecture/GOAL%20Architecture/Bildschirmfoto%202026-06-26%20um%2017.56.03.png)

### 4.2 Power Automate Flow — Technical Architecture

The flow **ISAAI – Daily Report Processing** is structured into six phases and is available as an importable Power Automate package in the repository under:

```
src/flow/ISAAI-DailyReportProcessing_20260625165442.zip
```

#### Phase A: Trigger and Variable Initialization
- **Trigger:** New email with subject "Financial Report" + ZIP attachment
- **Variables:** LogItemID, ReportDate, ReportA_Result, ReportB_Result, ReportA_Details, ReportB_Details

#### Phase B: SharePoint List Entry
- Creates a new entry in the SharePoint list **Report Processing Log**
- Sets OverallStatus = Processing

#### Phase C: ZIP Extraction and XML Reading
- Extracts ZIP attachment to OneDrive /Evidence Archive/Temp/
- Reads ReportTypeA.xml and ReportTypeB.xml as text content

#### Phase D: Parallel Validation (Status Evaluation)
- **Report A (Daily):** XPath query checks /XetraReport/Summary/OverallStatus
- **Report B (Monthly):** XPath query checks /XetraReport/Summary/OverallStatus
- In case of status "Violation", the corresponding result is marked

```
+------------------------------------------------------------------+
|  Read Status:                                                     |
|  - Report A: /XetraReport/Summary/OverallStatus                  |
|  - Report B: /XetraReport/Summary/OverallStatus                  |
|                                                                   |
|  Evaluate:                                                        |
|  - If A or B == "Violation" -> OverallStatus = Exception          |
|  - Else                     -> OverallStatus = Completed          |
+------------------------------------------------------------------+
```

#### Phase E: Evidence Saving
- XLSX evidence files are saved in /Evidence Archive/Evidence/ (Report A and B separately)
- Original XML files are archived in /Evidence Archive/XML Archive/
- The raw XML content is written into the respective evidence spreadsheet

#### Phase F: Exception Gate and Conclusion
- **Violation detected:** SharePoint -> Exception, Email to Supervisor (Priority: High)
- **No Violation:** SharePoint -> Completed, Confirmation email to standard distribution list

### 4.3 SharePoint Schema — Report Processing Log

The SharePoint list **Report Processing Log** serves as the central audit trail:

| Column | Type | Description |
|--------|-----|-------------|
| Title | Text | Email subject |
| ReceivedDateTime | Date/Time | Time of receipt |
| SenderEmail | Text | Sender address |
| ReportDate | Text | Report date (from filename) |
| ReportA_Status | Choice | Pass / Violation / Error / Pending |
| ReportB_Status | Choice | Pass / Violation / Error / Pending |
| ReportA_ViolationDetails | Multiline Text | Violation details |
| ReportB_ViolationDetails | Multiline Text | Violation details |
| OverallStatus | Choice | Completed / Exception / Processing / Failed |
| ExceptionFlag | Yes/No | Escalation triggered? |
| EvidenceA_Link | Hyperlink | Link to Report A evidence (.xlsx) |
| EvidenceB_Link | Hyperlink | Link to Report B evidence (.xlsx) |

### 4.4 XML Structures

#### Report A — Daily Trades

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
      <ViolationDetails>Position limit exceeded - net short exposure beyond approved threshold</ViolationDetails>
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

#### Report B — Monthly Trader Summaries

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

### 4.5 Technology Stack

| Component | Technology |
|-----------|-------------|
| Automation | Microsoft Power Automate (Cloud Flow) |
| Data Storage | SharePoint Online (Lists + Document Library) |
| Evidence Format | XLSX (Excel) |
| Architecture Modeling | ArchiMate 3.1 (Archi) |
| Process Modeling | BPMN 2.0 |
| Local Simulation | Python 3, openpyxl, python-pptx |
| Version Control | Git / GitHub |

---

## 5. Challenges

### 5.1 Technical Challenges

#### Power Automate — Complex Branching Logic

Implementing parallel validation paths (Report A and Report B simultaneously) in Power Automate posed a significant challenge. The Copilot import could not import complex branching flows flawlessly, so the flow had to be built manually in the Power Automate Designer (see docs/guides/SHAREPOINT_FLOW_GUIDE.md).

#### XPath Parsing in Power Automate

Using XPath expressions within Power Automate to extract XML fields required specific syntax adjustments. In particular, converting XPath results to integer values for threshold comparisons was non-trivial:

```
int(xpath(xml(outputs('XML_A_Content')), 'string(/Report/Data/Row/Threshold1)'))
```

#### ZIP Extraction and File Handling

Automatically extracting ZIP attachments from emails and subsequently reading the contained XML files required precise orchestration of OneDrive for Business actions, as temporary files had to be correctly extracted, read, and then cleaned up.

### 5.2 Architectural Challenges

#### DMS Integration (Out of Scope)

The original VISION envisioned integration with the company's internal Document Management System (DMS), including UI scraping/RPA. This integration was deliberately removed from the GOAL scope because:

- UI scraping is fragile and requires high maintenance
- No stable API to the DMS was available
- SharePoint fully meets the requirements as the sole Evidence Repository

#### Three-Stage Architecture Model

Consistently modeling the transformation path CURRENT, VISION, GOAL in ArchiMate and BPMN required a clear delineation of architecture layers and careful coordination between Enterprise Architecture (ISA) and operative process automation (A+I).

### 5.3 Organizational Challenges

#### Dual-Module Coordination

Handling the requirements of two modules (ISA and A+I) with different focus areas in parallel required a clear separation of responsibilities and simultaneous integration at the repository level. The branching strategy (feature/isa-module and feature/ai-module) enabled parallel development with controlled integration.

#### Time Synchronization

The tight timeline (May–June 2026) required strict phasing and parallel work on both modules. Integrating both modules into a coherent overall system under time pressure was a central organizational challenge.

---

## 6. Lessons Learned and Findings

### 6.1 Architecture and Modeling

**Finding 1: ArchiMate as a bridge between strategy and implementation.**
The ArchiMate three-stage model (CURRENT, VISION, GOAL) has proven to be an excellent communication tool to transparently present the transformation path from the manual to the automated solution. The separation of VISION (what do we want) and GOAL (what have we realized) forces a conscious scope decision.

**Finding 2: BPMN as an operative validation instrument.**
BPMN modeling on three levels (CURRENT, VISION, GOAL) with lanes served not only for documentation but as an active validation tool for the Power Automate implementation. Discrepancies between the BPMN model and flow implementation could be detected early on.

### 6.2 Technology and Automation

**Finding 3: Power Automate is suitable for standardized processes.**
For the defined use case — email trigger, ZIP extraction, XML parsing, rule-based validation, and SharePoint storage — Power Automate has proven to be a suitable low-code platform. Its limits lie in complex logic and parallel branching.

**Finding 4: SharePoint as a lightweight audit trail system.**
The combination of a SharePoint list (structured metadata) and a SharePoint document library (evidence files) provides a pragmatic yet effective audit trail system. For production environments with higher compliance requirements, a dedicated database would be recommended.

**Finding 5: Local simulation as a development accelerator.**
The Python-based local simulation of the Power Automate Flow (local_flow_processor.py) enabled rapid iteration and validation of the processing logic without relying on the cloud environment. Reproducible test data generation (simulate_runs.py --count 30 --seed 42) was essential for quality assurance.

### 6.3 Process and Organization

**Finding 6: Dual-module projects require clear interface definitions.**
Working on two modules (ISA and A+I) in parallel only works with clearly defined interfaces and a shared repository structure. The Influence Matrix (ISA vs. A+I) proved to be a useful governance tool.

**Finding 7: Human-in-the-Loop as a governance pattern.**
The conscious decision to involve a human supervisor in the event of violations (instead of a fully automated escalation) complies with the requirements of the EU AI Act and ensures that compliance-critical decisions are not entirely delegated to machines.

### 6.4 Compliance and Data Privacy

**Finding 8: GDPR Compliance through Pseudonymization.**
Personally Identifiable Information (PII) is pseudonymized before any internal processing. CI/CD logs use exclusively mock data. This approach is minimally invasive and GDPR-compliant.

**Finding 9: EU AI Act — Human-in-the-Loop is mandatory.**
If an LLM supports exception reviews, human intervention is strictly required before handover to the archive. This principle was anchored in the GOAL process model.

---

## 7. Outcome and Conclusion

### 7.1 Project Result

The ISAAI project achieved all defined goals:

| Goal | Status | Description |
|------|--------|-------------|
| Full automation of the standard path | Achieved | Email, ZIP, XML, Validation, Evidence, SharePoint, Notification |
| Exception Governance | Achieved | Human-in-the-loop for violations with supervisor escalation |
| Audit Trail | Achieved | Seamless documentation in SharePoint list + document library |
| ArchiMate Modeling (3 stages) | Achieved | CURRENT, VISION, GOAL each as ArchiMate models (.archimate) |
| BPMN Process Modeling (3 stages) | Achieved | CURRENT, VISION, GOAL each as BPMN diagrams (.bpmn) |
| Power Automate Flow | Achieved | Importable flow package in the repository |
| Local Simulation | Achieved | 30 reproducible test runs with Python scripts |
| ISA Module (parallel) | Achieved | Invoice OCR, JSON/CSV, Chart Automation |
| Presentation Material | Achieved | Consolidated Findings Deck + Module Presentations |

### 7.2 Quantitative Benefits

| Metric | Before (CURRENT) | After (GOAL) | Improvement |
|--------|-----------------|----------------|-------------|
| Daily manual effort | 30–40 min | 0 min (Standard) / approx. 5 min (Exception) | 100% / 85% |
| Error rate (human errors) | High | Near zero (automated) | Over 95% reduction |
| Lead time per report | approx. 40 min | approx. 2 min (automated) | 95% faster |
| Audit trail completeness | Patchy | 100% system-supported | Complete |
| Scalability | Limited (1 person) | Hundreds of emails/day | Unlimited |

### 7.3 Milestones

| Milestone | Deliverables | Date | Status |
|-------------|-------------|-------|--------|
| M1: Requirements and Setup | Briefing analysis; Report A/B vs. ISA Split; GitHub repo structure | May 24, 2026 | Done |
| M2: ISA Module (parallel) | Invoice OCR Pipeline, JSON/CSV schema, Chart generation | Jun 01, 2026 | Done |
| M3: A+I Architecture and Process | CURRENT/VISION/GOAL ArchiMate; CURRENT/GOAL BPMN | Jun 15, 2026 | Done |
| M4: Power Automate Design | PA Prompt; SharePoint List schema; Evidence Library design | Jun 25, 2026 | Done |
| M5: Integration and Tests | Branch merge; E2E test; Flow deployment | Jun 28, 2026 | Done |
| M6: Submission and Docs | Main branch, Boardroom Deck, Charter (LaTeX/PDF), Presentation | Jun 30, 2026 | Done |

### 7.4 Conclusion

The ISAAI project successfully demonstrates how the combination of enterprise architecture methodology (ArchiMate, BPMN) and low-code automation (Power Automate, SharePoint) can completely transform an operational process. The systematic documentation of the transformation path CURRENT, VISION, GOAL ensures that architectural decisions remain traceable and the solution remains maintainable.

The deliberate scope reduction from VISION to GOAL (excluding DMS integration) also shows that pragmatic architecture decisions are just as important in a university project as they are in corporate practice. The SharePoint-based solution meets all functional requirements while providing a solid foundation for future enhancements.

---

## 8. BPMN Model with Camunda

### 8.1 Overview of BPMN Models

The project includes BPMN 2.0 process models for all three architecture stages. The models were created using a BPMN 2.0-compatible tool and are available as .bpmn files in the repository.

### 8.2 BPMN CURRENT — As-Is Process

The CURRENT BPMN model maps the manual as-is process with swim lanes. The lanes represent the involved roles (Employee, Supervisor, System).

**BPMN CURRENT — Operative Process View (Lanes):**

![BPMN CURRENT — Validation Process with Lanes](Process%20Modeling/CURRENT%20Process/daily_financial_report_validation_lanes_CURRENT.png)

**Process Steps:**

1. Receive email with ZIP attachment
2. Manually unpack ZIP
3. Import XML into spreadsheet
4. Visually check violation markers
5. Manually create evidence document
6. Archiving in DMS
7. Send email summary

**File:** docs/Documentation/Process Modeling/CURRENT Process/daily_financial_report_validation_lanes_CURRENT.bpmn

### 8.3 BPMN VISION — Target Process

The VISION BPMN model describes the targeted automated process including DMS integration and strategic governance.

**BPMN VISION — Operative Automation (Lanes):**

![BPMN VISION — Operative Automation Flow](Process%20Modeling/VISION%20Process/daily_financial_report_validation_lanes_OPERATION%20VISION.png)

**BPMN VISION — Strategic Governance:**

![BPMN VISION — Strategic Governance](Process%20Modeling/VISION%20Process/Strategic_Governance_Process.png)

**Files:**
- docs/Documentation/Process Modeling/VISION Process/daily_financial_report_validation_lanes_OPERATIVE VISION.bpmn
- docs/Documentation/Process Modeling/VISION Process/Strategic_Governance_Process.bpmn

### 8.4 BPMN GOAL — Realized Process

The GOAL BPMN model describes the actually implemented process using Power Automate and SharePoint.

**BPMN GOAL — Strategic Validation Process (Lanes):**

![BPMN GOAL — Strategic Validation Process](Process%20Modeling/GOAL%20Process/daily_financial_report_validation_lanes_Strategic%20GOAL%20Kopie.bpmn.png)

**Files:**
- docs/Documentation/Process Modeling/GOAL Process/daily_financial_report_validation_lanes_OPERATIVE GOAL.bpmn
- docs/Documentation/Process Modeling/GOAL Process/daily_financial_report_validation_lanes_Strategic GOAL Kopie.bpmn

### 8.5 BPMN Validation Videos

Validation videos are available for the GOAL process demonstrating both paths (Violation YES / Violation NO):

- BPMN GOAL - Rule Violation NO.mov
- BPMN GOAL - Rule violation YES.mov

### 8.6 BPMN Elements and Notation

The BPMN models use the following core elements:

| BPMN Element | Use in Project |
|-------------|----------------------|
| **Pool / Lanes** | Roles: Employee, Supervisor, System (Power Automate) |
| **Start Event** | Email receipt with ZIP attachment |
| **End Event** | Conclusion (Completed / Exception) |
| **Exclusive Gateway (XOR)** | Violation check (Yes/No) |
| **Parallel Gateway (AND)** | Parallel validation of Report A + B |
| **Service Task** | Automated actions (ZIP extraction, XML parsing, evidence creation) |
| **User Task** | Supervisor review for exceptions |
| **Data Object** | XML reports, XLSX evidence, SharePoint entries |
| **Message Event** | Email notifications |

---

## 9. Magic Charts

### 9.1 Concept

The **Magic Charts** system is part of the ISA module and automates the creation of visualizations and presentations from processed financial data. It transforms raw data from XML reports into professional, meaningful charts and presentation slides.

### 9.2 Implemented Scripts

#### 9.2.1 Test Data Generation (simulate_runs.py)

Generates reproducible mock XML/ZIP test data for 30 days:

```bash
python3 scripts/simulate_runs.py --count 30 --seed 42
```

**Output per run:**
- YYYYMMDD_ReportTypeA.xml — Daily trade report
- YYYYMMDD_ReportTypeB.xml — Monthly trader summary report
- YYYYMMDD_Reports.zip — ZIP archive of both reports

#### 9.2.2 Local Flow Processing (local_flow_processor.py)

Simulates the full Power Automate Flow offline and generates professionally styled evidence files:

```bash
python3 scripts/local_flow_processor.py
```

**Output per run:**
- evidence_ReportTypeA.xlsx — Professionally formatted trade compliance spreadsheet
- evidence_ReportTypeB.xlsx — Professionally formatted monthly trader summary spreadsheet
- summary.txt — Human-readable validation summary

#### 9.2.3 Consolidated Findings Presentation (generate_findings_presentation.py)

Generates a consolidated findings presentation across all test runs:

```bash
python3 scripts/generate_findings_presentation.py
```

**Output:**
- presentations/ISAAI-Consolidated-Findings.pptx — PowerPoint deck with aggregated results

#### 9.2.4 Boardroom Deck (build_boardroom_deck.py)

Creates a management-ready boardroom presentation:

```bash
python3 scripts/build_boardroom_deck.py
```

#### 9.2.5 Demo Flow (demo_flow.py)

Interactive flow run with visual output:

```bash
python3 scripts/demo_flow.py --run 1
```

### 9.3 Evidence Output Format

The generated XLSX evidence files contain professionally styled tables with:

- **Report Type A:** Trade ID, Execution Time, ISIN, Instrument, Side, Quantity, Price, Currency, Order Type, Trader ID, DayViol, Violation Details, Status
- **Report Type B:** Trader ID, Trader Name, Desk, Total Trades, Total Volume, Avg Trade Size, Top Instrument, MonthViol, Violation Count, Compliance Rating, Status

### 9.4 SharePoint Integration

Evidence files are automatically linked to the SharePoint list. The SharePoint status information follows a defined value range:

| Column | Allowed Values |
|--------|---------------|
| ReportA_Status / ReportB_Status | Pass, Violation, Error, Pending |
| OverallStatus | Completed, Exception, Processing, Failed |
| ExceptionFlag | Yes, No |

---

## 10. Attachments

### 10.1 Repository Structure

```
ISAAI-Automatic-Report-Documentation/
|
+-- README.md                          <- Project report (Main documentation)
|
+-- docs/
|   +-- Documentation/
|   |   +-- Architecture/
|   |   |   +-- CURRENT Architecture/  <- ArchiMate As-Is State
|   |   |   |   +-- CURRENT - Manual Daily Flow.png
|   |   |   |   +-- CURRENT - Workplace and Evidence Landscape.png
|   |   |   |   +-- report-processing-CURRENT.archimate
|   |   |   +-- VISION Architecture/   <- ArchiMate Target Architecture
|   |   |   |   +-- Archimate Vision 1.archimate
|   |   |   |   +-- Bildschirmfoto 2026-06-26 um 17.51.07.png
|   |   |   |   +-- report-processing-GOAL.archimate
|   |   |   +-- GOAL Architecture/     <- ArchiMate Realized State
|   |   |       +-- Archimate Goal 1.archimate
|   |   |       +-- Bildschirmfoto 2026-06-26 um 17.56.03.png
|   |   +-- Process Modeling/
|   |   |   +-- CURRENT Process/       <- BPMN As-Is Process
|   |   |   |   +-- daily_financial_report_validation_lanes_CURRENT.bpmn
|   |   |   |   +-- daily_financial_report_validation_lanes_CURRENT.png
|   |   |   +-- VISION Process/        <- BPMN Target Process
|   |   |   |   +-- daily_financial_report_validation_lanes_OPERATIVE VISION.bpmn
|   |   |   |   +-- daily_financial_report_validation_lanes_OPERATION VISION.png
|   |   |   |   +-- Strategic_Governance_Process.bpmn
|   |   |   |   +-- Strategic_Governance_Process.png
|   |   |   +-- GOAL Process/          <- BPMN Realized Process
|   |   |       +-- daily_financial_report_validation_lanes_OPERATIVE GOAL.bpmn
|   |   |       +-- daily_financial_report_validation_lanes_Strategic GOAL Kopie.bpmn
|   |   |       +-- daily_financial_report_validation_lanes_Strategic GOAL Kopie.bpmn.png
|   |   |       +-- BPMN GOAL - Rule Violation NO.mov
|   |   |       +-- BPMN GOAL - Rule violation YES.mov
|   |   +-- Project-Charter-ISAAI.tex  <- Project Charter (LaTeX)
|   |   +-- Project_Charter_ISAAI.pdf  <- Project Charter (PDF)
|   |   +-- ISAAI_Abschlussbericht.md  <- This final report
|   |   +-- roadmap.md                 <- Phase plan
|   |   +-- issue-list.md              <- Task list
|   +-- guides/
|       +-- SHAREPOINT_FLOW_GUIDE.md   <- Step-by-step Flow Setup Guide
|
+-- src/
|   +-- flow/
|   |   +-- ISAAI-DailyReportProcessing_*.zip      <- Importable Flow Package
|   |   +-- ISAAI-DailyReportProcessing_*/          <- Unpacked Flow Definition
|   |       +-- manifest.json
|   |       +-- Microsoft.Flow/flows/.../
|   |           +-- definition.json                 <- Full Flow Logic
|   |           +-- apisMap.json
|   |           +-- connectionsMap.json
|   +-- presets/
|   |   +-- ReportTypeA_Daily_Template.xml          <- Daily Report XML Preset
|   |   +-- ReportTypeB_Monthly_Template.xml        <- Monthly Report XML Preset
|   |   +-- README.md                               <- Preset Documentation
|   +-- report_template/
|       +-- Report Processing Log (1).csv           <- SharePoint CSV Schema
|
+-- scripts/
|   +-- simulate_runs.py               <- Generates mock XML/ZIP test data
|   +-- local_flow_processor.py        <- Simulates the flow locally (offline)
|   +-- generate_findings_presentation.py  <- Creates consolidated findings PPTX
|   +-- build_boardroom_deck.py        <- Creates the boardroom deck
|   +-- demo_flow.py                   <- Interactive flow preview demo script
|   +-- build-charter-pdf.sh           <- Builds Charter PDF from LaTeX
|   +-- push-to-github.sh             <- GitHub Push Script
|   +-- verify-repo-sync.sh           <- Repository Sync Verification
|
+-- tests/
|   +-- runs/                          <- Generated test runs (run_1..run_30)
|   |   +-- run_N/
|   |       +-- YYYYMMDD_ReportTypeA.xml
|   |       +-- YYYYMMDD_ReportTypeB.xml
|   |       +-- YYYYMMDD_Reports.zip
|   |       +-- evidence_ReportTypeA.xlsx  <- XLSX Trade Evidence
|   |       +-- evidence_ReportTypeB.xlsx  <- XLSX Trader Summary Evidence
|   |       +-- summary.txt
|   +-- Report_Processing_Log_Local.csv  <- Local SharePoint Equivalent
|   +-- Email_Report_Schema (1).xlsx     <- SharePoint List Schema Definition
|
+-- presentations/
    +-- ISAAI-Consolidated-Findings.pptx  <- Consolidated Findings Deck
    +-- Local Demo Run video.mov          <- Demo Video
    +-- Project Presentation/
        +-- praesi isa 2906.pptx.pptx     <- ISA Module Presentation
        +-- praesi ai 2906.pptx.pptx      <- A+I Module Presentation
```

### 10.2 Import Guide — Power Automate Flow

1. Open Power Automate (https://make.powerautomate.com/)
2. Navigate to My Flows, Import, Import Package (Legacy)
3. Upload file src/flow/ISAAI-DailyReportProcessing_20260625165442.zip
4. Configure three connectors in the import wizard:
   - **Office 365 Outlook** — Select or create your own connection
   - **SharePoint** — Select or create your own connection
   - **OneDrive for Business** — Select or create your own connection
5. Click Import
6. Update SharePoint Site URL in the flow actions

**Prerequisite:** A SharePoint Site with the list "Report Processing Log" and the document library "Evidence Archive" must exist. See docs/guides/SHAREPOINT_FLOW_GUIDE.md for the full setup guide.

### 10.3 Central Project Documents

| Document | Path | Description |
|----------|------|-------------|
| Project Charter (PDF) | docs/Documentation/Project_Charter_ISAAI.pdf | Formal project mandate |
| Project Charter (LaTeX) | docs/Documentation/Project-Charter-ISAAI.tex | Source code of the project mandate |
| Roadmap | docs/Documentation/roadmap.md | Phase plan with 5 phases |
| Issue List | docs/Documentation/issue-list.md | Task list with 5 milestones |
| SharePoint Flow Guide | docs/guides/SHAREPOINT_FLOW_GUIDE.md | Step-by-step setup |
| Flow Package | src/flow/ISAAI-DailyReportProcessing_*.zip | Importable Power Automate Flow |
| ISA Presentation | presentations/Project Presentation/praesi isa 2906.pptx.pptx | ISA module presentation |
| A+I Presentation | presentations/Project Presentation/praesi ai 2906.pptx.pptx | A+I module presentation |

---

## 11. Sources

### 11.1 Technical References

1. **Microsoft Power Automate Documentation.** Microsoft Corporation. https://learn.microsoft.com/en-us/power-automate/
2. **SharePoint Online Documentation.** Microsoft Corporation. https://learn.microsoft.com/en-us/sharepoint/
3. **OneDrive for Business API Reference.** Microsoft Corporation. https://learn.microsoft.com/en-us/onedrive/developer/
4. **XPath Syntax Reference.** W3Schools. https://www.w3schools.com/xml/xpath_syntax.asp
5. **Office 365 Outlook Connector.** Microsoft Corporation. https://learn.microsoft.com/en-us/connectors/office365/

### 11.2 Architecture and Modeling

6. **ArchiMate 3.1 Specification.** The Open Group. https://pubs.opengroup.org/architecture/archimate3-doc/
7. **Archi — ArchiMate Modelling Tool.** https://www.archimatetool.com/
8. **BPMN 2.0 Specification.** Object Management Group (OMG). https://www.omg.org/spec/BPMN/2.0/
9. **Camunda BPMN Modeler.** Camunda Services GmbH. https://camunda.com/
10. **TOGAF Standard, 10th Edition.** The Open Group. https://www.opengroup.org/togaf

### 11.3 Compliance and Governance

11. **EU AI Act — Regulation (EU) 2024/1689.** European Parliament and Council. https://eur-lex.europa.eu/eli/reg/2024/1689/oj
12. **General Data Protection Regulation (GDPR) — Regulation (EU) 2016/679.** European Parliament and Council. https://eur-lex.europa.eu/eli/reg/2016/679/oj
13. **Human-in-the-Loop (HITL) Design Patterns.** ISO/IEC 22989:2022 — Artificial intelligence concepts and terminology.

### 11.4 Development Tools

14. **Python 3 Documentation.** Python Software Foundation. https://docs.python.org/3/
15. **openpyxl — A Python library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files.** https://openpyxl.readthedocs.io/
16. **python-pptx — Python library for creating PowerPoint files.** https://python-pptx.readthedocs.io/
17. **Git — Distributed Version Control System.** https://git-scm.com/
18. **GitHub — Collaborative Development Platform.** https://github.com/

### 11.5 Project Resources

19. **ISAAI GitHub Repository.** https://github.com/pollo60/-ISAAI-Automatic-Report-Documentation
20. **SharePoint Site — ISAAI Daily Report Processing.** https://studfrauasde.sharepoint.com/sites/ISAAIDailyReportProcessing

---

*Created as part of the modules ISA (Information Systems Architecture) and A+I (Architecture and Integration) — Frankfurt University of Applied Sciences, Summer Semester 2026.*
