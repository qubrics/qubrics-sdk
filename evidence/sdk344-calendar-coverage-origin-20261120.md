# Calendar coverage origin correction

Goal: remove remaining named calendar consumer bindings while preserving supported mail operations and opaque delivery history. This source-only correction authorises no package publication.

Status: coded, not merged. Reviewed against worktree base `82e32cdc538bed170c75cc3e5094a8055f0f6672`. Root owns the correction commit, normal CI, review replies and merge.

## Origin fixes

- Runner inventory comes from the generated CLI manifest (`scripts/run-live-e2e.mjs:455`), whose generator excludes calendar routes (`scripts/generate-cli.mjs:40`). Raw producer inventory remains 128 OpenAPI operations plus 2 custom MCP operations. Runnable inventory contains the remaining 118 OpenAPI operations plus those same 2 custom operations.
- `scripts/check-live-e2e-runner.mjs:29` now compares exact plan IDs with all scenario IDs except the literal ten held calendar IDs. Every held scenario must remain inventoried with no SDK, CLI or MCP adapter. Normal and all-gates plans cover every supported ID; existing mail-read and safety-gate checks remain.
- `scripts/check-live-e2e-coverage.mjs:731` checks adapter applicability before counting executable operations. Its generated matrix keeps all 130 rows and separates 60 executable, 60 safety-gated and 10 withheld operations. Three adapter-less calendar reads previously inflated the executable count.
- `scripts/check-surface-coverage.mjs:30` checks physical CLI modules independently of manifest membership, using the existing generator's default command naming (`scripts/generate-cli.mjs:308`). An orphan `mailbox/list-calendars.ts` is rejected. Existing SDK and manifest checks remain.
- Calendar-test removal also removed the shared environment helper used by mail safety tests. `scripts/test-live-e2e-safety.mjs:84` restores `origin/main`'s `withEnv` unchanged. Its all-gates and explicit-selection cases now compare every supported operation ID and inventory length instead of the stale 130-operation assumption.

Operator rule 12 intentionally removes exactly ten calendar consumer bindings. Replacing their old executable/gated assertions follows that approved behaviour; it does not lower supported-operation coverage. Raw scenarios, snapshots, CLI generated files, package metadata and safety permissions remain unchanged by these coverage fixes.

## Red and green receipts

Logs are under `.claude/artifacts/rebrand-qubrics-sdk344/` in the coordinating checkout.

| Check | Result | Log |
| --- | --- | --- |
| `node scripts/check-live-e2e-runner-environment.test.mjs` before correction | exit 1, `120 !== 130` | `calendar-coverage-runner-red.log` |
| Same command after inventory correction, before matrix correction | exit 1, `63 !== 60` | `calendar-coverage-runner-matrix-red.log` |
| `node --test --test-name-pattern='surface gate rejects withheld CLI modules' scripts/rust-surface-coverage.test.mjs` before checker correction | exit 1, orphan command accepted | `calendar-coverage-orphan-red.log` |
| `node scripts/check-live-e2e-coverage.mjs --write` | exit 0, matrix regenerated | `calendar-coverage-matrix-write.log` |
| `node --test scripts/rust-surface-coverage.test.mjs && pnpm check:surface-coverage` | exit 0, 3/3 tests, 0 skipped, 128-operation surface check | `calendar-coverage-surface-green.log` |
| `node --test --test-name-pattern='every send operation rejects\|draft and usage reads\|all-gates default\|JSON plans bind explicit' scripts/test-live-e2e-safety.mjs` before shared-helper/inventory correction | exit 1, missing `withEnv` and `120 !== 130` | `calendar-coverage-safety-origin-red.log` |
| `node --test --test-name-pattern='calendar bindings are withheld\|every send operation rejects\|draft and usage reads\|all-gates default\|JSON plans bind explicit' scripts/test-live-e2e-safety.mjs` after correction | exit 0, 9/9 tests, 0 skipped | `calendar-coverage-source-focused-green.log` |
| `node scripts/check-live-e2e-coverage.mjs` and `git diff --check` | exit 0 | Direct command receipts |

Tests added: orphan physical CLI command rejection in the existing surface fixture, with its unchanged healthy boundary. Tests removed: none in this correction. Existing stale inventory assertions now require exact supported IDs. No safety gate, failure assertion, timeout or workflow threshold was weakened.

## Local language setup and limits

An initial `pnpm check:live-e2e` reached and passed the corrected runner inventory, default/all-gates plans and matrix assertions, then failed inside the existing safety suite: 52 tests, 37 pass, 15 fail, 0 skipped (`calendar-coverage-live-green.log`; its attempted-green filename is not a passing verdict). Eight failures were the removed helper, one was stale inventory, and six initially encountered missing Python surface modules before HTTP or result assertions.

Canonical task-local Python setup followed `scripts/check-python.mjs:55-64` and the native cohort in `scripts/ci-consumers.mjs:22-24`:

```sh
.tmp/python-venv/bin/python -m pip install -r requirements-dev.txt
.tmp/python-venv/bin/python -m pip install -e packages/python/core -e packages/python/sending -e packages/python/mailbox -e packages/python/management -e packages/python/mcp
```

Both exited 0 (`calendar-coverage-python-requirements.log`, `calendar-coverage-python-native-install.log`). Only this task's existing venv changed; package source, configuration, requirements and lockfiles did not.

The existing six adapter cases were then run with `node --test --test-name-pattern='created IDs are persisted|language adapter runs substantive|expected API negative remains|expected API negatives require|Python and PHP changes certification|a child success cannot masquerade' scripts/test-live-e2e-safety.mjs`: 2 pass, 4 fail, 0 skipped (`calendar-coverage-adapter-focused.log`). Python imports and its previously blocked public-result cases now pass. The remaining cases reach Ruby, whose exact configured runtime is unavailable locally: `rbenv: version '3.4.12' is not installed` (`calendar-coverage-ruby-trace.log`). This is a local setup limitation, not a source diagnosis. No runtime installation, version fallback, pin change or knowingly-red full adapter rerun followed. Full language verification remains CI's responsibility.

No credentialed live run, workflow dispatch, publication, release, tag, protected environment or queue action occurred. Generated CLI inputs are unchanged by this correction; the published CLI digest was not recomputed here.

## Review dispositions

- Inline `4637031080`: valid, physical-command origin fixed and orphan fixture seen red then green.
- Review `5985733924`, outside-diff finding at `check-live-e2e-coverage.mjs:729`: valid, adapter applicability fixed and withheld operations separated from safety gates.
- Root owns final thread replies. Historical audit evidence and opaque delivery-history support remain untouched by this correction.
