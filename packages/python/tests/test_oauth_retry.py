from __future__ import annotations

import json
from collections.abc import Callable
from types import SimpleNamespace
from typing import Any

import pytest
import urllib3.util.retry

import sendmux_core.retry as retry_module
from sendmux_core import RetryOptions
from sendmux_mailbox import MailboxAPIApi, create_mailbox_client
from sendmux_management import ConnectionApi, create_management_client
from sendmux_sending import AttachmentsApi, MetaApi, create_sending_client
from urllib3.exceptions import ProtocolError


@pytest.fixture(autouse=True)
def transport_clock(monkeypatch: Any) -> None:
    monkeypatch.setattr(
        urllib3.util.retry, "time", SimpleNamespace(time=lambda: 1788912000.0, sleep=lambda _seconds: None),
    )


CLIENTS: list[tuple[Callable[..., Any], Callable[[Any], Any]]] = [
    (create_management_client, lambda client: ConnectionApi(client).management_get_connection_without_preload_content()),
    (create_sending_client, lambda client: MetaApi(client).sending_get_connection_without_preload_content()),
    (create_mailbox_client, lambda client: MailboxAPIApi(client).mailbox_get_connection_without_preload_content()),
]


@pytest.mark.parametrize("factory,connect", CLIENTS)
def test_access_token_reaches_each_public_connection_endpoint(factory: Any, connect: Any, endpoint: Any) -> None:
    url, requests, _responses = endpoint
    with factory(access_token="access.token-one", base_url=url) as client:
        response = connect(client)
        response.read()
        response.release_conn()
    assert [request["Authorization"] for request in requests] == ["Bearer access.token-one"]


@pytest.mark.parametrize("factory,connect", CLIENTS)
def test_provider_renews_between_public_requests(factory: Any, connect: Any, endpoint: Any) -> None:
    url, requests, _responses = endpoint
    tokens = iter(["access.token-one", "access.token-two"])
    with factory(access_token=lambda: next(tokens), base_url=url) as client:
        for _ in range(2):
            response = connect(client)
            response.read()
            response.release_conn()
    assert [request["Authorization"] for request in requests] == [
        "Bearer access.token-one", "Bearer access.token-two",
    ]


@pytest.mark.parametrize("family", ["qubrics", "sendmux"])
def test_delegated_upload_does_not_read_or_leak_bearer_provider(family: str, endpoint: Any) -> None:
    url, requests, responses = endpoint
    responses.append((201, {}, {}))

    def bearer_provider() -> str:
        raise AssertionError("Delegated upload must not read the bearer credential")

    with create_sending_client(access_token=bearer_provider, base_url=url) as client:
        response = AttachmentsApi(client).sending_complete_attachment_upload_without_preload_content(
            content_length=4, upload_id="upl_aaaaaaaaaaaaaaaaaaaaaaaa", body=b"test",
            x_qubrics_upload_token="upload-token" if family == "qubrics" else None,
            x_sendmux_upload_token="upload-token" if family == "sendmux" else None,
        )
        response.read()
        response.release_conn()
    assert requests[0][f"X-{family.capitalize()}-Upload-Token"] == "upload-token"
    assert "Authorization" not in requests[0]


@pytest.mark.parametrize("token", ["", "Bearer token", "token\r\nX-Injected: yes", "token with spaces"])
def test_invalid_provider_token_never_reaches_transport(token: str, endpoint: Any) -> None:
    url, requests, _responses = endpoint
    with pytest.raises(ValueError, match="bearer token"):
        with create_management_client(access_token=lambda: token, base_url=url) as client:
            ConnectionApi(client).management_get_connection_without_preload_content()
    assert requests == []


@pytest.mark.parametrize("credentials", [{}, {"api_key": "smx_root_test", "access_token": "access.token"}])
def test_client_requires_exactly_one_credential(credentials: Any, endpoint: Any) -> None:
    url, requests, _responses = endpoint
    with pytest.raises(ValueError, match="exactly one"):
        create_management_client(base_url=url, **credentials)
    assert requests == []


@pytest.mark.parametrize("headers", [
    {"Retry-After": "120"},
    {"Retry-After": "Wed, 09 Sep 2026 00:02:00 GMT"},
    {"X-RateLimit-Reset": "1788912120"},
])
def test_server_retry_delay_is_a_minimum(headers: dict[str, str], endpoint: Any, monkeypatch: Any) -> None:
    url, requests, responses = endpoint
    responses.append((429, headers, {"ok": False, "error": {"retryable": True}}))
    sleeps: list[float] = []
    monkeypatch.setattr(retry_module, "time", SimpleNamespace(time=lambda: 1788912000.0, monotonic=lambda: 0.0))
    with create_management_client(
        api_key="smx_root_test", base_url=url,
        retry_options=RetryOptions(sleep=sleeps.append),
    ) as client:
        response = ConnectionApi(client).management_get_connection_without_preload_content()
        response.read()
        response.release_conn()
    assert response.status == 200
    assert len(requests) == 2
    assert sleeps == [120.0]


@pytest.mark.parametrize("compressed", [False, True])
def test_explicit_nonretryable_error_preserves_response(endpoint: Any, compressed: bool) -> None:
    url, requests, responses = endpoint
    payload = {"ok": False, "error": {"code": "conflict", "retryable": False}}
    headers = {"X-Request-Id": "req-no-retry"}
    if compressed:
        headers["Content-Encoding"] = "gzip"
    responses.append((409, headers, payload))
    sleeps: list[float] = []
    with create_management_client(
        api_key="smx_root_test", base_url=url,
        retry_options=RetryOptions(sleep=sleeps.append),
    ) as client:
        response = ConnectionApi(client).management_get_connection_without_preload_content()
        body = json.loads(response.read())
        response.release_conn()
    assert response.status == 409
    assert response.headers["X-Request-Id"] == "req-no-retry"
    assert body == payload
    assert len(requests) == 1
    assert sleeps == []


@pytest.mark.parametrize("delay,budget,oversleep", [(120, 30, 0), (30, 30, 0), (1, 30, 31)])
def test_retry_budget_returns_last_error_without_early_replay(
    delay: int, budget: int, oversleep: int, endpoint: Any, monkeypatch: Any,
) -> None:
    url, requests, responses = endpoint
    payload = {"ok": False, "error": {"code": "rate_limit_exceeded", "retryable": True}}
    responses.append((429, {"Retry-After": str(delay), "X-Request-Id": "req-budget"}, payload))
    elapsed = [0.0]
    sleeps: list[float] = []

    def sleep(seconds: float) -> None:
        sleeps.append(seconds)
        elapsed[0] += seconds + oversleep

    monkeypatch.setattr(retry_module, "time", SimpleNamespace(time=lambda: 1788912000.0, monotonic=lambda: elapsed[0]))
    with create_management_client(
        api_key="smx_root_test", base_url=url,
        retry_options=RetryOptions(max_elapsed_seconds=budget, sleep=sleep),
    ) as client:
        response = ConnectionApi(client).management_get_connection_without_preload_content()
        body = json.loads(response.read())
        response.release_conn()
    assert response.status == 429
    assert response.headers["Retry-After"] == str(delay)
    assert response.headers["X-Request-Id"] == "req-budget"
    assert body == payload
    assert len(requests) == 1
    assert sleeps == ([float(delay)] if oversleep else [])


def test_transport_cannot_bypass_sdk_retry_limit(endpoint: Any) -> None:
    url, requests, responses = endpoint
    responses.append((429, {"Retry-After": "120"}, {"ok": False, "error": {"retryable": True}}))
    with create_management_client(
        api_key="smx_root_test", base_url=url,
        retry_options=RetryOptions(max_attempts=1),
    ) as client:
        response = ConnectionApi(client).management_get_connection_without_preload_content()
        response.read()
        response.release_conn()
    assert response.status == 429
    assert len(requests) == 1


def test_retry_owner_recovers_from_connection_failure(endpoint: Any) -> None:
    url, requests, responses = endpoint
    responses.append((0, {}, None))
    sleeps: list[float] = []
    with create_management_client(
        api_key="smx_root_test", base_url=url,
        retry_options=RetryOptions(max_attempts=2, sleep=sleeps.append),
    ) as client:
        response = ConnectionApi(client).management_get_connection_without_preload_content()
        response.read()
        response.release_conn()
    assert response.status == 200
    assert len(requests) == 2
    assert len(sleeps) == 1


def test_retry_owner_bounds_connection_failures(endpoint: Any) -> None:
    url, requests, responses = endpoint
    responses.extend([(0, {}, None), (0, {}, None)])
    sleeps: list[float] = []
    with create_management_client(
        api_key="smx_root_test", base_url=url,
        retry_options=RetryOptions(max_attempts=2, sleep=sleeps.append),
    ) as client:
        with pytest.raises(ProtocolError):
            ConnectionApi(client).management_get_connection_without_preload_content()
    assert len(requests) == 2
    assert len(sleeps) == 1
