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

PR367 CI run `42801545285` passed all language/runtime jobs but `verify` failed at `scripts/check-live-e2e-runner.mjs:436`. The source-text gate still required the two old service hosts after `go/livee2e/main.go:658` adopted the A18 Qubrics defaults. The gate now requires the exact new hosts and retains both environment fallback arguments and the existing rejection of URL literals passed as environment names. No check was skipped or relaxed. Raw CI failure: `pr367-ci-failed.log`. Local verification initially lacked the built TypeScript exports, then the native Python editable installations used by the nested language tests; those missing setup dependencies were identified directly and installed through the existing workspace build and pip editable commands. These setup failures are not green verification receipts.

After setup, `node scripts/check-live-e2e-runner-environment.test.mjs` exited 0 (`go-runner-gate-green.log`). This executes the unchanged nested language safety tests plus the exact fallback assertions. `node --check scripts/check-live-e2e-runner.mjs` and `git diff --check` also exited 0. The origin fix changes only the two expected hosts to the A18 defaults.

- SITE#193 remains OPEN under attachment HOLD. #898 is CLOSED.
- Legacy `sendmux.ai/go` and `/go/v3` go-get requests return HTTP 200 with meta tags. New Qubrics vanity paths return HTTP 522. Latest root readback: `go-public-readback.json`.
- SITE `src/middleware.ts:9–11` hardcodes the legacy metadata root; its existing routing exemption precedes redirects, but the crawl script has no go-get request proof. SITE owner must implement host-correct metadata and prove both hosts before/after redirect activation.
- Required metadata root is the host (`qubrics.com` or `sendmux.ai`) with repository `https://github.com/qubrics/qubrics-sdk`; a `/go` metadata prefix against the repository root would mis-map the module subdirectory.
- No Go v4 tag, new-path public clean install, Python/Ruby publication, pointer publication or registry mutation has run.

PR367's second CI run `42805322082` passed every language/runtime job but failed the publication fixtures. Released Skills v2.0.1 now reads MCP identity from the candidate's immutable `packages/python/mcp/pyproject.toml`; both synthetic fixture builders omitted that file, so inspection failed before the existing assertions. The focused unchanged positive case reproduced the exact missing-file error (`go-fixture-metadata-red.log`). Both builders now seed the legacy project metadata beside their legacy contract paths. With the reviewed v2.0.1 checker, the two existing positive cases passed, zero skipped (`go-fixture-metadata-green.log`, exit 0). A further focused release case caught that `releaseFixture` overwrote the seeded name when adding its version (`go-release-fixture-metadata-red.log`: Unsupported MCP project.name). That writer now preserves the name. The complete existing `pnpm test:publication-guard` gate against the identical reviewed/released checker passed 101/101, zero skipped, exit 0 (`go-publication-fixtures-v201.log`). Assertions and checker enforcement remain unchanged. This is distinct from the earlier stale Go-host gate diagnosis.

The Python candidate's fresh qualification against the exact released checker separately exposed a real namespace defect: `qubrics-mcp` maps to `qubrics_mcp`, but A18's native namespace uses `qubrics/mcp`. Legacy acceptance and changed-snapshot rejection passed; renamed positive acceptance failed. Origin evidence and exact identities are in the Python candidate's `evidence/rebrand-qubrics-sdk344-python-20261110.md`, raw `skills-3ad9e60-qualification.log`. Ops ASK sent to route the Skills origin correction and reviewed release. No SDK fallback, weakened assertion or checker retry.

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

Legacy pointer releases must install replacements, carry the specified Inactive classifier or post-install message, and preserve useful existing imports. Ops settled all twelve final old-name versions: each takes the SAME next-major version as its replacement in the table above, per [SemVer 2.0.0 item 8](https://semver.org/spec/v2.0.0.html#spec-item-8) and A10/A18. This avoids silently moving ~= / ~> pinned users across a breaking replacement. The exact twelve are recorded in MAIN `.claude/tasks/rebrand-qubrics-sdk344/pointer-version-decision.md`. This is a version decision, not publication approval. Published PyPI/RubyGems versions cannot be reused; yank only. MCP Registry server identity is distinct from the PyPI artifact identifier: the existing `io.github.Sendmux/sendmux-mcp` identity and ownership markers stay unchanged while the artifact reference becomes `qubrics-mcp`; no replacement server identity is specified or needed. New-name trusted-publisher ownership remains unproved. Every PyPI/RubyGems/pointer publication requires exact-artifact/version operator approval and operator execution; none is authorised by this evidence.

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

The source-consumer directory was removed by its existing runner. Shell tooling rejected deleting this task's `.tmp/go-codegen` with `rm -rf`: `rm -f style commands are not permitted. Use a safer approach`. No deletion retry or workaround was attempted. Ops subsequently chose normal `git worktree remove` at close-off to collect this task's caches with its worktree; no operator cache deletion ask remains. Shared SDK worktrees, sdk343 work and shared caches remain with their owners.

No publishing credentials were read or printed. Public install/publication and live vanity acceptance remain unproved. This task is not complete.
