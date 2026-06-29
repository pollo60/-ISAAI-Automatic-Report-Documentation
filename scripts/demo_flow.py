#!/usr/bin/env python3
"""ISAAI — Live Demo Script for Video Recording.

Simulates the complete Power Automate flow in real-time with visual output,
timed delays, and step-by-step phase announcements. Perfect for recording
a video demo of the ISAAI system.

Usage:
    python scripts/demo_flow.py                  # Demo with run_1
    python scripts/demo_flow.py --run 7          # Demo with a specific run
    python scripts/demo_flow.py --run 7 --fast   # Faster delays for rehearsal
"""

import argparse
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    from openpyxl import Workbook
except ImportError:
    print("pip install openpyxl")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
RUNS_DIR = ROOT / "tests" / "runs"

# ANSI colors
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

PHASE_BAR = f"{BLUE}{'━' * 70}{RESET}"


def wait(seconds):
    """Visible countdown pause."""
    time.sleep(seconds)


def print_phase(phase_id, title, icon="▶"):
    """Print a phase header with delay."""
    print(f"\n{PHASE_BAR}")
    print(f"  {BOLD}{CYAN}{icon}  PHASE {phase_id}: {title}{RESET}")
    print(PHASE_BAR)
    wait(delay)


def print_action(text, icon="  →"):
    """Print a flow action step."""
    print(f"{icon} {text}")
    wait(delay * 0.5)


def print_result(text, success=True):
    """Print a result with color."""
    color = GREEN if success else RED
    icon = "  ✅" if success else "  ⚠️"
    print(f"{color}{icon} {text}{RESET}")
    wait(delay * 0.3)


def open_file(path):
    """Open a file with the default application (macOS)."""
    try:
        subprocess.Popen(["open", str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass  # Silently fail on non-macOS


def run_demo(run_number, open_files=True):
    """Run the full flow demo for a specific test run."""
    run_dir = RUNS_DIR / f"run_{run_number}"
    if not run_dir.exists():
        print(f"{RED}Error: {run_dir} does not exist. Run simulate_runs.py first.{RESET}")
        sys.exit(1)

    xml_a = list(run_dir.glob("*_ReportTypeA.xml"))[0]
    xml_b = list(run_dir.glob("*_ReportTypeB.xml"))[0]
    zip_file = list(run_dir.glob("*_Reports.zip"))[0]
    date_str = xml_a.stem.split("_")[0]

    print(f"\n{BOLD}{BLUE}{'═' * 70}{RESET}")
    print(f"  {BOLD}{CYAN}🚀  ISAAI — Daily Report Processing Flow{RESET}")
    print(f"  {DIM}Simulating Power Automate execution for {date_str}{RESET}")
    print(f"  {DIM}Run #{run_number}  |  {xml_a.parent}{RESET}")
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")
    wait(delay)

    # ── PHASE A ──────────────────────────────────────────────────────────────
    print_phase("A", "EMAIL TRIGGER & VARIABLE INITIALIZATION", "📨")

    print_action(f"New email detected: Subject = {BOLD}\"Xetra Financial Report — {date_str}\"{RESET}")
    print_action(f"Attachment found: {BOLD}{zip_file.name}{RESET} ({zip_file.stat().st_size:,} bytes)")
    print_action(f"Initializing variables...")
    print(f"     ReportDate     = {YELLOW}{date_str}{RESET}")
    print(f"     ReportA_Result = {GREEN}Pending{RESET}")
    print(f"     ReportB_Result = {GREEN}Pending{RESET}")
    print_result("Variables initialized")

    # ── PHASE B ──────────────────────────────────────────────────────────────
    print_phase("B", "SHAREPOINT LIST ENTRY", "📋")

    print_action("Creating new item in SharePoint list \"Report Processing Log\"...")
    print(f"     Title          = Xetra Report Ingestion — {date_str}")
    print(f"     OverallStatus  = {YELLOW}Processing{RESET}")
    print(f"     ExceptionFlag  = No")
    print_result("SharePoint list item created (LogItemID = 1)")

    # ── PHASE C ──────────────────────────────────────────────────────────────
    print_phase("C", "ZIP EXTRACTION & XML READING", "📦")

    print_action(f"Uploading {zip_file.name} to OneDrive /Evidence Archive/Temp/...")
    wait(delay * 0.5)
    print_action("Extracting archive to /Evidence Archive/Temp/Extracted/...")
    wait(delay * 0.5)

    print_action(f"Reading {BOLD}{xml_a.name}{RESET}...")
    tree_a = ET.parse(xml_a)
    root_a = tree_a.getroot()
    trades_a = root_a.findall(".//Trade")
    print(f"     Parsed {len(trades_a)} trades from Report Type A (Daily)")

    print_action(f"Reading {BOLD}{xml_b.name}{RESET}...")
    tree_b = ET.parse(xml_b)
    root_b = tree_b.getroot()
    traders_b = root_b.findall(".//Trader")
    print(f"     Parsed {len(traders_b)} trader summaries from Report Type B (Monthly)")

    print_result("XML content loaded successfully")

    # Show a preview of the data
    print(f"\n  {DIM}┌─── Report A Preview (first 3 trades) ───┐{RESET}")
    for trade in trades_a[:3]:
        isin = trade.findtext("ISIN", "")
        instrument = trade.findtext("Instrument", "")
        side = trade.findtext("Side", "")
        qty = trade.findtext("Quantity", "")
        price = trade.findtext("Price", "")
        viol = trade.findtext("DayViol", "No")
        color = RED if viol == "Yes" else DIM
        print(f"  {color}  │ {side:4s} {qty:>5s} x {instrument:<22s} @ EUR {price:>8s}  DayViol={viol}{RESET}")
    if len(trades_a) > 3:
        print(f"  {DIM}  │ ... and {len(trades_a) - 3} more trades{RESET}")
    print(f"  {DIM}└──────────────────────────────────────────┘{RESET}")
    wait(delay)

    # ── PHASE D ──────────────────────────────────────────────────────────────
    print_phase("D", "STATUS READING (PARALLEL)", "🔍")

    status_a = root_a.find(".//Summary/OverallStatus").text
    status_b = root_b.find(".//Summary/OverallStatus").text
    viols_a = root_a.find(".//Summary/ViolationsFound").text
    viols_b = root_b.find(".//Summary/ViolationsFound").text

    print_action("Reading Report A status from XML...")
    print(f"     OverallStatus = {RED if status_a == 'Violation' else GREEN}{status_a}{RESET}")
    print(f"     ViolationsFound = {viols_a}")

    print_action("Reading Report B status from XML...")
    print(f"     OverallStatus = {RED if status_b == 'Violation' else GREEN}{status_b}{RESET}")
    print(f"     ViolationsFound = {viols_b}")

    has_violation = (status_a == "Violation" or status_b == "Violation")
    print_result(
        "Violations detected — escalation required" if has_violation else "All reports clean",
        success=not has_violation
    )

    # ── PHASE E ──────────────────────────────────────────────────────────────
    print_phase("E", "EVIDENCE STORAGE (XML → XLSX)", "💾")

    sys.path.insert(0, str(ROOT / "scripts"))
    from local_flow_processor import xml_to_xlsx_daily, xml_to_xlsx_monthly

    xlsx_a = run_dir / "evidence_ReportTypeA.xlsx"
    xlsx_b = run_dir / "evidence_ReportTypeB.xlsx"

    print_action(f"Converting Report A to XLSX...")
    xml_to_xlsx_daily(xml_a, xlsx_a)
    print(f"     Saved: {BOLD}{xlsx_a.name}{RESET} ({xlsx_a.stat().st_size:,} bytes)")

    print_action(f"Converting Report B to XLSX...")
    xml_to_xlsx_monthly(xml_b, xlsx_b)
    print(f"     Saved: {BOLD}{xlsx_b.name}{RESET} ({xlsx_b.stat().st_size:,} bytes)")

    print_action("Archiving original XML files to /Evidence Archive/XML Archive/...")
    print_result("Evidence files stored in SharePoint")

    # Open the XLSX files for the video
    if open_files:
        wait(delay)
        print(f"\n  {CYAN}📂 Opening evidence files...{RESET}")
        open_file(xlsx_a)
        wait(delay * 1.5)
        open_file(xlsx_b)
        wait(delay * 1.5)

    # ── PHASE F ──────────────────────────────────────────────────────────────
    overall = "Exception" if has_violation else "Completed"
    flag = "Yes" if has_violation else "No"

    print_phase("F", "EXCEPTION GATE & COMPLETION", "📧")

    if has_violation:
        print_action(f"{RED}Violation detected → updating SharePoint to Exception{RESET}")
        print(f"     OverallStatus  = {RED}Exception{RESET}")
        print(f"     ExceptionFlag  = {RED}Yes{RESET}")
        print_action(f"{RED}Sending exception alert email to supervisor...{RESET}")
        print(f"\n  {RED}{'─' * 60}{RESET}")
        print(f"  {RED}  To:      supervisor@fra-uas.de{RESET}")
        print(f"  {RED}  Subject: ⚠️ ISAAI Exception — {date_str} Xetra Report{RESET}")
        print(f"  {RED}  Priority: HIGH{RESET}")
        print(f"  {RED}  Body:{RESET}")
        print(f"  {RED}    Report A (Daily):  {status_a} ({viols_a} violations){RESET}")
        print(f"  {RED}    Report B (Monthly): {status_b} ({viols_b} violations){RESET}")
        print(f"  {RED}    Evidence: [XLSX files attached]{RESET}")
        print(f"  {RED}{'─' * 60}{RESET}")
    else:
        print_action(f"{GREEN}No violations → updating SharePoint to Completed{RESET}")
        print(f"     OverallStatus  = {GREEN}Completed{RESET}")
        print(f"     ExceptionFlag  = {GREEN}No{RESET}")
        print_action(f"{GREEN}Sending confirmation email...{RESET}")
        print(f"\n  {GREEN}{'─' * 60}{RESET}")
        print(f"  {GREEN}  To:      team@fra-uas.de{RESET}")
        print(f"  {GREEN}  Subject: ✅ ISAAI Completed — {date_str} Xetra Report{RESET}")
        print(f"  {GREEN}  Priority: Normal{RESET}")
        print(f"  {GREEN}  Body:{RESET}")
        print(f"  {GREEN}    Report A (Daily):  {status_a}{RESET}")
        print(f"  {GREEN}    Report B (Monthly): {status_b}{RESET}")
        print(f"  {GREEN}    Evidence files archived.{RESET}")
        print(f"  {GREEN}{'─' * 60}{RESET}")

    print_result("Verification email sent")

    # ── DONE ─────────────────────────────────────────────────────────────────
    wait(delay)
    print(f"\n{BOLD}{BLUE}{'═' * 70}{RESET}")
    status_emoji = "⚠️" if has_violation else "✅"
    print(f"  {BOLD}{status_emoji}  FLOW EXECUTION COMPLETE{RESET}")
    print(f"  {DIM}Report Date: {date_str}  |  Result: {overall}  |  Flag: {flag}{RESET}")
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ISAAI Live Demo for Video Recording")
    parser.add_argument("--run", type=int, default=1, help="Run number to demo (default: 1)")
    parser.add_argument("--fast", action="store_true", help="Fast mode (shorter delays)")
    parser.add_argument("--no-open", action="store_true", help="Don't open XLSX files automatically")
    args = parser.parse_args()

    delay = 0.8 if args.fast else 2.0
    run_demo(args.run, open_files=not args.no_open)
