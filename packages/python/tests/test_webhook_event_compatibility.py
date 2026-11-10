from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from qubrics.management import WebhookEventData, WebhookEventPayload


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
