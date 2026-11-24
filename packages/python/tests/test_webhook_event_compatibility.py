from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from qubrics.management import WebhookEventData, WebhookEventPayload


def test_new_subscription_rejects_unknown_labels_and_accepts_mail_events() -> None:
    import qubrics.management as management

    with pytest.raises(ValueError):
        management.WebhookCreateBody(url="https://example.com/hooks", event_types=["historical.event"])
    body = management.WebhookCreateBody(url="https://example.com/hooks", event_types=["message.received"])
    assert body.event_types == ["message.received"]


@pytest.mark.parametrize("event", ["historical.event", "message.received"])
def test_existing_webhook_subscription_event_labels_round_trip(event: str) -> None:
    from qubrics.management import WebhookSubscription

    body: dict[str, Any] = {
        "id": "hook_test", "name": None, "url": "https://example.com/hooks",
        "event_types": [event], "filters": {"mailbox_ids": []}, "enabled": True,
        "failing": False, "created_at": "2026-11-19T00:00:00Z", "updated_at": "2026-11-19T00:00:00Z",
    }
    decoded = WebhookSubscription.from_dict(body)
    assert decoded is not None
    assert decoded.to_dict() == body


@pytest.mark.parametrize("event", ["historical.event", "message.received"])
def test_retained_delivery_payload_round_trips_as_opaque_data(event: str) -> None:
    from qubrics.management import WebhookDeliveryPayload

    document = json.loads((Path(__file__).resolve().parents[1] / "mcp/qubrics/mcp/openapi/openapi-app.json").read_text())
    payload = document["components"]["schemas"]["WebhookEventPayload"]["example"]
    if event == "historical.event":
        payload["type"] = event
        payload["data"] = {"opaque": ["retained", {"unknown": True}]}
    body: dict[str, Any] = {
        "id": "delivery_test", "event_id": payload["id"], "event_type": event,
        "delivery_attempt": 1, "created_at": "2026-11-19T00:00:00Z",
        "expires_at": "2026-11-20T00:00:00Z", "payload": payload,
    }
    decoded = WebhookDeliveryPayload.from_dict(body)
    assert decoded is not None
    assert decoded.payload == payload
    assert decoded.to_dict() == body


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
