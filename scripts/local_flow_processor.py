#!/usr/bin/env python3
"""ISAAI Local Flow Ingestion & Processing Simulator.

Simulates the Power Automate (Microsoft Flow) logic completely offline:
1. Extracts ZIP attachments from tests/runs/ directories.
2. Parses the XML data — Report A uses DayViol, Report B uses MonthViol.
3. Evaluates the two-step validation rules (Marker = 'V', Threshold < 50).
4. Generates XLSX evidence files (matching SharePoint storage format).
5. Logs all results into a local CSV mimicking the SharePoint List schema.

Status values match SharePoint dropdown schema:
  ReportA_Status / ReportB_Status: Pass, Violation, Error, Pending
  OverallStatus: Completed, Exception, Processing, Failed
  ExceptionFlag: Yes, No
"""

import os
import sys
import zipfile
import csv
from datetime import datetime
from pathlib import Path

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
except ImportError:
    print("Error: openpyxl is required. Install it with: pip install openpyxl")
    sys.exit(1)

# Setup paths relative to the script location
ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = ROOT / "tests"
RUNS_DIR = TESTS_DIR / "runs"

# Ensure folders exist
TESTS_DIR.mkdir(parents=True, exist_ok=True)

# SharePoint List CSV schema (matches Email_Report_Schema.xlsx)
SHAREPOINT_LOG_CSV = TESTS_DIR / "Report_Processing_Log_Local.csv"
CSV_COLUMNS = [
    "Title", "ReceivedDateTime", "SenderEmail", "ReportDate",
    "ReportA_Status", "ReportB_Status", "ReportA_ViolationDetails",
    "ReportB_ViolationDetails", "OverallStatus", "ExceptionFlag",
    "EvidenceA_Link", "EvidenceB_Link"
]

THRESHOLD_LIMIT = 50

# Excel styling constants
HEADER_FONT = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
HEADER_FILL = PatternFill(start_color='00335B', end_color='00335B', fill_type='solid')
PASS_FONT = Font(name='Calibri', size=11, color='2E7D32')
VIOLATION_FONT = Font(name='Calibri', size=11, color='D9383A', bold=True)
NORMAL_FONT = Font(name='Calibri', size=11)
THIN_BORDER = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)


def init_log_file():
    """Initializes the mock SharePoint List CSV locally (always fresh)."""
    with open(SHAREPOINT_LOG_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_COLUMNS)


def parse_xml_rules(xml_path, report_type):
    """Parses XML and evaluates the two-step validation rules.

    Report Type A checks <DayViol> marker.
    Report Type B checks <MonthViol> marker.
    """
    import xml.etree.ElementTree as ET
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        row = root.find(".//Row")
        if row is None:
            return "Error", "No Row data element found in XML", {}

        # Select the correct violation marker based on report type
        if report_type == "ReportTypeA":
            marker_elem = row.find("DayViol")
            marker_name = "DayViol"
        else:
            marker_elem = row.find("MonthViol")
            marker_name = "MonthViol"

        marker = marker_elem.text if marker_elem is not None else "N"

        # Read all threshold values
        thresholds = {}
        for i in range(1, 5):
            t_elem = row.find(f"Threshold{i}")
            if t_elem is not None:
                thresholds[f"Threshold{i}"] = int(t_elem.text)

        if marker != "V":
            return "Pass", f"No violation marker detected ({marker_name} = '{marker}')", thresholds

        # If marker is V, check secondary thresholds
        breaches = []
        for t_name, t_val in thresholds.items():
            if t_val < THRESHOLD_LIMIT:
                breaches.append(f"{t_name} ({t_val} < {THRESHOLD_LIMIT})")

        if breaches:
            return "Violation", f"Threshold breach: {', '.join(breaches)}", thresholds
        else:
            return "Pass", f"{marker_name} = 'V' but all thresholds healthy: {thresholds}", thresholds

    except Exception as e:
        return "Error", f"Failed to parse XML: {e}", {}


def generate_evidence_xlsx(run_dir, date_str, report_type, marker_name, status, details, thresholds):
    """Generates XLSX evidence file matching SharePoint storage format."""
    evidence_path = run_dir / f"evidence_{report_type}.xlsx"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"{report_type} Evidence"

    # Headers
    headers = ["Report Date", "Report Type", "Coverage Period", "Violation Marker",
               "Validation Status", "Threshold1", "Threshold2", "Threshold3",
               "Threshold4", "Breach Details"]
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal='center')
        cell.border = THIN_BORDER

    # Data row
    coverage = "Daily" if report_type == "ReportTypeA" else "Monthly"
    marker_val = "V" if status == "Violation" or "healthy" in details else "N"
    if "'V'" in details:
        marker_val = "V"

    # Read actual marker from details
    if "DayViol" in details or "MonthViol" in details:
        if "= 'V'" in details:
            marker_val = "V"
        elif "= 'N'" in details:
            marker_val = "N"

    data_row = [
        date_str,
        report_type,
        coverage,
        marker_val,
        status,
        thresholds.get("Threshold1", ""),
        thresholds.get("Threshold2", ""),
        thresholds.get("Threshold3", ""),
        thresholds.get("Threshold4", ""),
        details
    ]

    for col_idx, value in enumerate(data_row, 1):
        cell = ws.cell(row=2, column=col_idx, value=value)
        cell.font = NORMAL_FONT
        cell.border = THIN_BORDER
        cell.alignment = Alignment(horizontal='center')

        # Color-code status
        if col_idx == 5:  # Status column
            if value == "Violation":
                cell.font = VIOLATION_FONT
            elif value == "Pass":
                cell.font = PASS_FONT

    # Auto-fit column widths
    for col in ws.columns:
        max_length = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max(max_length + 4, 14)

    wb.save(evidence_path)
    return evidence_path


def process_run(run_path):
    """Ingests a single run directory, extracting ZIP and running validation."""
    # Find ZIP file
    zip_files = list(run_path.glob("*.zip"))
    if not zip_files:
        print(f"Skipping {run_path.name}: No ZIP found.")
        return None

    zip_path = zip_files[0]
    date_str = zip_path.name.split("_")[0]

    # Extract ZIP contents to run directory
    with zipfile.ZipFile(zip_path, "r") as zipf:
        zipf.extractall(run_path)

    xml_a = run_path / f"{date_str}_ReportTypeA.xml"
    xml_b = run_path / f"{date_str}_ReportTypeB.xml"

    if not xml_a.exists() or not xml_b.exists():
        print(f"Skipping {run_path.name}: XML files missing from package.")
        return None

    # Execute validation — Report A uses DayViol, Report B uses MonthViol
    status_a, details_a, thresh_a = parse_xml_rules(xml_a, "ReportTypeA")
    status_b, details_b, thresh_b = parse_xml_rules(xml_b, "ReportTypeB")

    # Generate XLSX evidence files
    evidence_a = generate_evidence_xlsx(
        run_path, date_str, "ReportTypeA", "DayViol", status_a, details_a, thresh_a
    )
    evidence_b = generate_evidence_xlsx(
        run_path, date_str, "ReportTypeB", "MonthViol", status_b, details_b, thresh_b
    )

    # Determine overall status using SharePoint dropdown values
    has_violation = (status_a == "Violation" or status_b == "Violation")
    overall_status = "Exception" if has_violation else "Completed"
    exception_flag = "Yes" if has_violation else "No"

    # Log Row matching SharePoint schema
    log_row = {
        "Title": f"Financial Report Ingestion - {date_str}",
        "ReceivedDateTime": datetime.now().isoformat() + "Z",
        "SenderEmail": "automated-testing@fra-uas.de",
        "ReportDate": date_str,
        "ReportA_Status": status_a,
        "ReportB_Status": status_b,
        "ReportA_ViolationDetails": details_a,
        "ReportB_ViolationDetails": details_b,
        "OverallStatus": overall_status,
        "ExceptionFlag": exception_flag,
        "EvidenceA_Link": str(evidence_a.relative_to(ROOT)),
        "EvidenceB_Link": str(evidence_b.relative_to(ROOT)),
    }

    return log_row


def main():
    init_log_file()

    if not RUNS_DIR.exists():
        print("Error: No test runs found. Please run scripts/simulate_runs.py first.")
        sys.exit(1)

    run_folders = sorted(list(RUNS_DIR.glob("run_*")))
    print(f"Found {len(run_folders)} runs to process locally.")

    processed_count = 0
    logged_rows = []

    for run_folder in run_folders:
        row = process_run(run_folder)
        if row:
            logged_rows.append(row)
            processed_count += 1

    # Write logged rows to SharePoint-schema CSV
    with open(SHAREPOINT_LOG_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        for row in logged_rows:
            writer.writerow(row)

    print(f"\nProcessing complete: {processed_count} runs ingested locally.")
    print(f"Local database list logged to: {SHAREPOINT_LOG_CSV.relative_to(ROOT)}")
    print(f"Evidence XLSX files generated in each run directory.")


if __name__ == "__main__":
    main()
