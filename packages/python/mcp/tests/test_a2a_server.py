from __future__ import annotations

import asyncio
import json
import re
from dataclasses import replace
from pathlib import Path

import httpx
import httpx2
import pytest
from a2a.client import ClientConfig, ClientFactory
from a2a.client.card_resolver import A2ACardResolver
from a2a.helpers import get_data_parts, new_data_message
from a2a.server.request_handlers.response_helpers import agent_card_to_dict
from a2a.types import Role, SendMessageRequest
from fastmcp.server.auth import AccessToken
from fastmcp.server.auth.providers.jwt import RSAKeyPair
from joserfc import jwk

from qubrics.mcp.a2a import (
    A2A_RESOURCE_URL,
    A2AHostedProxy,
    A2AOperationCatalog,
    A2AOperationRequest,
    build_a2a_agent_card,
)
from qubrics.mcp.config import ServerConfig
from qubrics.mcp.curation import HOSTED_BACKING_TOOLS_BY_SURFACE, OPENAPI_TOOLS_BY_SURFACE
from qubrics.mcp.hosted import (
    HOSTED_MCP_DISCOVERY_SCOPES,
    HostedServerRuntimeConfig,
    create_hosted_http_app,
)
from qubrics.mcp.hosted_proxy import HostedProxyConfig, build_hosted_operation_manifest
from qubrics.mcp.specs import load_spec, prepare_for_fastmcp


def test_agent_card_advertises_a2a_1_0_http_json_and_oauth() -> None:
    card = agent_card_to_dict(build_a2a_agent_card())
    pyproject = (Path(__file__).parents[1] / "pyproject.toml").read_text()
    project = pyproject.split("[project]", maxsplit=1)[1].split("\n[", maxsplit=1)[0]
    package_version = re.search(r'^version = "([^"]+)"$', project, re.MULTILINE)

    assert card["name"] == "Qubrics A2A"
    assert package_version is not None
    assert card["version"] == package_version.group(1)
    assert card["description"]
    assert card["supportedInterfaces"] == [
        {
            "url": A2A_RESOURCE_URL,
            "protocolBinding": "HTTP+JSON",
            "protocolVersion": "1.0",
        }
    ]
    assert card["capabilities"] == {
        "streaming": False,
        "pushNotifications": False,
        "extendedAgentCard": False,
    }
    assert card["defaultInputModes"] == ["application/json"]
    assert card["defaultOutputModes"] == ["application/json"]
    assert [skill["id"] for skill in card["skills"]] == ["mailbox", "management", "sending"]
    assert all(skill["name"] and skill["description"] and skill["tags"] for skill in card["skills"])

    oauth = card["securitySchemes"]["oauth2"]["oauth2SecurityScheme"]
    assert oauth["oauth2MetadataUrl"] == "https://app.qubrics.com/.well-known/oauth-authorization-server"
    assert oauth["flows"]["authorizationCode"]["authorizationUrl"] == (
        "https://app.qubrics.com/mcp/oauth/authorize"
    )
    assert oauth["flows"]["authorizationCode"]["tokenUrl"] == "https://app.qubrics.com/mcp/oauth/token"
    assert oauth["flows"]["authorizationCode"]["pkceRequired"] is True
    assert set(oauth["flows"]["authorizationCode"]["scopes"]) == set(HOSTED_MCP_DISCOVERY_SCOPES)
    assert card["securityRequirements"] == [{"schemes": {"oauth2": {}}}]


def test_a2a_operation_catalog_has_full_hosted_operation_parity() -> None:
    manifests = []
    expected: set[str] = set()
    for surface in ("mailbox", "management", "sending"):
        config = ServerConfig(surfaces=(surface,), api_key=None)
        spec = prepare_for_fastmcp(load_spec(config), base_url=config.api_base_url)
        manifests.append(build_hosted_operation_manifest(spec, surface))
        expected.update(tool.operation_id for tool in OPENAPI_TOOLS_BY_SURFACE[surface])
        expected.update(tool.operation_id for tool in HOSTED_BACKING_TOOLS_BY_SURFACE[surface])

    catalog = A2AOperationCatalog(tuple(manifests))

    assert set(catalog.operation_ids) == expected
    assert {catalog.require("mailboxListMessages").surface, catalog.require("managementListDomains").surface} == {
        "mailbox",
        "management",
    }
    assert catalog.require("sendingSendEmail").surface == "sending"


def test_a2a_proxy_builds_exact_audience_bound_internal_envelope() -> None:
    async def run() -> None:
        captured: list[httpx.Request] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            captured.append(request)
            return httpx.Response(200, json={"ok": True, "data": []}, request=request)

        config = ServerConfig(surfaces=("management",), api_key=None)
        spec = prepare_for_fastmcp(load_spec(config), base_url=config.api_base_url)
        catalog = A2AOperationCatalog((build_hosted_operation_manifest(spec, "management"),))
        proxy = A2AHostedProxy(
            HostedProxyConfig(
                proxy_url="https://app.sendmux.ai/api/internal/mcp/proxy",
                upstream_base_url=config.api_base_url,
                internal_bearer_token="internal-service-token",
                resource=A2A_RESOURCE_URL,
                protocol="a2a",
            ),
            catalog=catalog,
            inner=httpx.MockTransport(handler),
        )

        response = await proxy.execute(
            A2AOperationRequest.model_validate(
                {
                    "operationId": "managementGetDomain",
                    "pathParameters": {"public_id": "dom_123"},
                    "query": {"include": ["dns", "status"]},
                    "headers": {"If-None-Match": '"etag"'},
                }
            ),
            grant_id="a2a_grant_public",
        )

        assert response.status_code == 200
        assert len(captured) == 1
        assert captured[0].headers["authorization"] == "Bearer internal-service-token"
        envelope = json.loads((await captured[0].aread()).decode())
        assert envelope == {
            "grant_id": "a2a_grant_public",
            "resource": A2A_RESOURCE_URL,
            "protocol": "a2a",
            "operation_id": "managementGetDomain",
            "tool_name": "management_get_domain",
            "surface": "management",
            "method": "GET",
            "path": "/domains/dom_123",
            "query": "include=dns&include=status",
            "headers": {"if-none-match": '"etag"'},
            "body_base64": None,
        }

        await proxy.aclose()

    asyncio.run(run())


def test_official_a2a_client_discovers_and_executes_without_task_routes() -> None:
    class StaticVerifier:
        async def verify_token(self, token: str) -> AccessToken | None:
            if token != "a2a_access_token":
                return None
            return AccessToken(
                token=token,
                client_id="a2a_client_public",
                scopes=["domain.read"],
                claims={
                    "grant_id": "a2a_grant_public",
                    "permissions": ["domain.read"],
                    "surface": ["management"],
                },
            )

    async def run() -> None:
        captured: list[httpx.Request] = []

        async def proxy_handler(request: httpx.Request) -> httpx.Response:
            captured.append(request)
            return httpx.Response(
                200,
                json={"ok": True, "data": [{"id": "dom_123"}]},
                headers={"content-type": "application/json", "x-request-id": "req_a2a"},
                request=request,
            )

        app = create_hosted_http_app(
            hosted_runtime(),
            a2a_token_verifier=StaticVerifier(),
            a2a_proxy_transport=httpx.MockTransport(proxy_handler),
        )
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="https://a2a.qubrics.com",
            headers={"Authorization": "Bearer a2a_access_token"},
        ) as http_client:
            card_response = await http_client.get("/.well-known/agent-card.json")
            assert card_response.status_code == 200
            assert "max-age=" in card_response.headers["cache-control"]
            assert card_response.headers["etag"]
            assert card_response.headers["strict-transport-security"].startswith("max-age=")

            cached_card_response = await http_client.get(
                "/.well-known/agent-card.json",
                headers={"If-None-Match": card_response.headers["etag"]},
            )
            assert cached_card_response.status_code == 304
            assert cached_card_response.content == b""

            resource_response = await http_client.get("/.well-known/oauth-protected-resource")
            assert resource_response.status_code == 200
            assert resource_response.json()["resource"] == A2A_RESOURCE_URL
            assert resource_response.headers["strict-transport-security"].startswith("max-age=")

            missing_auth = await http_client.post(
                "/a2a/v1/message:send",
                headers={"Authorization": ""},
                json={},
            )
            assert missing_auth.status_code == 401
            assert missing_auth.headers["content-type"] == "application/a2a+json"
            assert missing_auth.headers["www-authenticate"].startswith("Bearer resource_metadata=")
            assert missing_auth.headers["strict-transport-security"].startswith("max-age=")

            unsupported_version = await http_client.post(
                "/a2a/v1/message:send",
                content=b"{}",
                headers={"A2A-Version": "0.3", "Content-Type": "application/a2a+json"},
            )
            assert unsupported_version.status_code == 400
            assert unsupported_version.headers["content-type"] == "application/a2a+json"
            assert unsupported_version.json()["error"]["details"][0]["reason"] == "VERSION_NOT_SUPPORTED"

            unsupported_minor_version = await http_client.post(
                "/a2a/v1/message:send",
                content=b"{}",
                headers={"A2A-Version": "1.1", "Content-Type": "application/a2a+json"},
            )
            assert unsupported_minor_version.status_code == 400
            assert unsupported_minor_version.json()["error"]["details"][0]["reason"] == "VERSION_NOT_SUPPORTED"

            assert (await http_client.post("/a2a/v1/message:stream", json={})).status_code == 404
            assert (await http_client.get("/a2a/v1/tasks/task_123")).status_code == 404

            card = await A2ACardResolver(http_client, "https://a2a.qubrics.com").get_agent_card()
            client = ClientFactory(
                ClientConfig(
                    streaming=False,
                    httpx_client=http_client,
                    supported_protocol_bindings=["HTTP+JSON"],
                    accepted_output_modes=["application/json"],
                )
            ).create(card)
            request = SendMessageRequest(
                message=new_data_message(
                    {
                        "operationId": "managementListDomains",
                        "query": {"limit": 10},
                    },
                    media_type="application/json",
                    role=Role.ROLE_USER,
                )
            )
            responses = [response async for response in client.send_message(request)]

            assert len(responses) == 1
            assert responses[0].HasField("message")
            result = get_data_parts(responses[0].message.parts)
            assert result == [
                {
                    "ok": True,
                    "status": 200,
                    "headers": {"content-type": "application/json", "x-request-id": "req_a2a"},
                    "body": {"ok": True, "data": [{"id": "dom_123"}]},
                }
            ]

        assert len(captured) == 1
        envelope = json.loads((await captured[0].aread()).decode())
        assert envelope["grant_id"] == "a2a_grant_public"
        assert envelope["resource"] == A2A_RESOURCE_URL
        assert envelope["protocol"] == "a2a"
        assert envelope["operation_id"] == "managementListDomains"

    asyncio.run(run())


def test_qubrics_a2a_client_discovers_and_executes_with_its_resource(monkeypatch: pytest.MonkeyPatch) -> None:
    keys = RSAKeyPair.generate()
    public_key = jwk.import_key(keys.public_key, "RSA", {"kid": "a2a-rebrand-test"}).as_dict()
    resource = "https://a2a.qubrics.com/a2a/v1"

    async def fetch_jwks(_client: httpx2.AsyncClient, url: str) -> httpx2.Response:
        assert url == "https://app.sendmux.ai/.well-known/jwks.json"
        return httpx2.Response(200, json={"keys": [public_key]}, request=httpx2.Request("GET", url))

    monkeypatch.setattr(httpx2.AsyncClient, "get", fetch_jwks)

    async def run() -> None:
        captured: list[httpx.Request] = []

        async def proxy_handler(request: httpx.Request) -> httpx.Response:
            captured.append(request)
            return httpx.Response(200, json={"ok": True, "data": []}, request=request)

        app = create_hosted_http_app(
            replace(hosted_runtime(), issuer=["https://app.sendmux.ai", "https://app.qubrics.com"]),
            a2a_proxy_transport=httpx.MockTransport(proxy_handler),
        )
        token = keys.create_token(
            issuer="https://app.qubrics.com",
            audience=resource,
            scopes=["domain.read"],
            additional_claims={
                "grant_id": "a2a_grant_public",
                "permissions": ["domain.read"],
                "surface": ["management"],
            },
            kid="a2a-rebrand-test",
        )
        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app),
                base_url="https://a2a.qubrics.com",
                headers={"Authorization": f"Bearer {token}"},
            ) as http_client:
                response = await http_client.get("/.well-known/agent-card.json")
                assert response.status_code == 200
                assert response.headers["content-type"].startswith("application/json")
                card_json = response.json()
                assert card_json["name"] == "Qubrics A2A"
                assert "Sendmux" not in response.text
                assert "sendmux.ai" not in response.text
                assert card_json["supportedInterfaces"] == [
                    {"url": resource, "protocolBinding": "HTTP+JSON", "protocolVersion": "1.0"},
                ]
                oauth = card_json["securitySchemes"]["oauth2"]["oauth2SecurityScheme"]
                assert oauth["oauth2MetadataUrl"] == "https://app.qubrics.com/.well-known/oauth-authorization-server"
                assert oauth["flows"]["authorizationCode"]["authorizationUrl"] == (
                    "https://app.qubrics.com/mcp/oauth/authorize"
                )
                assert oauth["flows"]["authorizationCode"]["tokenUrl"] == "https://app.qubrics.com/mcp/oauth/token"
                metadata = await http_client.get("/.well-known/oauth-protected-resource")
                assert metadata.status_code == 200
                assert metadata.json()["resource"] == resource
                assert metadata.json()["resource_name"] == "Qubrics A2A"
                assert metadata.json()["authorization_servers"] == ["https://app.qubrics.com"]
                unauthenticated = await http_client.post(
                    "/a2a/v1/message:send", json={}, headers={"Authorization": ""},
                )
                assert unauthenticated.status_code == 401
                assert 'resource_metadata="https://a2a.qubrics.com/.well-known/oauth-protected-resource"' in (
                    unauthenticated.headers["www-authenticate"]
                )

                card = await A2ACardResolver(http_client, "https://a2a.qubrics.com").get_agent_card()
                client = ClientFactory(
                    ClientConfig(
                        streaming=False,
                        httpx_client=http_client,
                        supported_protocol_bindings=["HTTP+JSON"],
                        accepted_output_modes=["application/json"],
                    )
                ).create(card)
                request = SendMessageRequest(
                    message=new_data_message(
                        {"operationId": "managementListDomains", "query": {"limit": 10}},
                        media_type="application/json",
                        role=Role.ROLE_USER,
                    )
                )
                responses = [response async for response in client.send_message(request)]
                assert len(responses) == 1
                assert get_data_parts(responses[0].message.parts)[0]["status"] == 200

                for audience in ("https://mcp.qubrics.com/mcp", "https://a2a.sendmux.ai/a2a/v1"):
                    wrong_token = keys.create_token(
                        issuer="https://app.qubrics.com", audience=audience, kid="a2a-rebrand-test",
                    )
                    rejected = await http_client.post(
                        "/a2a/v1/message:send", json={}, headers={"Authorization": f"Bearer {wrong_token}"},
                    )
                    assert rejected.status_code == 401

        assert len(captured) == 1
        envelope = json.loads((await captured[0].aread()).decode())
        assert envelope["resource"] == resource
        assert envelope["protocol"] == "a2a"
        assert envelope["grant_id"] == "a2a_grant_public"
        assert envelope["operation_id"] == "managementListDomains"

    asyncio.run(run())


def test_a2a_discovery_separates_host_identities_and_cache_validators() -> None:
    async def run() -> None:
        app = create_hosted_http_app(hosted_runtime())
        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as client:
                path = "/.well-known/agent-card.json"
                legacy = await client.get(f"https://a2a.sendmux.ai{path}")
                qubrics = await client.get(f"https://a2a.qubrics.com{path}")
                assert legacy.status_code == qubrics.status_code == 200
                assert legacy.json()["name"] == "Sendmux A2A"
                assert legacy.json()["supportedInterfaces"][0]["url"] == "https://a2a.sendmux.ai/a2a/v1"
                assert qubrics.json()["name"] == "Qubrics A2A"
                assert qubrics.json()["supportedInterfaces"][0]["url"] == "https://a2a.qubrics.com/a2a/v1"
                assert legacy.headers["etag"] != qubrics.headers["etag"]

                for origin, response in (("https://a2a.sendmux.ai", legacy), ("https://a2a.qubrics.com", qubrics)):
                    assert response.headers["access-control-allow-origin"] == "*"
                    assert response.headers["strict-transport-security"].startswith("max-age=")
                    cached = await client.get(f"{origin}{path}", headers={"If-None-Match": response.headers["etag"]})
                    assert cached.status_code == 304
                    assert cached.content == b""
                    other_etag = qubrics.headers["etag"] if response is legacy else legacy.headers["etag"]
                    fresh = await client.get(f"{origin}{path}", headers={"If-None-Match": other_etag})
                    assert fresh.status_code == 200
                    assert fresh.content == response.content
                    assert (await client.head(f"{origin}{path}")).status_code == 200
                    assert (await client.post(f"{origin}{path}")).status_code == 405

                mixed_case = await client.get(
                    f"https://a2a.qubrics.com{path}", headers={"Host": "A2A.QUBRICS.COM"},
                )
                assert mixed_case.content == qubrics.content
                for host in ("a2a.qubrics.com.evil.example", "a2a.qubrics.com:8443", "unrecognised.example"):
                    unrecognised = await client.get(f"https://{host}{path}")
                    assert unrecognised.status_code == 200
                    assert unrecognised.content == qubrics.content
                    metadata = await client.get(f"https://{host}/.well-known/oauth-protected-resource")
                    assert metadata.json()["resource"] == "https://a2a.qubrics.com/a2a/v1"
                    challenge = await client.post(f"https://{host}/a2a/v1/message:send", json={})
                    assert challenge.status_code == 401
                    assert 'resource_metadata="https://a2a.qubrics.com/.well-known/oauth-protected-resource"' in (
                        challenge.headers["www-authenticate"]
                    )

    asyncio.run(run())


def hosted_runtime() -> HostedServerRuntimeConfig:
    return HostedServerRuntimeConfig(
        issuer="https://app.sendmux.ai",
        authorization_servers=("https://app.sendmux.ai",),
        jwks_uri="https://app.sendmux.ai/.well-known/jwks.json",
        resource_base_url="https://mcp.sendmux.ai",
        proxy_url="https://app.sendmux.ai/api/internal/mcp/proxy",
        internal_bearer_token="internal-service-token",
        mcp_path="/mcp",
        host="127.0.0.1",
        port=8765,
        stateless_http=True,
        scopes_supported=HOSTED_MCP_DISCOVERY_SCOPES,
        allowed_origins=("https://app.sendmux.ai",),
    )
