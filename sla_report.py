"""CLI report: read tickets.csv, evaluate SLA status, print a summary table.

Usage:
    python sla_report.py [tickets.csv] [--now "2026-10-28 10:30"]
"""

import csv
import sys
from datetime import datetime

from sla import evaluate, summarise


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(argv):
    path = argv[1] if len(argv) > 1 else "tickets.csv"
    now = datetime.now()
    if "--now" in argv:
        now = datetime.strptime(argv[argv.index("--now") + 1], "%Y-%m-%d %H:%M")
    evaluated = [evaluate(row, now) for row in load(path)]
    summary = summarise(evaluated)

    print(f"SLA report as of {now:%Y-%m-%d %H:%M}")
    print(f"Tickets: {summary['total']}  |  Open: {summary['open']}  |  "
          f"Closed: {summary['closed']}  |  Closed within SLA: "
          f"{summary['closed_sla_met_pct']}%")
    print("Status counts:", summary["by_overall"])
    print()
    print(f"{'ID':<4}{'Priority':<10}{'Overall':<10}{'Response':<10}"
          f"{'Resolution':<11}Title")
    for t in sorted(evaluated, key=lambda x: (x["overall"] != "breached",
                                              x["overall"] != "at_risk")):
        print(f"{t['id']:<4}{t['priority']:<10}{t['overall']:<10}"
              f"{t['response_state']:<10}{t['resolution_state']:<11}{t['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
