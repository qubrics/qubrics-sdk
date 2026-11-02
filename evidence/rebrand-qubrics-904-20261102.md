# A17 SDK integration contract aliases

Status: source finalisation and full drift verified after the calendar lease release on 2026-11-03; uncommitted, not merged, deployed or published. Base and fetched `origin/main`: `0dd32a2652f3fd7a9a8f7e2ab8976d79f1b1dc99`. Ticket: qubrics/qubrics#904, acceptance A17. SDK root/package README changes remain owned by #897.

## Source and behaviour

Qubrics environment names take precedence, with retained Sendmux fallbacks. MCP tools expose additive aliases while preserving original handlers. Generated native clients use the existing environment/URL configuration and preserve delegated-upload authentication independently of ordinary bearer credentials. Generators, rather than generated clients alone, own each correction.

Generation uses the task docs snapshots: app SHA256 `16439b3c0d9eee73554202cf909af6aade12b6f8d3390ddee922663ba061de1a`; sending SHA256 `3138c5f27e3c0ab8475d1ccaf7378815c12e12918c30a90e77e2115642bc3647`. Current canonical snapshots contain calendar contracts missing from this SDK baseline; generated calendar additions come from those snapshots, not invented local contracts.

## Upload authentication root cause

The sending contract now represents the two upload-token header families as alternative API-key schemes. Previously shared native authentication paths could treat any nonempty security list as bearer authentication, reading or leaking the main API credential during a delegated upload.

- Go generator preserves the existing bearer-only `SecuritySource`/`SecurityHandler` interfaces and resolves optional upload credentials without overwriting either explicit upload-token twin. Two explicit-header/source cases were red with Unauthorized before correction. Seven upload cases, environment selection and existing interface compatibility pass.
- TypeScript core excludes the exact two upload schemes from its bearer credential callback. Before correction the public upload test observed two main-credential reads instead of zero. Both header families now pass without reading the provider.
- Python generator excludes exact upload-only scheme lists from its bearer override. Both public upload-provider cases were red; ordinary OAuth paths retain their existing behaviour.
- Ruby generator `scripts/generate-ruby.mjs:297-321` preserves either explicit upload header and resolves upload-specific API keys directly. Delegating to generated `super` still evaluated the complete `auth_settings` hash, eagerly calling the bearer provider from generated configuration. The final source avoids that hash only for the two upload schemes. Both public upload tests originally raised `Delegated upload must not read the bearer credential`; final OAuth/upload suite passes. A subsequent incomplete response fixture failed deserialisation, then was corrected to the documented envelope without changing assertions.

Sibling review: PHP generated upload requests resolve exact upload API keys. Its pre-existing generic OAuth middleware adds Authorization regardless of operation metadata; reported as Parked, unchanged. Rust marks delegated binary upload unsupported, so no new supported upload adapter is inferred.

## Focused proof

Receipts live under the parent app's `.claude/artifacts/rebrand-qubrics-904/`; `sdk-final-handoff.md` and `sdk-final-status.txt` identify the exact source write set. No unchanged green check was repeated merely for resumption.

| Command / boundary | Final result | Receipt |
| --- | --- | --- |
| `go test ./sending -count=1` in `go/` | exit 0, upload/env/interface cases | `sdk-go-sending-final.log` |
| `node scripts/test-ts-helpers.mjs` | 41 passed, 0 skipped | `sdk-ts-env-upload-green.log` |
| CLI workspace build under heavy slot | exit 0 | `sdk-ts-cli-build-final.log` |
| `node scripts/test-cli-oauth.mjs` | 6 passed, 0 skipped | `sdk-cli-env-final.log` |
| `node --test scripts/generate-cli.test.mjs` | 1 passed, 0 skipped | `sdk-cli-capability-final.log` |
| Python OAuth and environment tests | 28 passed, 0 skipped | `sdk-python-oauth-env-green.log` |
| Python environment / unauthenticated aliases | 9 passed, 0 skipped | `sdk-python-env-alias-final.log` |
| Core/MCP mypy | success, 41 source files | `sdk-python-mypy-final.log` |
| PHP public environment configuration | 3 passed, 0 skipped | `sdk-php-env-final.log` |
| Ruby public aggregate environment seam | 1 run, 18 assertions, 0 failures/errors/skips | `sdk-ruby-env-green.log` |
| Ruby OAuth / delegated upload | 16 runs, 146 assertions, 0 failures/errors/skips | `sdk-ruby-oauth-final.log` |
| Rust OAuth/environment | 13 passed | `sdk-source-receipts.md` |

Final narrow Ruby review: Standards 0 hard violations / 0 heuristic findings; Spec 0 findings. Prior Go/TS/Python upload-auth reviews are clear. `git diff --check` exits 0. The final hash manifest `sdk-final-freeze-sha256.txt` was checked again after handback, all nine paths OK.

## Earlier dependencies and retained red proof

This section records the prior freeze. All three source dependencies below were resolved after Ops released the calendar leases; final proof follows.

Authenticated MCP aliases remain red: a permitted token lists/calls the original tool but not its alias. Two authenticated positive cases fail; two denied-permission cases pass. The shared registry lookups in `packages/python/mcp/sendmux_mcp/permissions.py:100,133` use the prefixed alias instead of its canonical name. The unapplied two-line `sdk-mcp-permission-aliases.patch` fixes both lookups without changing permissions, but calendar owns this frozen path. `sdk-mcp-auth-alias-rca.md` records the full trace and red receipts.

The pre-commit hook `.githooks/pre-commit:4` unconditionally invokes `pnpm drift:check`, which runs MCP generation and writes frozen `packages/python/mcp/sendmux_mcp/openapi/openapi-app.json`. No hook invocation, bypass, commit or push was attempted while that lease stands.

Coverage/provenance generation also requires owner-supplied Rust and frozen MCP curation decisions for nine calendar operations: `mailboxCreateCalendar`, `mailboxCreateCalendarEvent`, `mailboxDeleteCalendarEvent`, `mailboxGetCalendar`, `mailboxGetCalendarEvent`, `mailboxGetCalendarEventChanges`, `mailboxListCalendarEvents`, `mailboxListCalendars`, `mailboxUpdateCalendarEvent`. The guarded writer refused to invent these decisions. Receipt: `sdk-coverage-provenance-blocked.log`.

Frozen paths retain their original SHA256 values:

- `permissions.py`: `aa27f177b17871d954327a8a6d063dfb5b1f87d1a77d661893739137a1d5e2ca`.
- `curation.py`: `ba8e91c99cf203654e25a766db3bb02d1fa2bfa5768ad6a3edb69df03ad9774f`.
- embedded `openapi-app.json`: `dd39d2329fc51098455f499e551ad3e33f14bc9243c793dfa47fc353a57f62ea`.

Full drift/build/required CI remain unqualified until the lease releases and source can commit/push normally. Docs#78 keeps its existing MCP pin and release-facts snippet until a compatible publication is verified. No version is invented and no publication is authorised.

## Source finalisation after calendar release

Ops released all calendar SDK leases on 2026-11-03. Seven owner-supplied source paths were reconciled from the read-only calendar candidate, not its generated outputs:

- `packages/python/mcp/sendmux_mcp/permissions.py`: nine calendar permission entries, then the existing two-line alias correction.
- `packages/python/mcp/sendmux_mcp/curation.py`: nine curated calendar tools and their read/destructive/idempotent metadata.
- `packages/python/mcp/sendmux_mcp/hosted_proxy.py:263`: static routes precede parameter routes, so the calendar changes route resolves correctly.
- `packages/python/mcp/tests/test_permissions.py` and `test_hosted_proxy.py`: unchanged owner permission-isolation and canonical-route cases.
- `packages/python/tests/test_mcp.py`: owner calendar expectations combined with existing aliases; 74 originals and 74 aliases retain complete metadata.
- `rust/operation-decisions.json`: all nine owner decisions remain `raw-json-only`, with no named method or live certification inferred.

`permissions_for_tool` at permissions.py:109 and the surface lookup at :142 strip exactly one leading `qubrics_`. Both lookups use the same original registries. Unknown/nested aliases still fail; all permission and surface claim checks remain. The earlier authenticated positive red cases now pass alongside denied-token cases. No permission widening or bypass.

Normal MCP generation replaced the released embedded app snapshot with canonical app SHA256 `16439b3c0d9eee73554202cf909af6aade12b6f8d3390ddee922663ba061de1a`; sending remains `3138c5f27e3c0ab8475d1ccaf7378815c12e12918c30a90e77e2115642bc3647`. Guarded generation updated the surface matrix and Rust provenance from these same inputs. Existing environment and delegated-upload source corrections were preserved. The six prior Ruby source/runtime fingerprints still match.

| Command | Result | Parent artifact receipt |
| --- | --- | --- |
| `.tmp/python-venv/bin/python -m pytest packages/python/mcp/tests/test_contract_aliases.py -k authenticated_http -q` | exit 0, 4 passed / 6 deselected | `sdk-mcp-auth-alias-resume-green.log` |
| `OPENAPI_INPUT_DIR=<task-docs> AGENT_TASK=rebrand-qubrics-904 heavy-slot.sh pnpm generate:mcp` | exit 0 | `sdk-resume-generate-mcp.log` |
| `OPENAPI_INPUT_DIR=<task-docs> node scripts/check-surface-coverage.mjs --write --write-provenance` | exit 0, 127 operations | `sdk-resume-coverage-provenance.log` |
| `.tmp/python-venv/bin/python -m pytest packages/python/mcp/tests/test_permissions.py packages/python/mcp/tests/test_hosted_proxy.py packages/python/tests/test_mcp.py -q` | exit 0, 71 passed | `sdk-resume-calendar-permission-mcp.log` |
| `.tmp/python-venv/bin/python -m mypy packages/python/mcp` | exit 0, 34 source files | `sdk-resume-mcp-mypy.log` |
| `OPENAPI_INPUT_DIR=<task-docs> AGENT_TASK=rebrand-qubrics-904 heavy-slot.sh pnpm drift:check` | exit 0, every normal generator and staleness check | `sdk-resume-drift-check.log` |

Here `<task-docs>` is `/Users/rj/Desktop/GIT-REPOS/sendmux-docs-rebrand-qubrics-904`; `heavy-slot.sh` is `/Users/rj/Desktop/GIT-REPOS/ja-k8s/AA-AI/heavy-slot.sh`. Generated paths were staged before the standard drift proof, as required by the unchanged staleness checker. Handwritten source and this evidence remain for root review/staging. No commit or hook bypass.

Calendar candidate preservation: before/after status SHA256 `6ccf664a24c10d9b85f18f73e95f612f9cfa203f36705deb4458588d86a3cfb2`; binary diff `ed94f857a8fa1549a6f88bd084e98c4b74cf80131bee734cc5e5c47ea60e20bd`; untracked content manifest `c6b3b12657fdbeb813cddfda3a8dde95dea94486f8976acf788887d7ef906092`. Each before/after comparison exited 0. Receipts: `sdk-calendar-{before,after}-status.txt`, `sdk-calendar-{before,after}.patch`, `sdk-calendar-{before,after}-untracked-sha256.txt`. Source-only comparisons also passed: `sdk-resume-source-preservation.log`.

Source freeze: 1,105 tracked/staged paths differ from HEAD, with 124,868 insertions and 41,707 deletions; full status contains 1,121 changed/untracked paths, captured in `sdk-resume-final-status.txt`. Staged and unstaged whitespace checks pass. No root/package README change. No source dependency remains. Root owns review, final commit, push, PR and CI; full build/required CI and publication remain unqualified. Docs#78 retains its MCP pin/snippet until a compatible publication is verified. No full build or unchanged focused green was rerun here.

Root's final reviews of the complete handwritten diff and calendar integration returned Standards 0 hard violations / 0 actionable heuristics, and Spec 0 findings. Root also verified the drift tail and staged/unstaged whitespace checks. The worker's source claims were released after evidence finalisation; root owns the normal commit hook.

## Cleanup

Owned disposable fixtures are stopped. Command guard rejected the prior cache teardown; no deletion workaround attempted. SDK build/test caches remain listed in `sdk-final-handoff.md` for manual removal. Calendar checkout, venv and dist remain untouched.
