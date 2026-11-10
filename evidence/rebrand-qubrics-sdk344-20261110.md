# SDK #344: Go source tracer and release audit

Goal: Own qubrics/qubrics-sdk#344 through every acceptance box, merged source and published packages.

Status: coded locally, not merged or published. This change is the Go source tracer only. No #344 acceptance box is claimed complete.

## Go source

Canonical per [Go major-version suffixes](https://go.dev/ref/mod#major-version-suffixes) and [repository version mapping](https://go.dev/ref/mod#vcs-version): `qubrics.com/go/v4@v4.0.0`, with tag `go/v4.0.0` because the module lives under `go/`. A bare `qubrics.com/go` cannot represent major 4. Existing `sendmux.ai/go/v3@v3.0.0` remains immutable.

The generator owns defaults and helper imports. All three clients now default to Qubrics service hosts. A17 header and environment twins, `SendmuxOption`, validation, explicit overrides and existing compatibility shims remain supported. Release Please has a one-time `release-as: 4.0.0`; remove it after the intended release PR exists.

## Measured local checks

Against base `f0e8b721acf62816475f43dd87b18fe025fa0e10`, unchanged `pnpm-lock.yaml`, and committed OpenAPI snapshots:

| Check | Result | Operator-local receipt |
| --- | --- | --- |
| New public-client default-origin test, before fix | Red for all three surfaces | `go-defaults-red.log` |
| `pnpm generate:go` | Exit 0 | `go-generate-exact.log` |
| `node scripts/check-go.mjs` | Exit 0 | `go-surface-check.log` |
| `go test ./...` | Exit 0, six packages | `go-test-green.log` |
| `go vet ./...` | Exit 0 | `go-vet-green.log` |
| `node scripts/ci-consumers.mjs go` | Exit 0, isolated source consumer removed | `go-consumer.log` |
| `pnpm test:release-state` | Exit 0, 32 tests, zero skipped | `go-release-state.log` |

Receipts reside under `/Users/rj/Desktop/GIT-REPOS/sendmux-sdk/.claude/artifacts/rebrand-qubrics-sdk344/`. Source-consumer checks use a local module replacement; they prove source imports and dependencies, not public publication or vanity discovery.

Observed red output included `request origin = "https://smtp.sendmux.ai", expected "https://smtp.qubrics.com"`, with equivalent app-host failures for Mailbox and Management. The existing public-client HTTP boundary catches restoring any legacy default. Existing security and dual-environment tests remain.

First generation failed because an overbroad brand replacement altered compatibility/security-family literals. The fix restored those literals and narrowed edits at the generator origin. `go-first-failure.diff` retains the failed delta. Sibling docs and committed snapshots had identical hashes; snapshot selection was not the cause. Final regeneration leaves no `oas_*` delta.

Two independent source reviews cover Standards and Spec. Copy receives the required fresh-reader critique, one aggregate humanize pass and protected-name/URL check. Historical v3/v2 instructions remain historical; all new v4 instructions explicitly say unpublished.

## External acceptance still outstanding

- SITE#193 remains OPEN under attachment HOLD. #898 is CLOSED.
- Legacy `sendmux.ai/go` and `/go/v3` go-get requests return HTTP 200 with meta tags. New Qubrics vanity paths return HTTP 522. Latest root readback: `go-public-readback.json`.
- SITE `src/middleware.ts:9–11` hardcodes the legacy metadata root; its existing routing exemption precedes redirects, but the crawl script has no go-get request proof. SITE owner must implement host-correct metadata and prove both hosts before/after redirect activation.
- Required metadata root is the host (`qubrics.com` or `sendmux.ai`) with repository `https://github.com/qubrics/qubrics-sdk`; a `/go` metadata prefix against the repository root would mis-map the module subdirectory.
- No Go v4 tag, new-path public clean install, Python/Ruby publication, pointer publication or registry mutation has run.

## Registry audit: A18-derived replacement versions

`registry-audit.json` measured every old project HTTP 200 at the version below and every new project HTTP 404. These responses do not prove ownership or reserve names. Each proposed replacement major is computed from the current published major plus one, per A18.

| Registry | Existing distribution | Published | Replacement | Next major |
| --- | --- | --- | --- | --- |
| PyPI | sendmux-core | 1.3.1 | qubrics-core | 2.0.0 |
| PyPI | sendmux-sdk | 3.0.1 | qubrics-sdk | 4.0.0 |
| PyPI | sendmux-mailbox | 2.0.2 | qubrics-mailbox | 3.0.0 |
| PyPI | sendmux-management | 2.0.1 | qubrics-management | 3.0.0 |
| PyPI | sendmux-sending | 1.6.0 | qubrics-sending | 2.0.0 |
| PyPI | sendmux-mcp | 2.2.0 | qubrics-mcp | 3.0.0 |
| PyPI | langchain-sendmux | 0.4.0 | langchain-qubrics | 1.0.0 |
| RubyGems | sendmux-core | 1.3.0 | qubrics-core | 2.0.0 |
| RubyGems | sendmux-sdk | 2.0.0 | qubrics-sdk | 3.0.0 |
| RubyGems | sendmux-mailbox | 2.0.2 | qubrics-mailbox | 3.0.0 |
| RubyGems | sendmux-management | 2.0.1 | qubrics-management | 3.0.0 |
| RubyGems | sendmux-sending | 1.5.0 | qubrics-sending | 2.0.0 |

Canonical Python packaging uses a native `qubrics` namespace, one component subtree per distribution, including the existing umbrella loader at `qubrics.sdk`; no distribution owns `qubrics/__init__.py`. A separately published project named `qubrics` is unnecessary. See [PyPA namespace guidance](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/). Ruby replacements use `Qubrics` as specified.

Legacy pointer releases must install replacements, carry the specified Inactive classifier or post-install message, and preserve useful existing imports. Their exact versions are absent from A18 and remain an operator decision. MCP Registry replacement identity is also absent from the spec; existing `io.github.Sendmux/sendmux-mcp` is held unchanged pending that decision. New-name trusted-publisher ownership remains unproved. Every PyPI/RubyGems/pointer publication requires exact-version operator approval and operator execution; none is authorised by this evidence.

## Parked release PR triage

All eight PRs remain OPEN, MERGEABLE, `autorelease: pending`; none was merged. Their release intent must be reconciled with the rename, not published unchanged.

| PR | Current proposal | Disposition |
| --- | --- | --- |
| #326 | python-mailbox 2.1.0 | Refresh after A18 namespace/major migration |
| #327 | python-management 2.1.0 | Refresh after A18 namespace/major migration |
| #328 | python-mcp 2.3.0 | Refresh after A18 migration and registry-identity decision |
| #329 | go 3.1.0 | Refresh to 4.0.0 after this source rename |
| #330 | rust 0.6.0 | Held: A18 supplies no replacement crate identity; no invented rename |
| #331 | ruby-sending 1.6.0 | Refresh after A18 namespace/major migration |
| #332 | ruby-mailbox 2.1.0 | Refresh after A18 namespace/major migration |
| #333 | ruby-management 2.1.0 | Refresh after A18 namespace/major migration |

Release PR merges trigger publishing workflows, so they remain held. Pending-publisher setup is distinct from publication: [PyPI documents that it does not reserve a name](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/).

## Cleanup and limits

The source-consumer directory was removed by its existing runner. Shell tooling rejected deleting this task's `.tmp/go-codegen` with `rm -rf`: `rm -f style commands are not permitted. Use a safer approach`. No deletion retry or workaround was attempted. Cache cleanup remains outstanding; shared SDK worktrees, sdk343 work and shared caches were retained.

No publishing credentials were read or printed. Public install/publication and live vanity acceptance remain unproved. This task is not complete.
