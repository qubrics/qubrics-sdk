from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from qubrics.core.environment import env_value
from qubrics.mailbox import MailboxAPIApi, create_mailbox_client
from qubrics.management import ConnectionApi, create_management_client
from qubrics.sending import MetaApi, create_sending_client


CLIENTS: list[tuple[Callable[..., Any], Callable[[Any], Any]]] = [
    (create_management_client, lambda client: ConnectionApi(client).management_get_connection_without_preload_content()),
    (create_sending_client, lambda client: MetaApi(client).sending_get_connection_without_preload_content()),
    (create_mailbox_client, lambda client: MailboxAPIApi(client).mailbox_get_connection_without_preload_content()),
]


@pytest.mark.parametrize(("factory", "origin"), [
    (create_mailbox_client, "https://app.qubrics.com/api/v1"),
    (create_management_client, "https://app.qubrics.com/api/v1"),
    (create_sending_client, "https://smtp.qubrics.com/api/v1"),
])
def test_clients_default_to_qubrics_hosts(monkeypatch: pytest.MonkeyPatch, factory: Callable[..., Any], origin: str) -> None:
    for family in ("QUBRICS", "SENDMUX"):
        monkeypatch.delenv(f"{family}_BASE_URL", raising=False)
    key = "smx_root_test" if factory is create_management_client else "smx_mbx_test"
    with factory(api_key=key) as client:
        assert client.configuration.host == origin


@pytest.mark.parametrize("create,key", [(create_mailbox_client, "smx_mbx_"), (create_management_client, "smx_root_"), (create_sending_client, "smx_mbx_")])
def test_clients_use_legacy_env_then_qubrics_env_then_explicit_configuration(monkeypatch: pytest.MonkeyPatch, create: Callable[..., Any], key: str) -> None:
    for prefix in ("QUBRICS", "SENDMUX"):
        for suffix in ("API_KEY", "ACCESS_TOKEN", "BASE_URL"):
            monkeypatch.delenv(f"{prefix}_{suffix}", raising=False)
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


@pytest.mark.parametrize("factory,connect", CLIENTS)
@pytest.mark.parametrize("credential_name", ["API_KEY", "ACCESS_TOKEN"])
def test_empty_qubrics_credentials_retain_legacy_public_requests(
    monkeypatch: pytest.MonkeyPatch,
    factory: Callable[..., Any],
    connect: Callable[[Any], Any],
    credential_name: str,
    endpoint: Any,
) -> None:
    for family in ("QUBRICS", "SENDMUX"):
        for suffix in ("API_KEY", "ACCESS_TOKEN", "BASE_URL"):
            monkeypatch.delenv(f"{family}_{suffix}", raising=False)
    url, requests, _responses = endpoint
    prefix = "smx_root_" if factory is create_management_client else "smx_mbx_"
    legacy = prefix + "legacy" if credential_name == "API_KEY" else "legacy.token"
    current = prefix + "current" if credential_name == "API_KEY" else "current.token"
    option_name = "api_key" if credential_name == "API_KEY" else "access_token"
    monkeypatch.setenv(f"SENDMUX_{credential_name}", legacy)
    monkeypatch.setenv(f"QUBRICS_{credential_name}", "")
    monkeypatch.setenv("SENDMUX_BASE_URL", url)
    monkeypatch.setenv("QUBRICS_BASE_URL", "")
    with factory() as client:
        assert client.configuration.host == url
        response = connect(client)
        response.read()
        response.release_conn()
    monkeypatch.setenv(f"QUBRICS_{credential_name}", current)
    with factory() as client:
        response = connect(client)
        response.read()
        response.release_conn()
    with factory(**{option_name: legacy}, base_url=url) as client:
        response = connect(client)
        response.read()
        response.release_conn()
    assert [request["Authorization"] for request in requests] == [
        "Bearer " + legacy, "Bearer " + current, "Bearer " + legacy,
    ]
    with pytest.raises(ValueError, match="API key|bearer token"):
        factory(**{option_name: ""})
    monkeypatch.setenv(f"QUBRICS_{credential_name}", " ")
    with pytest.raises(ValueError, match="API key|bearer token"):
        factory()
    monkeypatch.setenv(f"QUBRICS_{credential_name}", "")
    monkeypatch.setenv(f"SENDMUX_{credential_name}", "")
    other_name = "ACCESS_TOKEN" if credential_name == "API_KEY" else "API_KEY"
    monkeypatch.setenv(f"SENDMUX_{other_name}", "legacy.token" if other_name == "ACCESS_TOKEN" else prefix + "legacy")
    with pytest.raises(ValueError, match="exactly one"):
        factory()


def test_public_environment_helper_skips_only_empty_qubrics_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("QUBRICS_API_KEY", "")
    monkeypatch.setenv("SENDMUX_API_KEY", "legacy")
    assert env_value("SENDMUX_API_KEY", "fallback") == "legacy"
    for value in ("current", "0", " "):
        monkeypatch.setenv("QUBRICS_API_KEY", value)
        assert env_value("SENDMUX_API_KEY", "fallback") == value
    monkeypatch.setenv("QUBRICS_API_KEY", "")
    monkeypatch.setenv("SENDMUX_API_KEY", "")
    assert env_value("SENDMUX_API_KEY", "fallback") == ""
    monkeypatch.delenv("SENDMUX_API_KEY")
    assert env_value("SENDMUX_API_KEY", "fallback") == "fallback"
    assert env_value("SENDMUX_API_KEY") is None
    assert env_value("SENDMUX_API_KEY", "") == ""
