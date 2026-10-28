"""SLA logic for the ticket dashboard.

Each priority has a first-response target and a resolution target
(in business hours, simplified here to plain hours so the maths stays
transparent in a portfolio demo). A ticket is:

- "breached"  -- a target deadline has passed without the event happening
- "at_risk"   -- the deadline is within 25% of its window and still open
- "on_track"  -- otherwise, or already resolved inside its targets
- "met"       -- resolved inside both targets
"""

from datetime import datetime, timedelta

# priority -> (first-response target hours, resolution target hours)
SLA_TARGETS = {
    "P1": (1, 4),
    "P2": (4, 24),
    "P3": (8, 48),
    "P4": (24, 120),
}

AT_RISK_FRACTION = 0.25  # last quarter of the window counts as at-risk


def parse_ts(value):
    """Parse 'YYYY-MM-DD HH:MM' or return None for an empty cell."""
    if value is None or str(value).strip() == "":
        return None
    return datetime.strptime(str(value).strip(), "%Y-%m-%d %H:%M")


def evaluate(ticket, now):
    """Return a dict with SLA status for one ticket row (dict of strings)."""
    priority = ticket["priority"]
    response_h, resolution_h = SLA_TARGETS[priority]
    created = parse_ts(ticket["created_at"])
    first_response = parse_ts(ticket.get("first_response_at"))
    resolved = parse_ts(ticket.get("resolved_at"))

    response_deadline = created + timedelta(hours=response_h)
    resolution_deadline = created + timedelta(hours=resolution_h)

    def state(event_time, deadline, window_h):
        if event_time is not None:
            return "met" if event_time <= deadline else "breached"
        if now > deadline:
            return "breached"
        if now > deadline - timedelta(hours=window_h * AT_RISK_FRACTION):
            return "at_risk"
        return "on_track"

    response_state = state(first_response, response_deadline, response_h)
    resolution_state = state(resolved, resolution_deadline, resolution_h)

    if "breached" in (response_state, resolution_state):
        overall = "breached"
    elif "at_risk" in (response_state, resolution_state):
        overall = "at_risk"
    elif resolved is not None:
        overall = "met"
    else:
        overall = "on_track"

    return {
        "id": ticket["id"],
        "title": ticket["title"],
        "priority": priority,
        "channel": ticket["channel"],
        "status": ticket["status"],
        "owner": ticket["owner"],
        "response_state": response_state,
        "resolution_state": resolution_state,
        "overall": overall,
        "response_deadline": response_deadline.strftime("%Y-%m-%d %H:%M"),
        "resolution_deadline": resolution_deadline.strftime("%Y-%m-%d %H:%M"),
    }


def summarise(evaluated):
    """Aggregate counts + compliance percentages for a list of evaluated tickets."""
    total = len(evaluated)
    by_overall = {k: 0 for k in ("met", "on_track", "at_risk", "breached")}
    for t in evaluated:
        by_overall[t["overall"]] += 1
    closed = [t for t in evaluated if t["status"] == "resolved"]
    met_closed = sum(1 for t in closed if t["overall"] == "met")
    return {
        "total": total,
        "by_overall": by_overall,
        "closed": len(closed),
        "open": total - len(closed),
        "closed_sla_met_pct": round(100 * met_closed / len(closed), 1) if closed else 0.0,
    }
