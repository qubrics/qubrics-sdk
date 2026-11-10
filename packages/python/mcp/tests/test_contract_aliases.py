from __future__ import annotations

import asyncio
from typing import Any

import httpx
import pytest
from fastmcp import Client
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

from qubrics.mcp.config import ServerConfig, Surface, config_from_env
from qubrics.mcp.server import create_server


@pytest.mark.parametrize("prefix", ["QUBRICS", "SENDMUX"])
def test_configuration_accepts_both_environment_families(monkeypatch: pytest.MonkeyPatch, prefix: str) -> None:
    other_prefix = "SENDMUX" if prefix == "QUBRICS" else "QUBRICS"
    for suffix in ("API_KEY", "MCP_SURFACES", "APP_BASE_URL", "MCP_TIMEOUT_SECONDS"):
        monkeypatch.delenv(f"{other_prefix}_{suffix}", raising=False)
    monkeypatch.setenv(f"{prefix}_API_KEY", "smx_mbx_fixture")
    monkeypatch.setenv(f"{prefix}_MCP_SURFACES", "mailbox,sending")
    monkeypatch.setenv(f"{prefix}_APP_BASE_URL", "https://app.fixture.test/api/v1")
    monkeypatch.setenv(f"{prefix}_MCP_TIMEOUT_SECONDS", "12")
    config = config_from_env()
    assert config.api_key == "smx_mbx_fixture"
    assert config.surfaces == ("mailbox", "sending")
    assert config.app_base_url == "https://app.fixture.test/api/v1"
    assert config.timeout_seconds == 12


def test_qubrics_environment_precedes_legacy_and_explicit_key_precedes_both(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SENDMUX_API_KEY", "smx_mbx_legacy")
    monkeypatch.setenv("QUBRICS_API_KEY", "smx_mbx_current")
    monkeypatch.setenv("SENDMUX_MAILBOX_API_KEY", "smx_mbx_legacy_surface")
    monkeypatch.setenv("QUBRICS_MAILBOX_API_KEY", "smx_mbx_current_surface")
    monkeypatch.setenv("SENDMUX_MCP_PORT", "8765")
    monkeypatch.setenv("QUBRICS_MCP_PORT", "8766")
    config = config_from_env()
    assert config.api_key == "smx_mbx_current"
    assert config.api_keys["mailbox"] == "smx_mbx_current_surface"
    assert config.port == 8766
    assert config_from_env(api_key="smx_mbx_explicit").api_key == "smx_mbx_explicit"


def test_empty_qubrics_configuration_preserves_legacy_values_and_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    legacy = {
        "API_KEY": "smx_mbx_legacy",
        "MAILBOX_API_KEY": "smx_mbx_legacy_surface",
        "MCP_PORT": "9000",
        "MCP_SURFACES": "mailbox,sending",
        "APP_BASE_URL": "https://legacy.fixture.test/api/v1",
        "MCP_TIMEOUT_SECONDS": "12",
        "MCP_STATELESS_HTTP": "",
    }
    for suffix, value in legacy.items():
        monkeypatch.setenv(f"SENDMUX_{suffix}", value)
        monkeypatch.setenv(f"QUBRICS_{suffix}", "")
    monkeypatch.delenv("SENDMUX_MCP_HOST", raising=False)
    monkeypatch.setenv("QUBRICS_MCP_HOST", "")
    config = config_from_env()
    assert config.api_key == "smx_mbx_legacy"
    assert config.api_keys["mailbox"] == "smx_mbx_legacy_surface"
    assert config.port == 9000
    assert config.surfaces == ("mailbox", "sending")
    assert config.app_base_url == "https://legacy.fixture.test/api/v1"
    assert config.timeout_seconds == 12
    assert config.host == "127.0.0.1"
    assert config.stateless_http is False
    assert config_from_env(api_key="").api_key == "smx_mbx_legacy"
    monkeypatch.setenv("QUBRICS_MCP_PORT", " ")
    with pytest.raises(ValueError, match="invalid literal"):
        config_from_env()


@pytest.mark.parametrize("surface,path", [("mailbox", "/api/v1/mailbox/connection"), ("management", "/api/v1/me"), ("sending", "/api/v1/me")])
def test_mcp_lists_and_calls_both_names_with_identical_contracts(surface: Surface, path: str) -> None:
    async def scenario() -> None:
        requests: list[str] = []
        response = {"ok": True, "data": {"label": "Fixture", "permissions": [], "mailboxes": [], "team": {"id": "team_fixture", "name": "Fixture"}, "credential": {"id": "key_fixture", "type": "api_key", "name": None}}, "meta": {"request_id": "req_fixture"}}

        def upstream(request: httpx.Request) -> httpx.Response:
            requests.append(request.url.path)
            return httpx.Response(200, json=response)

        api_key = "smx_root_fixture" if surface == "management" else "smx_mbx_fixture"
        server = create_server(ServerConfig(surfaces=(surface,), api_key=api_key), transport=httpx.MockTransport(upstream))
        async with Client(server) as client:
            tools = {tool.name: tool for tool in await client.list_tools()}
            original = f"{surface}_get_connection"
            alias = f"qubrics_{original}"
            assert alias in tools
            assert tools[alias].input_schema == tools[original].input_schema
            assert tools[alias].output_schema == tools[original].output_schema
            assert tools[alias].annotations == tools[original].annotations
            assert (await client.call_tool(original, {})).data == (await client.call_tool(alias, {})).data
        assert requests == [path, path]

    asyncio.run(scenario())


@pytest.mark.parametrize("method", ["tools/list", "tools/call"])
@pytest.mark.parametrize("permissions", [("email.send",), ()])
def test_authenticated_http_aliases_share_discovery_calls_and_permissions(method: str, permissions: tuple[str, ...]) -> None:
    async def scenario() -> None:
        requests: list[str] = []
        payload = {"ok": True, "data": {"label": "Fixture", "permissions": [], "mailboxes": [], "team": {"id": "team_fixture", "name": "Fixture"}, "credential": {"id": "key_fixture", "type": "api_key", "name": None}}, "meta": {"request_id": "req_fixture"}}

        def upstream(request: httpx.Request) -> httpx.Response:
            requests.append(request.url.path)
            return httpx.Response(200, json=payload)

        verifier = StaticTokenVerifier(tokens={"alias_access_token": {"client_id": "alias-test", "permissions": list(permissions), "surface": ["sending"]}})
        server = create_server(ServerConfig(surfaces=("sending",), api_key="smx_mbx_fixture"), transport=httpx.MockTransport(upstream), auth_provider=verifier)
        app = server.http_app(path="/mcp", stateless_http=True, json_response=True)
        names = ("sending_get_connection", "qubrics_sending_get_connection")
        responses: list[dict[str, Any]] = []
        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="https://mcp.sendmux.ai") as client:
                for name in names if method == "tools/call" else names[:1]:
                    params: dict[str, Any] = {"name": name, "arguments": {}} if method == "tools/call" else {}
                    params["_meta"] = {"io.modelcontextprotocol/protocolVersion": "2026-07-28", "io.modelcontextprotocol/clientCapabilities": {}}
                    response = await client.post("/mcp", headers={"Authorization": "Bearer alias_access_token", "Content-Type": "application/json", "MCP-Protocol-Version": "2026-07-28", "Mcp-Method": method, "Mcp-Name": name}, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
                    assert response.status_code == 200
                    responses.append(response.json())

        if method == "tools/list":
            listed = {tool["name"] for tool in responses[0]["result"]["tools"]}
            assert all((name in listed) == bool(permissions) for name in names), listed
            assert requests == []
        elif permissions:
            for result in responses:
                assert "error" not in result, result
                assert result["result"].get("isError", False) is False, result
            assert responses[0]["result"] == responses[1]["result"]
            assert requests == ["/api/v1/me", "/api/v1/me"]
        else:
            for result in responses:
                assert result.get("error") is not None or result["result"].get("isError", False) is True
            assert requests == []

    asyncio.run(scenario())
