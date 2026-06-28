#!/usr/bin/env python3
"""ISAAI Local Flow Ingestion & Processing Simulator.

Simulates the Power Automate (Microsoft Flow) logic completely offline:
1. Extracts ZIP attachments from tests/runs/ directories.
2. Parses the XML data using native XML parsing.
3. Evaluates the two-step validation rules (Marker = 'V', Threshold < 50).
4. Generates local CSV/Excel evidence sheets.
5. Populates a local PowerPoint run summary template.
6. Logs all results into a local CSV mimicking your SharePoint List schema.
"""

import os
import sys
import zipfile
import csv
from datetime import datetime
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# Setup paths relative to the script location
ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = ROOT / "tests"
RUNS_DIR = TESTS_DIR / "runs"
PRESENTATIONS_DIR = ROOT / "presentations" / "Automated Presentations"
TEMPLATES_DIR = ROOT / "src" / "report_template"

# Ensure folders exist
PRESENTATIONS_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

# List output database file matching SharePoint CSV schema
SHAREPOINT_LOG_CSV = TESTS_DIR / "Report_Processing_Log_Local.csv"
CSV_COLUMNS = [
    "Titel", "ReceivedDateTime", "SenderEmail", "ReportDate",
    "ReportA_Status", "ReportB_Status", "ReportA_ViolationDetails",
    "ReportB_ViolationDetails", "OverallStatus", "ExceptionFlag",
    "EvidenceA_Link", "EvidenceB_Link", "Presentation_Link"
]

THRESHOLD_LIMIT = 50

def setup_powerpoint_template():
    """Generates a default daily template pptx if none exists."""
    template_path = TEMPLATES_DIR / "daily_run_template.pptx"
    if template_path.exists():
        return template_path

    print("Generating default PowerPoint template locally...")
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # Add title slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title only
    title = slide.shapes.title
    title.text = "ISAAI Run Report: {{ReportDate}}"
    title.text_frame.paragraphs[0].font.size = Pt(36)
    title.text_frame.paragraphs[0].font.color.rgb = RGBColor(0x00, 0x33, 0x5B)

    # Add text box for placeholders
    tx_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(8.0), Inches(4.5))
    tf = tx_box.text_frame
    tf.word_wrap = True

    p1 = tf.paragraphs[0]
    p1.text = "Report A Validation Status: {{ReportA_Status}}"
    p1.font.size = Pt(20)
    p1.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    p2 = tf.add_paragraph()
    p2.text = "Report B Validation Status: {{ReportB_Status}}"
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    p3 = tf.add_paragraph()
    p3.text = "\nReport A Details: {{ReportA_Details}}"
    p3.font.size = Pt(16)
    p3.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    p4 = tf.add_paragraph()
    p4.text = "Report B Details: {{ReportB_Details}}"
    p4.font.size = Pt(16)
    p4.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    prs.save(template_path)
    print(f"Template saved to {template_path.relative_to(ROOT)}")
    return template_path

def init_log_file():
    """Initializes the mock SharePoint List CSV locally (always fresh)."""
    with open(SHAREPOINT_LOG_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_COLUMNS)

def parse_xml_rules(xml_path):
    """Parses XML and evaluates the two-step validation rules."""
    import xml.etree.ElementTree as ET
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Check rows
        row = root.find(".//Row")
        if row is None:
            return "Error", "No Row data element found in XML"
            
        marker_elem = row.find("ViolationMarker")
        marker = marker_elem.text if marker_elem is not None else "N"
        
        if marker != "V":
            return "Pass", "No violation marker detected (Step 1 Clean)"
            
        # If marker is V, check secondary thresholds
        thresholds = {}
        breaches = []
        for i in range(1, 5):
            t_elem = row.find(f"Threshold{i}")
            if t_elem is not None:
                val = int(t_elem.text)
                thresholds[f"Threshold{i}"] = val
                if val < THRESHOLD_LIMIT:
                    breaches.append(f"Threshold{i} ({val} < {THRESHOLD_LIMIT})")
                    
        if breaches:
            return "Violation", f"Breached limits: {', '.join(breaches)}"
        else:
            return "Pass", f"Violation marker present but thresholds healthy: {thresholds}"
            
    except Exception as e:
        return "Error", f"Failed to parse XML: {e}"

def generate_evidence_csv(run_dir, date_str, report_type, status, details):
    """Generates Excel-compatible CSV evidence sheets."""
    evidence_path = run_dir / f"evidence_{report_type}.csv"
    with open(evidence_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Report Date", "Report Type", "Validation Status", "Breach Details"])
        writer.writerow([date_str, report_type, status, details])
    return evidence_path

def generate_presentation_deck(template_path, date_str, status_a, status_b, details_a, details_b):
    """Copies PowerPoint template and populates placeholders with run validation metrics."""
    output_path = PRESENTATIONS_DIR / f"{date_str}_Run_Summary.pptx"
    prs = Presentation(template_path)
    
    replacements = {
        "{{ReportDate}}": date_str,
        "{{ReportA_Status}}": status_a,
        "{{ReportB_Status}}": status_b,
        "{{ReportA_Details}}": details_a,
        "{{ReportB_Details}}": details_b
    }

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        for key, val in replacements.items():
                            if key in run.text:
                                run.text = run.text.replace(key, str(val))

    prs.save(output_path)
    return output_path

def process_run(run_path, template_path):
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
        
    # Execute Rule Val Engine
    status_a, details_a = parse_xml_rules(xml_a)
    status_b, details_b = parse_xml_rules(xml_b)
    
    # Generate Excel CSV Evidence
    evidence_a = generate_evidence_csv(run_path, date_str, "ReportTypeA", status_a, details_a)
    evidence_b = generate_evidence_csv(run_path, date_str, "ReportTypeB", status_b, details_b)
    
    # Check Exception Flag (If either is Violation)
    has_violation = (status_a == "Violation" or status_b == "Violation")
    overall_status = "Exception" if has_violation else "Completed"
    exception_flag = "Yes" if has_violation else "No"
    
    # Generate presentation
    presentation_path = generate_presentation_deck(
        template_path, date_str, status_a, status_b, details_a, details_b
    )
    
    # Log Row to SharePoint database
    log_row = {
        "Titel": f"Financial Report Ingestion - {date_str}",
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
        "Presentation_Link": str(presentation_path.relative_to(ROOT))
    }
    
    return log_row

def main():
    template_path = setup_powerpoint_template()
    init_log_file()
    
    if not RUNS_DIR.exists():
        print("Error: No test runs found. Please run scripts/simulate_runs.py first.")
        sys.exit(1)
        
    run_folders = sorted(list(RUNS_DIR.glob("run_*")))
    print(f"Found {len(run_folders)} runs to process locally.")
    
    processed_count = 0
    logged_rows = []
    
    for run_folder in run_folders:
        row = process_run(run_folder, template_path)
        if row:
            logged_rows.append(row)
            processed_count += 1
            
    # Write logged rows to SHAREPOINT_LOG_CSV database
    with open(SHAREPOINT_LOG_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        for row in logged_rows:
            writer.writerow(row)
            
    print(f"\nProcessing complete: {processed_count} runs ingested locally.")
    print(f"Local database list logged to: {SHAREPOINT_LOG_CSV.relative_to(ROOT)}")
    print(f"Presentation decks output to: {PRESENTATIONS_DIR.relative_to(ROOT)}/")

if __name__ == "__main__":
    main()
