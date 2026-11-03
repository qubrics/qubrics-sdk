# Current-contract generation prerequisite for #897

Source-only prerequisite. API PR qubrics/qubrics#917 at `6039ee7a` names the existing webhook union variants; companion snapshot PR qubrics/docs#80 at `b0bb1e79` emits the explicit discriminator mapping. SDK generators and CI current-input binding remain unchanged.

## Cause and minimal fix

API `src/app/api/v1/_lib/schemas/webhooks.ts:125-135` used unnamed union options. `zod-to-openapi` 7.3.4 omits the mapping unless every option has a component name. The SDK preserves the metadata, but pinned ogen 1.14.0 cannot infer these variants from identical fields and inline enums (`gen/schema_gen_sum.go:334-521`). Naming the existing closed variants at the API source fixes normal Go generation without changing wire validation.

The next full-chain gate exposed ten released Calendar operations missing MCP curation and Rust decisions on SDK main. Reused the approved nine-operation handoff in `calendar-api/.claude/artifacts/calendar-api/sdk-tracer-implementation.md`, then added PR916 empty-calendar DELETE with the same `calendar.write`, destructive/idempotent and Rust raw-JSON policy. Static `/calendar-events/changes` precedes templated event routes, as required by the OpenAPI Paths Object. No Calendar or #904 checkout was edited.

Generated files cover the current contract, including Calendar and webhook types. Four CI checkout URL replacements use canonical `qubrics/docs`; branch selection and input binding are unchanged. No generator, dependency or lockfile changes.

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
