# Support SLA Dashboard

A small operations tool that tracks whether support tickets meet their
service-level agreements (SLAs). It reads tickets from a CSV file, evaluates
first-response and resolution targets per priority, and shows the result two
ways: a command-line report and a one-page Flask dashboard.

Built with **Python, Flask, HTML/CSS** — skills on the resume, nothing extra
claimed.

## How SLA status is decided

| Priority | First response target | Resolution target |
|----------|----------------------|-------------------|
| P1 | 1 hour | 4 hours |
| P2 | 4 hours | 24 hours |
| P3 | 8 hours | 48 hours |
| P4 | 24 hours | 120 hours |

A ticket is **breached** if a deadline passed without the event, **at risk**
if it is inside the last 25% of its window and still open, **on track**
otherwise, and **met** if it was resolved inside both targets.

## How to run

```bash
pip install -r requirements.txt

# CLI report (uses the current time, or --now for a fixed demo time)
python sla_report.py tickets.csv
python sla_report.py tickets.csv --now "2026-10-28 10:30"

# Web dashboard
python app.py
# then open http://127.0.0.1:5000
```

## Sample output

```
SLA report as of 2026-10-28 10:30
Tickets: 8  |  Open: 5  |  Closed: 3  |  Closed within SLA: 66.7%
Status counts: {'met': 2, 'on_track': 0, 'at_risk': 0, 'breached': 6}

ID  Priority  Overall   Response  Resolution Title
1   P1        breached  met       breached   Payment gateway timeout on checkout
2   P2        breached  met       breached   Login page slow for some users
4   P4        breached  breached  at_risk    Feature request: dark mode
5   P1        breached  met       breached   Account locked after password reset
7   P2        breached  breached  breached   Dashboard chart shows stale data
8   P3        breached  met       breached   Bulk import fails on large files
3   P2        met       met       met        Invoice PDF shows wrong total
6   P3        met       met       met        Weekly report email not received
```

## Files

- `sla.py` — SLA targets and evaluation logic (no framework dependency)
- `sla_report.py` — command-line report
- `app.py` — Flask dashboard (breached/at-risk tickets sorted first)
- `tickets.csv` — sample dataset of 8 support tickets
- `requirements.txt` — Flask

## Try your own data

Replace `tickets.csv` with your own tickets keeping the same columns
(`id,title,priority,channel,created_at,first_response_at,resolved_at,status,owner`).
Leave `first_response_at` / `resolved_at` empty for events that have not
happened yet. Priorities must be P1–P4.
