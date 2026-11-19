from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from qubrics.management import WebhookEventData, WebhookEventPayload


def test_management_withholds_calendar_but_preserves_mail_webhooks() -> None:
    import qubrics.management as management
    import qubrics.management.models as models

    assert not [name for name in dir(management) if "calendar" in name.lower()]
    assert not [name for name in dir(models) if "calendar" in name.lower()]
    with pytest.raises(ValueError):
        management.WebhookCreateBody(url="https://example.com/hooks", event_types=["calendar.changed"])
    body = management.WebhookCreateBody(url="https://example.com/hooks", event_types=["message.received"])
    assert body.event_types == ["message.received"]


@pytest.mark.parametrize("event", ["calendar.changed", "message.received"])
def test_existing_webhook_subscription_event_labels_round_trip(event: str) -> None:
    from qubrics.management import WebhookSubscription

    body = {
        "id": "hook_test", "name": None, "url": "https://example.com/hooks",
        "event_types": [event], "filters": {"mailbox_ids": []}, "enabled": True,
        "failing": False, "created_at": "2026-11-19T00:00:00Z", "updated_at": "2026-11-19T00:00:00Z",
    }
    assert WebhookSubscription.from_dict(body).to_dict() == body


@pytest.mark.parametrize("correlation", [{}, {"qubrics_message_id": None}, {"qubrics_message_id": "message_compatibility"}], ids=["omitted", "null", "string"])
@pytest.mark.parametrize("nested", [False, True], ids=["data", "payload"])
def test_webhook_message_alias_preserves_presence_and_value(correlation: dict[str, Any], nested: bool) -> None:
    document = json.loads((Path(__file__).resolve().parents[1] / "mcp/qubrics/mcp/openapi/openapi-app.json").read_text())
    payload = document["components"]["schemas"]["WebhookEventPayload"]["example"]
    payload["data"].pop("qubrics_message_id")
    payload["data"]["sendmux_message_id"] = "message_compatibility"
    payload["data"].update(correlation)
    model = WebhookEventPayload if nested else WebhookEventData
    body = payload if nested else payload["data"]
    decoded = model.from_dict(body)
    assert decoded is not None
    assert decoded.to_dict() == body
    assert json.loads(decoded.to_json()) == body
