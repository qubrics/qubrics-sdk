from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from sendmux_mailbox import create_mailbox_client
from sendmux_management import create_management_client
from sendmux_sending import create_sending_client


@pytest.mark.parametrize("create,key", [(create_mailbox_client, "smx_mbx_"), (create_management_client, "smx_root_"), (create_sending_client, "smx_mbx_")])
def test_clients_use_legacy_env_then_qubrics_env_then_explicit_configuration(monkeypatch: pytest.MonkeyPatch, create: Callable[..., Any], key: str) -> None:
    monkeypatch.delenv("QUBRICS_API_KEY", raising=False)
    monkeypatch.delenv("QUBRICS_BASE_URL", raising=False)
    monkeypatch.setenv("SENDMUX_API_KEY", key + "legacy")
    monkeypatch.setenv("SENDMUX_BASE_URL", "https://legacy.fixture.test/api/v1")
    with create() as client:
        assert client.configuration.access_token == key + "legacy"
        assert client.configuration.host == "https://legacy.fixture.test/api/v1"
    monkeypatch.setenv("QUBRICS_API_KEY", key + "current")
    monkeypatch.setenv("QUBRICS_BASE_URL", "https://current.fixture.test/api/v1")
    with create() as client:
        assert client.configuration.access_token == key + "current"
        assert client.configuration.host == "https://current.fixture.test/api/v1"
    with create(api_key=key + "explicit", base_url="https://explicit.fixture.test/api/v1") as client:
        assert client.configuration.access_token == key + "explicit"
        assert client.configuration.host == "https://explicit.fixture.test/api/v1"
