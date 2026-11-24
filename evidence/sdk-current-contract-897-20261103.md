# Current-contract generation prerequisite for #897

Source-only prerequisite. API PR qubrics/qubrics#917 at `6a7378de` names the existing webhook union variants; companion snapshot PR qubrics/docs#80 at `6dd1c642` emits that metadata. Pinned generators and CI current-input binding remain unchanged; the PHP template and its existing serializer correction path are fixed at their origin below.

## Cause and minimal fix

API `src/app/api/v1/_lib/schemas/webhooks.ts:125-135` used unnamed union options. `zod-to-openapi` 7.3.4 omits the mapping unless every option has a component name. The SDK preserves the metadata, but pinned ogen 1.14.0 cannot infer these variants from identical fields and inline enums (`gen/schema_gen_sum.go:334-521`). Naming the existing closed variants at the API source fixes normal Go generation without changing wire validation.

Generated files cover the current contract, including webhook types. Four CI checkout URL replacements use canonical `qubrics/docs`; branch selection and input binding are unchanged. No dependency or lockfile changes.

## Verification

Logs: `/Users/rj/Desktop/GIT-REPOS/sendmux/.claude/artifacts/rebrand-qubrics-897/`.

- API contract regression red: exit 1, missing refs/discriminator; after the metadata fix, webhook and closed-object tests exit 0, 36 passed. `current-contract-{red,green}.log`.
- API fast/commit/push gates exit 0; app CI `41558089585` green at `6039ee7a`. Docs CI `41558050980` green at `b0bb1e79`; preview skipped, no deploy claimed.
- Normal Go generation exit 0 using corrected snapshot and unchanged pinned generator: `current-contract-go.log`.
- MCP discovery/quality test exit 0, 1 passed: `current-contract-mcp-quality.log`.
- Full normal `pnpm drift:check` reached all 128 operations and reported no generated drift: `current-contract-drift.log`. Commit hook independently runs the same chain against companion snapshot `b0bb1e79`.
- `git diff --cached --check`: exit 0. No tests removed, weakened or skipped.

No package publication, deployment. This proves generation and local contract behaviour; CI is required before delegated source merge. Original row4 rebrand changes remain separate, and rows2/5 stay held for cutover #902.

## CI origins corrected under Ops A approval

CI `41564375406` failed in five PHP jobs because the pinned php-nextgen template interpolated dotted discriminator values into PHP constant identifiers. The serializer also tried raw class names and inheritance instead of the explicit mapping, and nested delivery setters accepted only the former base class. Reuse normal enumVars, dispatch the declared mapping and derive the containing property's union type in the existing generator/template. Unknown discriminator fallback and Sending attachment handling are preserved. Canonical references: OpenAPI 3.1.1 Discriminator Object and OpenAPI Generator v7.22.0 `php/model_generic.mustache` enumVars plus `DefaultCodegen.java` resolved-schema extensions. No canonical contract rewrite or generated-file hand edit.

Real ObjectSerializer tests first failed on invalid constants, then wrong subtype, then nested setter TypeError. Final direct/nested webhook data plus unchanged attachment regression: 13 tests, 73 assertions, exit 0. Final normal generation and staged staleness check: exit 0 against docs `6dd1c642`. Logs: `php-discriminator-{red,mapping-red,nested-red,green}.log`.

Independent final Standards and Spec review: zero findings. README package/install/auth claims stay accurate: this prerequisite changes generated responses and runtime coverage, with no package rename/version or install change. Temporary loopback servers/directories were verified gone; final cache cleanup follows the commit hook. Exact-head CI remains required. Further discoveries stay outside this approved slice.
