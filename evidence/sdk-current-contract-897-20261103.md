# Current-contract generation prerequisite for #897

Source-only prerequisite. API PR qubrics/qubrics#917 at `6a7378de` names the existing webhook union variants and adds GET-only Calendar JSON `etag`; companion snapshot PR qubrics/docs#80 at `6dd1c642` emits both. Pinned generators and CI current-input binding remain unchanged; the PHP template and its existing serializer correction path are fixed at their origin below.

## Cause and minimal fix

API `src/app/api/v1/_lib/schemas/webhooks.ts:125-135` used unnamed union options. `zod-to-openapi` 7.3.4 omits the mapping unless every option has a component name. The SDK preserves the metadata, but pinned ogen 1.14.0 cannot infer these variants from identical fields and inline enums (`gen/schema_gen_sum.go:334-521`). Naming the existing closed variants at the API source fixes normal Go generation without changing wire validation.

The next full-chain gate exposed ten released Calendar operations missing MCP curation and Rust decisions on SDK main. Reused the approved nine-operation handoff in `calendar-api/.claude/artifacts/calendar-api/sdk-tracer-implementation.md`, then added PR916 empty-calendar DELETE with the same `calendar.write`, destructive/idempotent and Rust raw-JSON policy. Static `/calendar-events/changes` precedes templated event routes, as required by the OpenAPI Paths Object. No Calendar or #904 checkout was edited.

Generated files cover the current contract, including Calendar and webhook types. Four CI checkout URL replacements use canonical `qubrics/docs`; branch selection and input binding are unchanged. No dependency or lockfile changes.

## Verification

Logs: `/Users/rj/Desktop/GIT-REPOS/sendmux/.claude/artifacts/rebrand-qubrics-897/`.

- API contract regression red: exit 1, missing refs/discriminator; after the metadata fix, webhook and closed-object tests exit 0, 36 passed. `current-contract-{red,green}.log`.
- API fast/commit/push gates exit 0; app CI `41558089585` green at `6039ee7a`. Docs CI `41558050980` green at `b0bb1e79`; preview skipped, no deploy claimed.
- Normal Go generation exit 0 using corrected snapshot and unchanged pinned generator: `current-contract-go.log`.
- DELETE scope and hosted-route tests red: exit 1, `ValueError: unknown MCP tool: mailbox_delete_calendar` and unresolved DELETE route. Green: exit 0, 27 passed; `current-contract-delete-{red,green}.log`.
- MCP discovery/quality test exit 0, 1 passed: `current-contract-mcp-quality.log`.
- Full normal `pnpm drift:check` reached all 128 operations and reported no generated drift: `current-contract-drift.log`. Commit hook independently runs the same chain against companion snapshot `b0bb1e79`.
- `git diff --cached --check`: exit 0. No tests removed, weakened or skipped.
- Public-copy critique checked all ten Calendar entries against the API schema and approved handoff. New DELETE description now states `calendar.write`; one humanize pass preserved permission names, ETag, If-Match, UID, 409 conflict and uncertainty qualifiers. No other curation copy changed.

No package publication, deployment or live Calendar calls. This proves generation and local contract behaviour; CI is required before delegated source merge. Original row4 rebrand changes remain separate, and rows2/5 stay held for cutover #902.

## CI origins corrected under Ops A approval

CI `41564375406` failed in five PHP jobs because the pinned php-nextgen template interpolated dotted discriminator values into PHP constant identifiers. The serializer also tried raw class names and inheritance instead of the explicit mapping, and nested delivery setters accepted only the former base class. Reuse normal enumVars, dispatch the declared mapping and derive the containing property's union type in the existing generator/template. Unknown discriminator fallback and Sending attachment handling are preserved. Canonical references: OpenAPI 3.1.1 Discriminator Object and OpenAPI Generator v7.22.0 `php/model_generic.mustache` enumVars plus `DefaultCodegen.java` resolved-schema extensions. No canonical contract rewrite or generated-file hand edit.

Real ObjectSerializer tests first failed on invalid constants, then wrong subtype, then nested setter TypeError. Final direct/nested mail and calendar data plus unchanged attachment regression: 13 tests, 73 assertions, exit 0. Final normal generation and staged staleness check: exit 0 against docs `6dd1c642`. Logs: `php-discriminator-{red,mapping-red,nested-red,green}.log`, `calendar-etag-{generation,php-final}.log`.

The same CI run's inventory failure exposed five missing Calendar lifecycle factories. The existing runner now persists owned Calendar names and event UIDs before dispatch, observes returned IDs, refuses uncertain-create replay, obtains fresh JSON ETags and cleans child events before empty parents with absence readback. Run-owned paths must contain an ID; unresolved creation leaves cleanup failed. Creates omit Idempotency-Key because Calendar has no such contract and the SDK would otherwise automatically replay POST. Five real Calendar operations run through the existing public SDK/loopback seam; no new harness.

Calendar tests were red at the missing create factory, replay guard and absent-ID ownership guard, then green: 4 selected cases, exit 0, no skips. Intentional inventory assertions now require 130 total, 65 executable, 65 gated, zero blocked; static emitter exit 0. Full local native safety is not green: its Python adapter package is uninstalled in the transient environment; normal CI prepares it through the existing language check. No assertion was relaxed to avoid this prerequisite. Logs: `calendar-lifecycle-{red,uncertain-red,owned-path-red,focused-green,static-emitter,inventory-green}.log`.

Independent final Standards and Spec review: zero findings. README package/install/auth claims stay accurate: this prerequisite changes generated responses and runtime coverage, with no package rename/version or install change. Temporary loopback servers/directories were verified gone; final cache cleanup follows the commit hook. Exact-head CI remains required. Further discoveries stay outside this approved slice.
