from datetime import datetime

import app as dashboard_app


class FixedDatetime:
    @staticmethod
    def now():
        return datetime(2026, 10, 28, 10, 30)


def test_dashboard_route_renders_expected_summary(monkeypatch):
    monkeypatch.setattr(dashboard_app, "datetime", FixedDatetime)

    client = dashboard_app.app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    content = response.get_data(as_text=True)
    assert "Support SLA Dashboard" in content
    assert "8 tickets, 5 open," in content
    assert "3 closed, 66.7% of closed tickets met SLA." in content
    assert "met: 2" in content
    assert "breached: 6" in content
