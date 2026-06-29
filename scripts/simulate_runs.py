#!/usr/bin/env python3
"""ISAAI Daily Report Run Simulator.

Generates mock XML/ZIP reports for Report Type A (Daily) and B (Monthly) with
varying validation statuses and provides an automated SMTP dispatcher to
simulate daily email runs.

Report Type A uses DayViol marker (daily snapshot).
Report Type B uses MonthViol marker (month-to-date cumulative).

Status values match the SharePoint dropdown schema:
  ReportA_Status / ReportB_Status: Pass, Violation, Error, Pending
  OverallStatus: Completed, Exception, Processing, Failed
  ExceptionFlag: Yes, No
"""

import os
import sys
import zipfile
import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib

# Setup paths relative to the script location
ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = ROOT / "tests"
RUNS_DIR = TESTS_DIR / "runs"

# Ensure directories exist
RUNS_DIR.mkdir(parents=True, exist_ok=True)

# Schema parameters
THRESHOLD_LIMIT = 50

# XML template for Report Type A (Daily — DayViol marker)
XML_TEMPLATE_A = """\
<?xml version="1.0" encoding="UTF-8"?>
<Report type="ReportTypeA" date="{date_str}">
  <Metadata>
    <ReportID>{report_id}</ReportID>
    <GeneratedAt>{timestamp}</GeneratedAt>
    <Description>Daily financial report — previous business day snapshot</Description>
    <CoveragePeriod>Daily</CoveragePeriod>
  </Metadata>
  <Data>
    <Row>
      <RowID>1</RowID>
      <DayViol>{violation_marker}</DayViol>
      <Threshold1>{t1}</Threshold1>
      <Threshold2>{t2}</Threshold2>
      <Threshold3>{t3}</Threshold3>
      <Threshold4>{t4}</Threshold4>
    </Row>
  </Data>
</Report>
"""

# XML template for Report Type B (Monthly — MonthViol marker)
XML_TEMPLATE_B = """\
<?xml version="1.0" encoding="UTF-8"?>
<Report type="ReportTypeB" date="{date_str}">
  <Metadata>
    <ReportID>{report_id}</ReportID>
    <GeneratedAt>{timestamp}</GeneratedAt>
    <Description>Monthly financial report — month-to-date cumulative</Description>
    <CoveragePeriod>Monthly</CoveragePeriod>
  </Metadata>
  <Data>
    <Row>
      <RowID>1</RowID>
      <MonthViol>{violation_marker}</MonthViol>
      <Threshold1>{t1}</Threshold1>
      <Threshold2>{t2}</Threshold2>
      <Threshold3>{t3}</Threshold3>
      <Threshold4>{t4}</Threshold4>
    </Row>
  </Data>
</Report>
"""

def generate_threshold_values(status_type):
    """Generates threshold values based on the requested validation status."""
    if status_type == "Pass":
        # Step 1 fails to trigger (marker is 'N', healthy thresholds)
        violation_marker = "N"
        t1, t2, t3, t4 = (random.randint(60, 100) for _ in range(4))
    elif status_type == "Pass_NoEscalation":
        # Step 1 triggers (marker 'V'), but Step 2 passes (all >= 50)
        violation_marker = "V"
        t1, t2, t3, t4 = (random.randint(50, 100) for _ in range(4))
    elif status_type == "Violation":
        # Step 1 triggers (marker 'V') and Step 2 fails (at least one < 50)
        violation_marker = "V"
        t1, t2, t3, t4 = [random.randint(50, 100) for _ in range(4)]
        # Force at least one below 50
        failed_idx = random.randint(0, 3)
        if failed_idx == 0: t1 = random.randint(10, 49)
        elif failed_idx == 1: t2 = random.randint(10, 49)
        elif failed_idx == 2: t3 = random.randint(10, 49)
        else: t4 = random.randint(10, 49)
    else:
        raise ValueError(f"Unknown status type: {status_type}")

    return violation_marker, {"Threshold1": t1, "Threshold2": t2, "Threshold3": t3, "Threshold4": t4}


def generate_mock_xml(report_type, date_str, status_type):
    """Generates mock XML contents for Report A (DayViol) or Report B (MonthViol)."""
    report_id = f"RPT-{random.randint(100000, 999999)}"
    timestamp = datetime.now().isoformat()

    violation_marker, thresholds = generate_threshold_values(status_type)

    template = XML_TEMPLATE_A if report_type == "ReportTypeA" else XML_TEMPLATE_B

    xml_content = template.format(
        date_str=date_str,
        report_id=report_id,
        timestamp=timestamp,
        violation_marker=violation_marker,
        t1=thresholds["Threshold1"],
        t2=thresholds["Threshold2"],
        t3=thresholds["Threshold3"],
        t4=thresholds["Threshold4"],
    )

    # Map internal status to SharePoint dropdown values
    if status_type == "Pass":
        sp_status = "Pass"
    elif status_type == "Pass_NoEscalation":
        sp_status = "Pass"
    else:
        sp_status = "Violation"

    return xml_content, violation_marker, thresholds, sp_status


def create_run_files(run_id, date):
    """Generates the XML files and packages them into a ZIP archive locally."""
    date_str = date.strftime("%Y%m%d")
    run_dir = RUNS_DIR / f"run_{run_id}"
    run_dir.mkdir(exist_ok=True)

    # Determine status types randomly
    # 60% Pass, 20% Pass_NoEscalation, 20% Violation
    status_choices = ["Pass"] * 60 + ["Pass_NoEscalation"] * 20 + ["Violation"] * 20
    status_a = random.choice(status_choices)
    status_b = random.choice(status_choices)

    # Generate XML contents
    xml_a, marker_a, thresh_a, sp_status_a = generate_mock_xml("ReportTypeA", date_str, status_a)
    xml_b, marker_b, thresh_b, sp_status_b = generate_mock_xml("ReportTypeB", date_str, status_b)

    xml_file_a = run_dir / f"{date_str}_ReportTypeA.xml"
    xml_file_b = run_dir / f"{date_str}_ReportTypeB.xml"

    with open(xml_file_a, "w") as f:
        f.write(xml_a)
    with open(xml_file_b, "w") as f:
        f.write(xml_b)

    # Package into a ZIP file
    zip_filename = f"{date_str}_Reports.zip"
    zip_filepath = run_dir / zip_filename
    with zipfile.ZipFile(zip_filepath, "w") as zipf:
        zipf.write(xml_file_a, arcname=f"{date_str}_ReportTypeA.xml")
        zipf.write(xml_file_b, arcname=f"{date_str}_ReportTypeB.xml")

    # Determine overall status using SharePoint dropdown values
    has_violation = (sp_status_a == "Violation" or sp_status_b == "Violation")
    overall_status = "Exception" if has_violation else "Completed"
    exception_flag = "Yes" if has_violation else "No"

    # Save summary metadata locally
    summary_file = run_dir / "summary.txt"
    with open(summary_file, "w") as f:
        f.write(f"Run ID: {run_id}\n")
        f.write(f"Report Date: {date_str}\n")
        f.write(f"Report A Status: {sp_status_a} (DayViol: {marker_a}, Thresholds: {thresh_a})\n")
        f.write(f"Report B Status: {sp_status_b} (MonthViol: {marker_b}, Thresholds: {thresh_b})\n")
        f.write(f"OverallStatus: {overall_status}\n")
        f.write(f"ExceptionFlag: {exception_flag}\n")

    return zip_filepath, date_str, {
        "A": {"status": sp_status_a, "marker": marker_a, "thresholds": thresh_a},
        "B": {"status": sp_status_b, "marker": marker_b, "thresholds": thresh_b},
        "overall": overall_status,
        "exception_flag": exception_flag,
    }


def send_email(zip_path, date_str, smtp_config):
    """Sends the ZIP file as an email attachment to trigger the Power Automate flow."""
    msg = MIMEMultipart()
    msg['From'] = smtp_config['sender']
    msg['To'] = smtp_config['recipient']
    msg['Subject'] = f"Financial Report Daily Ingest - {date_str}"

    body = (
        f"Hello,\n\nPlease find attached the daily financial reports for {date_str}.\n\n"
        f"Best regards,\nAutomated Report Simulator"
    )
    msg.attach(MIMEText(body, 'plain'))

    # Attach ZIP
    with open(zip_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {zip_path.name}',
        )
        msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_config['server'], smtp_config['port'])
        server.starttls()
        server.login(smtp_config['username'], smtp_config['password'])
        server.send_message(msg)
        server.quit()
        print(f"Successfully sent email for run {date_str}.")
        return True
    except Exception as e:
        print(f"Error sending email for run {date_str}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Simulate daily report validation runs.")
    parser.add_argument("--count", type=int, default=30, help="Number of daily runs to simulate (default: 30).")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible data generation (default: 42).")
    parser.add_argument("--send", action="store_true", help="Send generated ZIP files via email to trigger the flow.")
    parser.add_argument("--dry-run", action="store_true", help="Only generate files locally (default).")

    # SMTP options
    parser.add_argument("--smtp-server", default=os.getenv("SMTP_SERVER"), help="SMTP Server hostname.")
    parser.add_argument("--smtp-port", type=int, default=int(os.getenv("SMTP_PORT", 587)), help="SMTP Server port.")
    parser.add_argument("--smtp-user", default=os.getenv("SMTP_USER"), help="SMTP Login username.")
    parser.add_argument("--smtp-pass", default=os.getenv("SMTP_PASS"), help="SMTP Login password.")
    parser.add_argument("--sender", default=os.getenv("SENDER_EMAIL"), help="Sender email address.")
    parser.add_argument("--recipient", default=os.getenv("RECIPIENT_EMAIL"), help="Recipient email address.")

    args = parser.parse_args()

    # Load SMTP config if --send is requested
    smtp_config = {}
    if args.send:
        smtp_config = {
            "server": args.smtp_server,
            "port": args.smtp_port,
            "username": args.smtp_user,
            "password": args.smtp_pass,
            "sender": args.sender,
            "recipient": args.recipient
        }
        missing = [k for k, v in smtp_config.items() if not v]
        if missing:
            print(f"Error: Missing SMTP configuration options: {', '.join(missing)}")
            print("Please configure them via command line arguments or a .env file.")
            sys.exit(1)

    random.seed(args.seed)
    print(f"Starting simulation of {args.count} daily runs (seed={args.seed})...")
    print(f"Test data will end up locally in: {TESTS_DIR.relative_to(ROOT)}")

    start_date = datetime.now() - timedelta(days=args.count)

    for i in range(args.count):
        run_date = start_date + timedelta(days=i)
        zip_path, date_str, summary = create_run_files(i + 1, run_date)
        print(f"Run {i+1:03d} [{date_str}]: Created ZIP locally at {zip_path.relative_to(ROOT)}")
        print(f"  └─ Report A: {summary['A']['status']} (DayViol={summary['A']['marker']}), "
              f"Report B: {summary['B']['status']} (MonthViol={summary['B']['marker']})")

        if args.send:
            send_email(zip_path, date_str, smtp_config)

    print("\nSimulation setup complete.")
    if not args.send:
        print("To run the email simulation, configure your SMTP server and run with --send.")
        print(f"Local files generated successfully inside {RUNS_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
