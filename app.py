"""Flask SLA dashboard: a one-page view of ticket SLA health.

Run:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000
"""

import csv
from datetime import datetime

from flask import Flask, render_template_string

from sla import evaluate, summarise

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html><head><meta charset="utf-8"><title>SLA Dashboard</title>
<style>
body { font-family: system-ui, sans-serif; max-width: 900px; margin: 2rem auto; }
.badge { padding: 2px 8px; border-radius: 12px; color: #fff; font-size: 0.85em; }
.met { background: #2e7d32; } .on_track { background: #1565c0; }
.at_risk { background: #ef6c00; } .breached { background: #c62828; }
table { border-collapse: collapse; width: 100%; }
th, td { border-bottom: 1px solid #ddd; padding: 8px; text-align: left; }
</style></head>
<body>
<h1>Support SLA Dashboard</h1>
<p>As of {{ now }} &mdash; {{ s.total }} tickets, {{ s.open }} open,
{{ s.closed }} closed, {{ s.closed_sla_met_pct }}% of closed tickets met SLA.</p>
<p>
  <span class="badge met">met: {{ s.by_overall.met }}</span>
  <span class="badge on_track">on track: {{ s.by_overall.on_track }}</span>
  <span class="badge at_risk">at risk: {{ s.by_overall.at_risk }}</span>
  <span class="badge breached">breached: {{ s.by_overall.breached }}</span>
</p>
<table>
<tr><th>ID</th><th>Title</th><th>Priority</th><th>Owner</th>
<th>Response</th><th>Resolution</th><th>Overall</th></tr>
{% for t in tickets %}
<tr><td>{{ t.id }}</td><td>{{ t.title }}</td><td>{{ t.priority }}</td>
<td>{{ t.owner }}</td>
<td><span class="badge {{ t.response_state }}">{{ t.response_state }}</span></td>
<td><span class="badge {{ t.resolution_state }}">{{ t.resolution_state }}</span></td>
<td><span class="badge {{ t.overall }}">{{ t.overall }}</span></td></tr>
{% endfor %}
</table>
</body></html>
"""


def load_tickets():
    with open("tickets.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


@app.route("/")
def dashboard():
    now = datetime.now()
    evaluated = [evaluate(row, now) for row in load_tickets()]
    order = {"breached": 0, "at_risk": 1, "on_track": 2, "met": 3}
    evaluated.sort(key=lambda t: order[t["overall"]])
    return render_template_string(
        TEMPLATE,
        tickets=evaluated,
        s=summarise(evaluated),
        now=now.strftime("%Y-%m-%d %H:%M"),
    )


if __name__ == "__main__":
    app.run(debug=True)
