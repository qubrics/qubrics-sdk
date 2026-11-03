from __future__ import annotations

import asyncio
from dataclasses import replace
from importlib.metadata import version
from urllib.parse import urlparse

import httpx
import httpx2
import pytest
from fastmcp.server.auth import RemoteAuthProvider
from fastmcp.server.auth.providers.jwt import JWTVerifier, RSAKeyPair
from joserfc import jwk

from sendmux_mcp.curation import MAILBOX_TOOLS
from sendmux_mcp.hosted import (
    HOSTED_MCP_DISCOVERY_SCOPES,
    HOSTED_SURFACES,
    HostedServerRuntimeConfig,
    create_hosted_http_app,
    create_hosted_server,
    hosted_mcp_proxy_config,
    hosted_http_middleware,
    hosted_runtime_config_from_env,
    hosted_surface_config,
    origin_from_url,
)
from sendmux_mcp.hosted_auth import HostedAuthConfig, create_remote_auth_provider
from sendmux_mcp.hosted_proxy import HostedProxyConfig
from sendmux_mcp.server import create_server


def runtime_config() -> HostedServerRuntimeConfig:
    return HostedServerRuntimeConfig(
        issuer="https://app.sendmux.ai",
        authorization_servers=("https://app.sendmux.ai",),
        jwks_uri="https://app.sendmux.ai/.well-known/jwks.json",
        resource_base_url="https://mcp.sendmux.ai",
        proxy_url="http://sendmux-app.sendmux.svc.cluster.local/api/internal/mcp/proxy",
        internal_bearer_token="internal-service-token",
        mcp_path="/mcp",
        host="127.0.0.1",
        port=8765,
        stateless_http=True,
        scopes_supported=HOSTED_MCP_DISCOVERY_SCOPES,
        allowed_origins=("https://app.sendmux.ai",),
    )


def test_hosted_server_mounts_all_surfaces_without_process_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    async def run() -> None:
        monkeypatch.delenv("SENDMUX_API_KEY", raising=False)

        server = create_hosted_server(runtime_config())
        unauthenticated_tools = await server.list_tools()

        assert server.auth is not None
        assert unauthenticated_tools == []

    asyncio.run(run())


def test_hosted_mcp_proxy_carries_exact_oauth_resource_context() -> None:
    runtime = runtime_config()

    config = hosted_mcp_proxy_config(runtime, hosted_surface_config("mailbox", runtime))

    assert config.resource == "https://mcp.sendmux.ai/mcp"
    assert config.protocol == "mcp"


def test_hosted_server_rejects_localhost_browser_preflight_by_default() -> None:
    async def run() -> None:
        server = create_hosted_server(runtime_config())
        app = server.http_app(path="/mcp", middleware=hosted_http_middleware(), stateless_http=True)
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(transport=transport, base_url="https://mcp.sendmux.ai") as client:
            response = await client.options(
                "/mcp",
                headers={
                    "Origin": "http://localhost:6274",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "authorization,content-type,mcp-protocol-version",
                },
            )

        assert response.status_code == 403
        assert response.json()["error"]["code"] == "origin_forbidden"

    asyncio.run(run())


def test_hosted_server_allows_browser_preflight_from_app_origin() -> None:
    async def run() -> None:
        server = create_hosted_server(runtime_config())
        app = server.http_app(path="/mcp", middleware=hosted_http_middleware(), stateless_http=True)
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(transport=transport, base_url="https://mcp.sendmux.ai") as client:
            response = await client.options(
                "/mcp",
                headers={
                    "Origin": "https://app.sendmux.ai",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "authorization,content-type,mcp-protocol-version",
                },
            )

        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == "https://app.sendmux.ai"
        assert "authorization" in response.headers["access-control-allow-headers"].lower()
        assert "mcp-protocol-version" in response.headers["access-control-allow-headers"].lower()
        assert "post" in response.headers["access-control-allow-methods"].lower()
        assert "access-control-allow-credentials" not in response.headers

    asyncio.run(run())


def test_hosted_server_allows_bounded_modern_routing_headers() -> None:
    async def run() -> None:
        server = create_hosted_server(runtime_config())
        app = server.http_app(path="/mcp", middleware=hosted_http_middleware(), stateless_http=True)
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(transport=transport, base_url="https://mcp.sendmux.ai") as client:
            response = await client.options(
                "/mcp",
                headers={
                    "Origin": "https://app.sendmux.ai",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "authorization,content-type,mcp-protocol-version,mcp-method,mcp-name,mcp-param-cursor",
                },
            )

        assert response.status_code == 200
        allowed = response.headers["access-control-allow-headers"].lower()
        assert "mcp-param-cursor" in allowed

    asyncio.run(run())


def test_hosted_server_rejects_unknown_browser_preflight_header() -> None:
    async def run() -> None:
        server = create_hosted_server(runtime_config())
        app = server.http_app(path="/mcp", middleware=hosted_http_middleware(), stateless_http=True)
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(transport=transport, base_url="https://mcp.sendmux.ai") as client:
            response = await client.options(
                "/mcp",
                headers={
                    "Origin": "https://app.sendmux.ai",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "authorization,x-arbitrary-header",
                },
            )

        assert response.status_code == 400
        assert response.json()["error"]["code"] == "invalid_mcp_header"

    asyncio.run(run())


def test_hosted_server_rejects_oversized_modern_parameter_header() -> None:
    async def run() -> None:
        server = create_hosted_server(runtime_config())
        app = server.http_app(path="/mcp", middleware=hosted_http_middleware(), stateless_http=True)
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(transport=transport, base_url="https://mcp.sendmux.ai") as client:
            response = await client.post("/mcp", headers={"Mcp-Param-Test": "x" * 1025})

        assert response.status_code == 400
        assert response.json()["error"]["code"] == "invalid_mcp_header"

    asyncio.run(run())


def test_hosted_server_rejects_unknown_browser_origin_before_auth() -> None:
    async def run() -> None:
        server = create_hosted_server(runtime_config())
        app = server.http_app(path="/mcp", middleware=hosted_http_middleware(), stateless_http=True)
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(transport=transport, base_url="https://mcp.sendmux.ai") as client:
            response = await client.post(
                "/mcp",
                headers={
                    "Origin": "https://evil.example",
                    "Content-Type": "application/json",
                    "MCP-Protocol-Version": "2025-11-25",
                },
                json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            )

        assert response.status_code == 403
        assert response.json()["error"]["code"] == "origin_forbidden"
        assert "www-authenticate" not in response.headers

    asyncio.run(run())


def test_hosted_server_rejects_unknown_browser_preflight() -> None:
    async def run() -> None:
        server = create_hosted_server(runtime_config())
        app = server.http_app(path="/mcp", middleware=hosted_http_middleware(), stateless_http=True)
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(transport=transport, base_url="https://mcp.sendmux.ai") as client:
            response = await client.options(
                "/mcp",
                headers={
                    "Origin": "https://evil.example",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "authorization,content-type,mcp-protocol-version",
                },
            )

        assert response.status_code == 403
        assert response.json()["error"]["code"] == "origin_forbidden"

    asyncio.run(run())


def test_hosted_server_exposes_mcp_headers_to_browser_requests() -> None:
    async def run() -> None:
        server = create_hosted_server(runtime_config())
        app = server.http_app(path="/mcp", middleware=hosted_http_middleware(), stateless_http=True)
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(transport=transport, base_url="https://mcp.sendmux.ai") as client:
            response = await client.post(
                "/mcp",
                headers={
                    "Origin": "https://app.sendmux.ai",
                    "Content-Type": "application/json",
                    "MCP-Protocol-Version": "2025-11-25",
                },
                json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            )

        assert response.headers["access-control-allow-origin"] == "https://app.sendmux.ai"
        assert "mcp-protocol-version" in response.headers["access-control-expose-headers"].lower()
        assert "mcp-session-id" in response.headers["access-control-expose-headers"].lower()
        assert "access-control-allow-credentials" not in response.headers

    asyncio.run(run())


def test_hosted_server_challenges_unauthenticated_requests_with_hosted_discovery_scope() -> None:
    async def run() -> None:
        server = create_hosted_server(runtime_config())
        app = server.http_app(path="/mcp", middleware=hosted_http_middleware(), stateless_http=True)
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(transport=transport, base_url="https://mcp.sendmux.ai") as client:
            response = await client.post(
                "/mcp",
                headers={
                    "Content-Type": "application/json",
                    "MCP-Protocol-Version": "2025-11-25",
                },
                json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            )

        assert response.status_code == 401
        authenticate = response.headers["www-authenticate"]
        assert 'resource_metadata="https://mcp.sendmux.ai/.well-known/oauth-protected-resource/mcp"' in authenticate
        assert f'scope="{" ".join(HOSTED_MCP_DISCOVERY_SCOPES)}"' in authenticate

    asyncio.run(run())


def test_hosted_server_protected_resource_metadata_preserves_authorization_server_origin() -> None:
    async def run() -> None:
        server = create_hosted_server(runtime_config())
        app = server.http_app(path="/mcp", middleware=hosted_http_middleware(), stateless_http=True)
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(transport=transport, base_url="https://mcp.sendmux.ai") as client:
            response = await client.get("/.well-known/oauth-protected-resource/mcp")

        assert response.status_code == 200
        assert response.json()["authorization_servers"] == ["https://app.sendmux.ai"]
        assert response.json()["scopes_supported"] == list(HOSTED_MCP_DISCOVERY_SCOPES)

    asyncio.run(run())


@pytest.mark.parametrize(
    ("resource_base_url", "mcp_path"),
    [
        ("https://mcp.sendmux.ai", "/mcp"),
        ("https://custom-mcp.example.com:8443", "/custom/"),
    ],
)
def test_hosted_root_metadata_uses_configured_mcp_host(resource_base_url: str, mcp_path: str) -> None:
    async def run() -> None:
        runtime = replace(runtime_config(), resource_base_url=resource_base_url, mcp_path=mcp_path)
        app = create_hosted_http_app(runtime)
        metadata_path = "/.well-known/oauth-protected-resource"

        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=resource_base_url) as client:
                root = await client.get(metadata_path)
                mixed_case = await client.get(metadata_path, headers={"Host": urlparse(resource_base_url).netloc.upper()})
                scoped = await client.get(f"{metadata_path}{mcp_path}")
                a2a = await client.get(f"https://a2a.sendmux.ai{metadata_path}")
                root_head = await client.head(metadata_path, headers={"Host": urlparse(resource_base_url).netloc.upper()})
                scoped_head = await client.head(f"{metadata_path}{mcp_path}")
                a2a_head = await client.head(f"https://a2a.sendmux.ai{metadata_path}")
                a2a_post = await client.post(f"https://a2a.sendmux.ai{metadata_path}")
                a2a_options = await client.options(f"https://a2a.sendmux.ai{metadata_path}")
                other_host = await client.get(f"https://other.example.com{metadata_path}")
                forbidden = await client.get(metadata_path, headers={"Origin": "https://evil.example"})
                unauthenticated = await client.post(
                    mcp_path,
                    json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
                )

        assert root.status_code == scoped.status_code == 200
        assert root.json()["resource"] == f"{resource_base_url}{mcp_path}"
        assert mixed_case.status_code == 200
        assert mixed_case.json() == root.json()
        assert root.json() == scoped.json()
        assert root_head.status_code == scoped_head.status_code == a2a_head.status_code == 200
        assert root_head.content == scoped_head.content == a2a_head.content == b""
        assert root_head.headers["content-length"] == scoped_head.headers["content-length"]
        assert root_head.headers["cache-control"] == scoped_head.headers["cache-control"]
        assert a2a_head.headers["cache-control"] == a2a.headers["cache-control"]
        assert a2a_post.status_code == a2a_options.status_code == 405
        assert set(a2a_post.headers["allow"].split(", ")) == set(a2a_options.headers["allow"].split(", ")) == {"GET", "HEAD"}
        assert a2a.status_code == other_host.status_code == 200
        assert a2a.json()["resource"] == "https://a2a.sendmux.ai/a2a/v1"
        assert a2a.json()["resource_name"] == "Sendmux A2A"
        assert other_host.json() == a2a.json()
        assert forbidden.status_code == 403
        assert forbidden.json()["error"]["code"] == "origin_forbidden"
        assert unauthenticated.status_code == 401
        assert f'resource_metadata="{resource_base_url}{metadata_path}{mcp_path}"' in (
            unauthenticated.headers["www-authenticate"]
        )

    asyncio.run(run())


@pytest.mark.parametrize("mcp_origin", ["https://mcp.sendmux.ai", "https://mcp.qubrics.com"])
def test_hosted_root_metadata_recognises_both_mcp_aliases(mcp_origin: str) -> None:
    async def run() -> None:
        runtime = replace(runtime_config(), resource_base_url=mcp_origin)
        app = create_hosted_http_app(runtime)
        metadata_path = "/.well-known/oauth-protected-resource"
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as client:
            for origin in ("https://mcp.sendmux.ai", "https://mcp.qubrics.com"):
                metadata = await client.get(f"{origin}{metadata_path}")
                assert metadata.status_code == 200
                assert metadata.json()["resource"] == f"{mcp_origin}/mcp"
                assert metadata.json()["resource_name"] == "Sendmux MCP"
            a2a = await client.get(f"https://a2a.sendmux.ai{metadata_path}")
            assert a2a.json()["resource"] == "https://a2a.sendmux.ai/a2a/v1"

    asyncio.run(run())


@pytest.mark.parametrize("mcp_path", ["/mcp", "/custom", "/custom/"])
def test_hosted_prm_jwt_and_proxy_share_exact_mounted_resource(mcp_path: str) -> None:
    async def run() -> None:
        runtime = replace(runtime_config(), mcp_path=mcp_path)
        server = create_hosted_server(runtime)
        app = server.http_app(path=mcp_path, middleware=hosted_http_middleware(), stateless_http=True)
        metadata_path = f"/.well-known/oauth-protected-resource{mcp_path}"

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="https://mcp.sendmux.ai") as client:
            response = await client.get(metadata_path)

        expected = f"https://mcp.sendmux.ai{mcp_path}"
        assert response.status_code == 200
        assert response.json()["resource"] == expected
        assert isinstance(server.auth, RemoteAuthProvider)
        assert isinstance(server.auth.token_verifier, JWTVerifier)
        assert server.auth.token_verifier.audience == (
            ["https://mcp.qubrics.com/mcp", "https://mcp.sendmux.ai/mcp"] if mcp_path == "/mcp" else expected
        )
        assert hosted_mcp_proxy_config(runtime, hosted_surface_config("mailbox", runtime)).resource == expected

    asyncio.run(run())


def test_hosted_server_advertises_sendmux_package_version() -> None:
    server = create_hosted_server(runtime_config())

    assert server._mcp_server.server_info.version == version("sendmux-mcp")


def test_hosted_surface_config_does_not_require_upstream_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SENDMUX_API_KEY", raising=False)

    config = hosted_surface_config("management", runtime_config())

    assert config.api_key is None
    assert config.allow_unauthenticated_http
    assert config.transport == "http"


def test_hosted_surface_children_keep_curated_tool_sets_without_process_api_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def run() -> None:
        monkeypatch.delenv("SENDMUX_API_KEY", raising=False)
        runtime = runtime_config()
        auth_provider = create_remote_auth_provider(
            HostedAuthConfig(
                issuer=runtime.issuer,
                authorization_servers=runtime.authorization_servers,
                jwks_uri=runtime.jwks_uri,
                resource_base_url=runtime.resource_base_url,
                mcp_path=runtime.mcp_path,
            )
        )
        tool_names: set[str] = set()
        tools_by_name = {}

        for surface in HOSTED_SURFACES:
            surface_config = hosted_surface_config(surface, runtime)
            child = create_server(
                surface_config,
                auth_provider=auth_provider,
                hosted_proxy_config=HostedProxyConfig(
                    proxy_url=runtime.proxy_url,
                    upstream_base_url=surface_config.api_base_url,
                    internal_bearer_token=runtime.internal_bearer_token,
                ),
            )
            tools = await child.list_tools(run_middleware=False)
            tool_names.update(tool.name for tool in tools)
            tools_by_name.update({tool.name: tool for tool in tools})

        assert "mailbox_get_me" in tool_names
        assert "management_list_domains" in tool_names
        assert "sending_send_email" in tool_names
        delivery_group = tools_by_name["sending_send_email"].parameters["properties"]["delivery_group"]
        assert delivery_group["description"] == "One delivery group public ID or a non-empty array of up to 50 IDs"
        assert len(delivery_group["anyOf"]) == 2

    asyncio.run(run())


def test_hosted_mailbox_action_tools_expose_mailbox_target(monkeypatch: pytest.MonkeyPatch) -> None:
    async def run() -> None:
        monkeypatch.delenv("SENDMUX_API_KEY", raising=False)

        runtime = runtime_config()
        auth_provider = create_remote_auth_provider(
            HostedAuthConfig(
                issuer=runtime.issuer,
                authorization_servers=runtime.authorization_servers,
                jwks_uri=runtime.jwks_uri,
                resource_base_url=runtime.resource_base_url,
                mcp_path=runtime.mcp_path,
            )
        )
        surface_config = hosted_surface_config("mailbox", runtime)
        child = create_server(
            surface_config,
            auth_provider=auth_provider,
            hosted_proxy_config=HostedProxyConfig(
                proxy_url=runtime.proxy_url,
                upstream_base_url=surface_config.api_base_url,
                internal_bearer_token=runtime.internal_bearer_token,
            ),
        )

        tools = await child.list_tools(run_middleware=False)
        tool_names = {tool.name for tool in tools}
        expected_tool_names = {tool.name for tool in MAILBOX_TOOLS}
        expected_tool_names |= {f"qubrics_{name}" for name in expected_tool_names}
        missing_target: list[str] = []

        assert tool_names == expected_tool_names

        for tool in tools:
            original_name = tool.name.removeprefix("qubrics_")
            properties = (tool.parameters or {}).get("properties", {})
            if original_name in {"mailbox_list_granted_mailboxes", "mailbox_get_connection"}:
                assert "mailbox_id" not in properties
                continue
            if original_name.startswith("mailbox_") and "mailbox_id" not in properties:
                missing_target.append(tool.name)

        assert missing_target == []

    asyncio.run(run())


def test_hosted_runtime_config_uses_public_resource_and_internal_proxy_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SENDMUX_MCP_APP_ORIGIN", "https://app.sendmux.ai")
    monkeypatch.setenv("SENDMUX_MCP_RESOURCE_BASE_URL", "https://mcp.sendmux.ai")
    monkeypatch.setenv("SENDMUX_MCP_PROXY_URL", "http://sendmux-app.sendmux.svc.cluster.local/api/internal/mcp/proxy")
    monkeypatch.setenv("INTERNAL_API_SECRET", "internal-service-token")
    monkeypatch.setenv("SENDMUX_MCP_SCOPES_SUPPORTED", "mailbox.read,email.send")
    monkeypatch.setenv("SENDMUX_MCP_ALLOWED_ORIGINS", "https://app.sendmux.ai,http://localhost:6274")

    config = hosted_runtime_config_from_env()

    assert config.issuer == "https://app.sendmux.ai"
    assert config.jwks_uri == "https://app.sendmux.ai/.well-known/jwks.json"
    assert config.resource_base_url == "https://mcp.sendmux.ai"
    assert config.proxy_url == "http://sendmux-app.sendmux.svc.cluster.local/api/internal/mcp/proxy"
    assert config.internal_bearer_token == "internal-service-token"
    assert config.scopes_supported == ("mailbox.read", "email.send")
    assert config.allowed_origins == ("https://app.sendmux.ai", "http://localhost:6274")


@pytest.mark.parametrize("issuer_env", ["SENDMUX_MCP_OAUTH_ISSUER", "QUBRICS_MCP_OAUTH_ISSUER"])
@pytest.mark.parametrize("mcp_origin", ["https://mcp.sendmux.ai", "https://mcp.qubrics.com"])
def test_hosted_auth_accepts_both_issuers_with_shared_jwks(
    monkeypatch: pytest.MonkeyPatch,
    issuer_env: str,
    mcp_origin: str,
) -> None:
    issuers = ("https://app.sendmux.ai", "https://app.qubrics.com")
    mcp_audiences = ("https://mcp.sendmux.ai/mcp", "https://mcp.qubrics.com/mcp")
    a2a_audience = "https://a2a.sendmux.ai/a2a/v1"
    keys = RSAKeyPair.generate()
    public_key = jwk.import_key(keys.public_key, "RSA", {"kid": "dual-issuer-test"}).as_dict()
    jwks_uri = "https://app.sendmux.ai/.well-known/jwks.json"
    monkeypatch.setenv(issuer_env, ",".join(issuers))
    monkeypatch.setenv("SENDMUX_MCP_RESOURCE_BASE_URL", mcp_origin)
    monkeypatch.setenv("SENDMUX_MCP_JWKS_URI", jwks_uri)

    async def fetch_jwks(_client: httpx2.AsyncClient, url: str) -> httpx2.Response:
        assert url == jwks_uri
        return httpx2.Response(200, json={"keys": [public_key]}, request=httpx2.Request("GET", url))

    monkeypatch.setattr(httpx2.AsyncClient, "get", fetch_jwks)

    async def run() -> None:
        runtime = hosted_runtime_config_from_env()
        server = create_hosted_server(runtime)
        assert isinstance(server.auth, RemoteAuthProvider)
        verifier = server.auth.token_verifier
        app = create_hosted_http_app(runtime)
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="https://a2a.sendmux.ai",
        ) as client:
            for issuer in issuers:
                for mcp_audience in mcp_audiences:
                    mcp_token = keys.create_token(issuer=issuer, audience=mcp_audience, kid="dual-issuer-test")
                    assert await verifier.verify_token(mcp_token) is not None
                a2a_token = keys.create_token(issuer=issuer, audience=a2a_audience, kid="dual-issuer-test")
                assert await verifier.verify_token(a2a_token) is None
                response = await client.post(
                    "/a2a/v1/message:send",
                    content=b"{}",
                    headers={
                        "Authorization": f"Bearer {a2a_token}",
                        "A2A-Version": "0.3",
                        "Content-Type": "application/a2a+json",
                    },
                )
                assert response.status_code == 400
                assert response.json()["error"]["details"][0]["reason"] == "VERSION_NOT_SUPPORTED"

            unknown_issuer = keys.create_token(
                issuer="https://attacker.example", audience=mcp_audiences[0], kid="dual-issuer-test",
            )
            assert await verifier.verify_token(unknown_issuer) is None
            unknown_resource = keys.create_token(
                issuer=issuers[0], audience="https://mcp.qubrics.com/custom", kid="dual-issuer-test",
            )
            assert await verifier.verify_token(unknown_resource) is None
            for issuer, audience in [
                ("https://attacker.example", a2a_audience),
                *((issuers[0], mcp_audience) for mcp_audience in mcp_audiences),
            ]:
                token = keys.create_token(issuer=issuer, audience=audience, kid="dual-issuer-test")
                rejected = await client.post(
                    "/a2a/v1/message:send", json={}, headers={"Authorization": f"Bearer {token}"},
                )
                assert rejected.status_code == 401

    asyncio.run(run())


def test_hosted_runtime_config_defaults_to_app_origin_only(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SENDMUX_MCP_APP_ORIGIN", "https://app.sendmux.ai")
    monkeypatch.delenv("SENDMUX_MCP_ALLOWED_ORIGINS", raising=False)
    monkeypatch.delenv("SENDMUX_MCP_SCOPES_SUPPORTED", raising=False)

    config = hosted_runtime_config_from_env()

    assert config.allowed_origins == ("https://app.sendmux.ai",)
    assert config.scopes_supported == HOSTED_MCP_DISCOVERY_SCOPES


def test_hosted_runtime_config_rejects_wildcard_origin(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SENDMUX_MCP_ALLOWED_ORIGINS", "*")

    with pytest.raises(ValueError, match="wildcard"):
        hosted_runtime_config_from_env()


def test_origin_from_url_strips_api_path() -> None:
    assert origin_from_url("https://app.sendmux.ai/api/v1") == "https://app.sendmux.ai"
