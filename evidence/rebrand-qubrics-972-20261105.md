# A2A service source qualification for qubrics/qubrics#972

Status: source qualified locally; PR, merge and deployment remain separate gates.

## Cause and scope

The hosted service owns the card, rather than the marketing proxy. `packages/python/mcp/sendmux_mcp/a2a.py` built a single legacy card and resource metadata response. `hosted.py` likewise fixed both the JWT audience and internal proxy resource to the legacy URL, regardless of the existing provisioned service alias.

The change precomputes the two finite service identities and selects their routes by exact normalised host. The Qubrics card uses Qubrics copy throughout, the qualified `https://a2a.qubrics.com/a2a/v1` interface and `https://app.qubrics.com` OAuth URLs. JWT validation and proxy envelopes bind to that identity's exact resource. Legacy hosts retain their existing card, metadata, challenge and protocol fields; package version follows the deployed package. Unknown hosts retain the existing legacy response and cannot supply arbitrary URLs. Each identity has a distinct card cache validator.

Canonical pattern: `hosted.py` already selects finite MCP metadata routes by exact host. App-side resource validation already permits both exact A2A resources; no app change is included.

## Local verification

- New public HTTP official-client test failed before the change: `assert 'Sendmux A2A' == 'Qubrics A2A'` (`red-qubrics.log`). It now passes using a signed Qubrics-audience JWT and read-only `managementListDomains`, with matching Qubrics proxy resource. MCP and legacy-audience tokens fail on the Qubrics resource.
- Adjacent public host/cache boundary failed when both card identities shared `ETag: "2.2.0"` (`red-boundary.log`). It now passes: per-host 304, cross-identity 200, GET/HEAD/method handling, case normalisation, suffix and port spoof boundaries, unknown-host legacy metadata/challenge.
- `pnpm exec .tmp/python-venv/bin/python -m pytest packages/python/mcp/tests/test_a2a_server.py packages/python/mcp/tests/test_hosted_server.py packages/python/mcp/tests/test_hosted_auth.py -q --disable-warnings`: exit 0, 42 passed. Existing legacy assertions were preserved.
- `pnpm exec .tmp/python-venv/bin/python -m mypy packages/python/mcp`: exit 0, 34 source files checked. The initial typecheck caught `BaseRoute.path`; precomputed Route-only maps resolve it.
- Metadata polish: fresh-reader Truth rubric passed, then one humanize pass retained the concise technical metadata unchanged. Protected brand, URLs, scopes, protocol and claims checked against source; no new claims.
- Package contract provenance regenerated through `python -m sendmux_mcp.contract`: only the two edited source hashes change. Initial contract check failed because `load_contract()` validates these hashes; no MCP tool/runtime contract content changes.
- Initial drift gate picked up unrelated current-docs rebrand examples/defaults and regenerated other language clients. Those generated changes were discarded; this service-only change uses the repository's committed MCP OpenAPI snapshots via supported `OPENAPI_INPUT_DIR`, retaining the source's published input contract.
- Local logs: SDK MAIN `.claude/artifacts/rebrand-qubrics-972/`. Full suite/build and conformance remain CI responsibilities.

## Release handoff to parent #972 owner

Parent measured before-change cards on candidate SITE, frozen legacy SITE and both direct A2A hosts: TLS verified; HTTP 200 JSON; all legacy name/interface. Both direct protocol endpoints returned HTTP 401 `application/a2a+json` and the legacy resource-metadata challenge. Existing unmodified SITE link-header verifier failed exactly the Qubrics A2A interface assertion. Raw public readbacks are in app MAIN `.claude/artifacts/rebrand-qubrics-972/`.

Named rollback image: `privregistry.jaa.nz/sendmux/sendmux-mcp:v1.0.17@sha256:151ff1179f9c1dd6ada5bc2b0ffd47e08da3cfef982e488f605d7b1a04703c3f`. Parent traced its source to SDK `python-mcp-v2.1.3`, commit `7c0c55b1`. Current source package is 2.2.0; this version delta and existing-main uptake must be explicit in the Ops slot packet.

Live runtime still has singleton `https://app.sendmux.ai` issuer/authorization-server/allowed-origin values, whereas already-reviewed infrastructure source contains both app hosts. Forward deployment requires the approved image and those three dual-host values; rollback restores the named image and singleton values. Parent owns exact source/tag/CI pin, image build, Ops slot approval, merge, rollout, before/after reads and SITE verification. No DNS, Custom Domain, Worker route/rule, credentials or package/tag publication is included in this source PR.

Acceptance remains open until deployment and fresh candidate/legacy readbacks. This source PR must not auto-close #972.
