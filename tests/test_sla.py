from datetime import datetime

import csv

from sla import evaluate, parse_ts, summarise


def load_sample_rows():
    with open("tickets.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_parse_ts_handles_empty_values():
    assert parse_ts("") is None
    assert parse_ts("   ") is None
    assert parse_ts(None) is None


def test_evaluate_and_summarise_with_sample_data():
    now = datetime(2026, 10, 28, 10, 30)
    evaluated = [evaluate(row, now) for row in load_sample_rows()]
    summary = summarise(evaluated)

    assert summary["total"] == 8
    assert summary["open"] == 5
    assert summary["closed"] == 3
    assert summary["closed_sla_met_pct"] == 66.7
    assert summary["by_overall"] == {
        "met": 2,
        "on_track": 0,
        "at_risk": 0,
        "breached": 6,
    }
