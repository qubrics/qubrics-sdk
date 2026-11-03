# A19 hosted OAuth issuer and MCP resource compatibility

Source follow-on to [qubrics/qubrics#905](https://github.com/qubrics/qubrics/issues/905), authorised by Ops Watch on 3 November 2026. Based on SDK main `dff5cb89bccb5840d55071d23f79ff88c7e58040`, after SDK #345 merged. No package publication, registry write, version bump or production deployment.

## Cause and source change

`hosted_runtime_config_from_env()` previously passed `OAUTH_ISSUER` unchanged into both the MCP `JWTVerifier` and the A2A `JWTVerifier`. A comma-separated pair became one literal expected issuer; a token from either host failed exact issuer validation. Existing tests covered only a single issuer. The same input also became one fallback authorisation-server URL.

The existing `QUBRICS_MCP_OAUTH_ISSUER` / `SENDMUX_MCP_OAUTH_ISSUER` setting now accepts CSV. Single values retain the existing string representation; multiple values use FastMCP's native finite issuer list. Fallback discovery servers use the parsed values. Both verifiers retain one configured JWKS URL and their protocol-specific audience checks. Unknown issuers remain rejected.

Ops Watch additionally assigned the MCP server-card producer contract to this PR. SDK main's `hosted.resource` was still the legacy URL. The default and generated contract now use `https://mcp.qubrics.com/mcp`, with `hosted.resource_aliases: ["https://mcp.sendmux.ai/mcp"]`. Registry source metadata lists both endpoints; its existing validator compares both against the package contract. The application consumer reads `hosted.resource` and permits additive hosted fields (`scripts/check-mcp-server-card.ts` in the application repository).

The two approved MCP resource URLs are exact audience aliases. Custom origins and custom mounted paths retain their one exact configured audience. A2A tokens cannot authenticate to MCP; MCP tokens from either alias cannot authenticate to A2A. A2A's existing resource URL is unchanged. No hostname pattern, suffix or wildcard matching was added.

Canonical implementation: FastMCP 4.0.3 `JWTVerifier` accepts `issuer: str | list[str]` and `audience: str | list[str]`; its issuer and audience validation uses exact membership. Existing resource metadata, signing and remote-key retrieval remain in use.

## Red and green

Logs live under SDK MAIN `.claude/artifacts/rebrand-qubrics-905-sdk/` through this worktree's artifact symlink.

| Public seam | Red evidence | Green evidence |
| --- | --- | --- |
| Configured MCP verification and A2A HTTP authentication | `dual-issuer-red.log`: `issuer mismatch` for `https://app.sendmux.ai`, expected the literal CSV; 2 failed | `focused-green.log`: 38 passed, including both environment-name families, both issuers and both configured MCP origins |
| MCP resource audience aliases | `resource-audience-red.log`: audience mismatch between `https://mcp.sendmux.ai/mcp` and `https://mcp.qubrics.com/mcp`; 4 failed | Same 38-test focused run accepts both exact MCP audiences and rejects unknown resources and cross-protocol audiences |
| Contract producer | `resource-contract-red.log`: expected Qubrics resource, received legacy resource; 1 failed | `contract-green.log`: canonical resource plus permanent legacy alias and packaged/factory equality; 2 passed |

The JWT tests sign real RSA tokens and obtain the public key through one mocked outbound JWKS HTTP response. The verifier is not mocked. A2A success reaches its protocol validation response; invalid authentication returns 401. The initial fixture patched `httpx` although the installed verifier uses `httpx2`; that fixture error was corrected, then baseline red was re-proven with explicit issuer-mismatch evidence before final green.

Other local checks: mypy reports no issues in 34 source files (`mypy.log`); registry contract tests report 11 passed (`registry-contract.log`); `python -m sendmux_mcp.contract --check` exits 0 (`contract-check.log`); `git diff --check` exits 0. No tests were removed or skipped. Two existing audience assertions now expect the explicitly approved finite alias pair; custom-path assertions retain their exact original resource.

## Review repairs

Candidate reopened for two confirmed alias-path blockers found in the parent session's combined Standards/Spec review:

1. `create_remote_auth_provider()` accepted both MCP audiences, but `hosted_mcp_proxy_config()` fixed the outbound proxy resource to the runtime URL. `HostedProxyTransport._proxy_request()` copied that URL into the envelope. The application's `grantAllowsOperation()` requires the envelope resource to equal the stored grant resource, so a token for the opposite alias passed JWT authentication and failed the tool call. The transport now preserves the verified access token's scalar `aud` only when both it and the configured resource are members of the finite MCP alias set and the protocol is MCP. The application's exact grant/resource check stays intact. Custom resources and A2A keep their existing paths.
2. Root protected-resource metadata recognised only the configured MCP hostname; the opposite advertised MCP alias received A2A metadata. For standard MCP resource configurations, the router now recognises both exact MCP hostnames. Custom resources retain their configured-host behaviour, and A2A discovery stays separate.

`proxy-resource-red.log` shows both alias directions failing with the wrong envelope resource; `proxy-resource-green.log` reports 17 proxy tests passed. `metadata-alias-red.log` shows both configured origins returning the A2A resource on the opposite MCP host; `metadata-alias-green.log` reports seven metadata/custom-mount tests passed. The combined follow-up selection reports 63 passed and 16 deselected in `followup-focused-green.log`; the unchanged installed-reader/source-copy fixture selection is left to full CI. Every new test was seen red. The packaged contract was regenerated after the repairs; `followup-contract-check.log` exits 0, and `followup-mypy.log` reports no issues in 34 source files. No app isolation checks were relaxed.

Actual installed contract-reader output (`contract-cli-output.json`), after the official producer CLI regenerated the packaged artifact:

```json
{"resource": "https://mcp.qubrics.com/mcp", "resource_aliases": ["https://mcp.sendmux.ai/mcp"], "transports": ["streamable-http"]}
```

The current `qubrics/docs` main OpenAPI documents were fetched read-only and compared as parsed JSON with the SDK's committed input snapshots: both equal. This runtime-only change uses those committed snapshots for local generation. The repository pre-commit hook runs the existing full generator drift check; CI owns full package, build, conformance and consumer checks.

## Release boundaries

- Source PR only. Parent session coordinates review and merge; no self-merge from this SDK subtask.
- SDK publication/release remains on the operator's hard list.
- MCP deployment changes issuer configuration and requires ASK under rebrand rule 4, the `holds/deploy-sendmux-prod` slot and Ops Watch GO. The current production image must not receive CSV issuer configuration until it contains this parser.
- Rollback is the previous runtime image and manifest. No data, keys, clients or grants change.
- Live hosted journeys and operator console screenshots belong to the coordinated A19 release proof; focused source tests do not claim deployment or publication.

Parked: local pre-commit runs every language generator plus network dependency checks; propose moving that broad gate to CI under the existing gate policy. No hook changes included.
