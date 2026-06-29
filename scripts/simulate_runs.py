#!/usr/bin/env python3
"""ISAAI — Xetra Report Simulation Engine.

Generates realistic daily (Report A) and monthly (Report B) Xetra trading
reports as XML files, packages them into ZIP archives, and stores them in
tests/runs/ for local flow simulation.

Report A (Daily):  Individual trade-level records from Xetra T7
Report B (Monthly): Trader-level aggregated monthly summaries
"""

import argparse
import os
import random
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = ROOT / "tests"
RUNS_DIR = TESTS_DIR / "runs"

# ── Xetra-realistic reference data ──────────────────────────────────────────

DAX_INSTRUMENTS = [
    ("DE0007164600", "SAP SE",            185.0, 210.0),
    ("DE0007236101", "Siemens AG",        160.0, 185.0),
    ("DE0008404005", "Allianz SE",        250.0, 280.0),
    ("DE000BAY0017", "Bayer AG",           28.0,  35.0),
    ("DE0005140008", "Deutsche Bank AG",   15.0,  18.0),
    ("DE0007100000", "Mercedes-Benz Group", 62.0,  75.0),
    ("DE000BASF111", "BASF SE",            43.0,  52.0),
    ("DE0006231004", "Infineon Technologies", 30.0,  38.0),
    ("DE0005557508", "Deutsche Telekom AG", 24.0,  28.0),
    ("DE000DTR0CK8", "Daimler Truck Holding", 38.0,  45.0),
    ("DE0008430026", "Münchener Rück",    440.0, 480.0),
    ("DE000A1EWWW0", "adidas AG",         210.0, 240.0),
]

TRADER_POOL = [
    ("T-1042", "Weber, Lukas",    "Equities"),
    ("T-2087", "Schmidt, Anna",   "Derivatives"),
    ("T-3011", "Fischer, Moritz", "Fixed Income"),
    ("T-4055", "Hoffmann, Lena",  "FX Spot"),
    ("T-5023", "Becker, Jan",     "Equities"),
    ("T-6091", "Krause, Sophie",  "Commodities"),
]

VIOLATION_TYPES_DAILY = [
    "Position limit exceeded — net exposure beyond approved threshold",
    "Late trade booking — execution not reported within T+0 window",
    "Wash trade suspicion — offsetting buy/sell within 60 seconds",
    "Unauthorized instrument — traded outside approved product list",
    "Price manipulation flag — order significantly away from VWAP",
]

VIOLATION_TYPES_MONTHLY = [
    "position limit breach",
    "late trade booking",
    "wash trade flag",
    "unauthorized instrument trade",
    "best execution deviation",
]

COMPLIANCE_RATINGS = ["A", "A", "A", "B", "B", "C"]

MEMBER_ID = "FRAUAS01"


def prettify_xml(elem):
    """Return a pretty-printed XML string."""
    raw = tostring(elem, encoding="unicode")
    parsed = minidom.parseString(raw)
    return parsed.toprettyxml(indent="  ", encoding=None)


def generate_daily_report(report_date, rng):
    """Generate a Report Type A — daily trade-level detail."""
    date_str = report_date.strftime("%Y%m%d")

    root = Element("XetraReport", type="ReportTypeA", date=date_str)

    # Metadata
    meta = SubElement(root, "Metadata")
    SubElement(meta, "ReportID").text = f"XETRA-DA-{date_str}"
    SubElement(meta, "GeneratedAt").text = report_date.strftime("%Y-%m-%dT18:30:00")
    SubElement(meta, "ReportType").text = "Daily"
    SubElement(meta, "CoveragePeriod").text = report_date.strftime("%Y-%m-%d")
    SubElement(meta, "TradingVenue").text = "XETR"
    SubElement(meta, "MemberID").text = MEMBER_ID

    # Generate trades
    trades_elem = SubElement(root, "Trades")
    num_trades = rng.randint(5, 15)
    violations_found = 0
    total_volume = 0.0
    trade_counter = 0

    for i in range(num_trades):
        trade_counter += 1
        isin, name, price_lo, price_hi = rng.choice(DAX_INSTRUMENTS)
        trader_id, _, _ = rng.choice(TRADER_POOL)
        side = rng.choice(["Buy", "Sell"])
        qty = rng.choice([50, 100, 150, 200, 250, 500, 750, 1000])
        price = round(rng.uniform(price_lo, price_hi), 2)
        order_type = rng.choice(["Limit", "Market", "Stop-Limit"])

        hour = rng.randint(9, 17)
        minute = rng.randint(0, 59)
        second = rng.randint(0, 59)
        exec_time = f"{hour:02d}:{minute:02d}:{second:02d}"

        # ~15% chance of violation
        has_violation = rng.random() < 0.15
        day_viol = "Yes" if has_violation else "No"
        viol_detail = rng.choice(VIOLATION_TYPES_DAILY) if has_violation else ""
        status = "Violation" if has_violation else "Pass"
        if has_violation:
            violations_found += 1

        trade_vol = qty * price
        total_volume += trade_vol

        trade = SubElement(trades_elem, "Trade")
        SubElement(trade, "TradeID").text = f"XTR-{date_str}-{trade_counter:05d}"
        SubElement(trade, "ExecutionTime").text = exec_time
        SubElement(trade, "ISIN").text = isin
        SubElement(trade, "Instrument").text = name
        SubElement(trade, "Side").text = side
        SubElement(trade, "Quantity").text = str(qty)
        SubElement(trade, "Price").text = f"{price:.2f}"
        SubElement(trade, "Currency").text = "EUR"
        SubElement(trade, "OrderType").text = order_type
        SubElement(trade, "TraderID").text = trader_id
        SubElement(trade, "DayViol").text = day_viol
        SubElement(trade, "ViolationDetails").text = viol_detail
        SubElement(trade, "Status").text = status

    # Summary
    summary = SubElement(root, "Summary")
    SubElement(summary, "TotalTrades").text = str(num_trades)
    SubElement(summary, "TotalVolume").text = f"{total_volume:.2f}"
    SubElement(summary, "ViolationsFound").text = str(violations_found)
    overall = "Violation" if violations_found > 0 else "Pass"
    SubElement(summary, "OverallStatus").text = overall
    SubElement(summary, "ExceptionFlag").text = "Yes" if violations_found > 0 else "No"

    return prettify_xml(root), overall, violations_found


def generate_monthly_report(report_date, rng):
    """Generate a Report Type B — monthly trader-level aggregation."""
    date_str = report_date.strftime("%Y%m%d")
    month_start = report_date.replace(day=1).strftime("%Y-%m-%d")
    month_end = report_date.strftime("%Y-%m-%d")

    root = Element("XetraReport", type="ReportTypeB", date=date_str)

    # Metadata
    meta = SubElement(root, "Metadata")
    SubElement(meta, "ReportID").text = f"XETRA-MA-{report_date.strftime('%Y%m')}"
    SubElement(meta, "GeneratedAt").text = report_date.strftime("%Y-%m-%dT18:30:00")
    SubElement(meta, "ReportType").text = "Monthly"
    SubElement(meta, "CoveragePeriod").text = f"{month_start} to {month_end}"
    SubElement(meta, "TradingVenue").text = "XETR"
    SubElement(meta, "MemberID").text = MEMBER_ID

    # Trader summaries
    summaries_elem = SubElement(root, "TraderSummaries")
    num_traders = rng.randint(3, 6)
    total_trades = 0
    total_volume = 0.0
    total_violations = 0
    traders_used = rng.sample(TRADER_POOL, min(num_traders, len(TRADER_POOL)))

    for trader_id, trader_name, desk in traders_used:
        trades = rng.randint(80, 450)
        volume = round(rng.uniform(1_500_000, 12_000_000), 2)
        avg_size = round(volume / trades, 2)
        top_isin, top_name, _, _ = rng.choice(DAX_INSTRUMENTS)

        # ~20% chance of monthly violation per trader
        has_violation = rng.random() < 0.20
        viol_count = rng.randint(1, 4) if has_violation else 0
        month_viol = "Yes" if has_violation else "No"

        if has_violation:
            chosen_viols = rng.sample(VIOLATION_TYPES_MONTHLY, min(viol_count, len(VIOLATION_TYPES_MONTHLY)))
            viol_detail = ", ".join(f"{rng.randint(1,3)}x {v}" for v in chosen_viols)
            rating = rng.choice(["C", "D"])
        else:
            viol_detail = ""
            rating = rng.choice(COMPLIANCE_RATINGS)

        status = "Violation" if has_violation else "Pass"
        total_trades += trades
        total_volume += volume
        total_violations += viol_count

        trader = SubElement(summaries_elem, "Trader")
        SubElement(trader, "TraderID").text = trader_id
        SubElement(trader, "TraderName").text = trader_name
        SubElement(trader, "Desk").text = desk
        SubElement(trader, "TotalTrades").text = str(trades)
        SubElement(trader, "TotalVolume").text = f"{volume:.2f}"
        SubElement(trader, "AvgTradeSize").text = f"{avg_size:.2f}"
        SubElement(trader, "TopInstrument").text = f"{top_name} ({top_isin})"
        SubElement(trader, "MonthViol").text = month_viol
        SubElement(trader, "ViolationCount").text = str(viol_count)
        SubElement(trader, "ViolationDetails").text = viol_detail
        SubElement(trader, "ComplianceRating").text = rating
        SubElement(trader, "Status").text = status

    # Summary
    summary = SubElement(root, "Summary")
    SubElement(summary, "TotalTraders").text = str(len(traders_used))
    SubElement(summary, "TotalTrades").text = str(total_trades)
    SubElement(summary, "TotalVolume").text = f"{total_volume:.2f}"
    SubElement(summary, "ViolationsFound").text = str(total_violations)
    overall = "Violation" if total_violations > 0 else "Pass"
    SubElement(summary, "OverallStatus").text = overall
    SubElement(summary, "ExceptionFlag").text = "Yes" if total_violations > 0 else "No"

    return prettify_xml(root), overall, total_violations


def main():
    parser = argparse.ArgumentParser(description="ISAAI Xetra Report Simulation")
    parser.add_argument("--count", type=int, default=30, help="Number of daily runs")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    base_date = datetime(2026, 5, 29)

    print(f"Generating {args.count} Xetra report runs (seed={args.seed})...")
    print(f"Output: tests/runs/\n")

    for i in range(1, args.count + 1):
        report_date = base_date + timedelta(days=i)
        date_str = report_date.strftime("%Y%m%d")

        run_dir = RUNS_DIR / f"run_{i}"
        run_dir.mkdir(parents=True, exist_ok=True)

        # Generate reports
        xml_a, status_a, viols_a = generate_daily_report(report_date, rng)
        xml_b, status_b, viols_b = generate_monthly_report(report_date, rng)

        # Save XML files
        file_a = run_dir / f"{date_str}_ReportTypeA.xml"
        file_b = run_dir / f"{date_str}_ReportTypeB.xml"
        file_a.write_text(xml_a)
        file_b.write_text(xml_b)

        # Create ZIP
        zip_path = run_dir / f"{date_str}_Reports.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(file_a, file_a.name)
            zf.write(file_b, file_b.name)

        # Determine overall status
        has_any_violation = (status_a == "Violation" or status_b == "Violation")
        overall = "Exception" if has_any_violation else "Completed"
        flag = "Yes" if has_any_violation else "No"

        # Write summary
        summary_path = run_dir / "summary.txt"
        summary_path.write_text(
            f"Run ID: {i}\n"
            f"Report Date: {date_str}\n"
            f"Report A (Daily Xetra): {status_a} ({viols_a} violations)\n"
            f"Report B (Monthly Xetra): {status_b} ({viols_b} violations)\n"
            f"OverallStatus: {overall}\n"
            f"ExceptionFlag: {flag}\n"
        )

        marker = "⚠️" if has_any_violation else "✅"
        print(f"  Run {i:03d} [{date_str}]: {marker} Report A: {status_a} | Report B: {status_b}")

    print(f"\n{args.count} Xetra report runs generated in tests/runs/")


if __name__ == "__main__":
    main()
