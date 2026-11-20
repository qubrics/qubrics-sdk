# Calendar-free SDK source

Goal: remove remaining calendar bindings from SDK source under the operator's 20 November rule 12. Published versions stay unchanged. No upload, tag, registry, release queue or environment action is authorised here.

## Preservation and scope

- `archive/calendar` preserves SDK main `086e6c40d2d0fb349d06811120aca504555ab6c6` before source removal.
- Reuse `withhold-mcp-calendar.mjs` and `withhold-management-calendar.mjs` on TypeScript, Go and PHP generator inputs. Raw OpenAPI producer snapshots remain unchanged while the App/gateway runtime awaits its infrastructure gate.
- Generated CLI omits the same ten calendar operations and the calendar event enum value. Coverage reports distinguish withheld bindings from missing implementations. Retired calendar fixture creation/cleanup code and discovery records are removed.
- Existing subscription/delivery labels stay strings. Retained webhook delivery payloads stay opaque maps, preserving unknown nested values. Mail webhook variants remain available.
- Python, Ruby, Rust, MCP source, package versions, release metadata and workflows have no diff. Separate PHP repositories follow this immutable canonical output. No announcement copy is added.

## Origin and regression evidence

Raw command logs live in MAIN `.claude/artifacts/rebrand-qubrics-sdk344/`.

| Signal | Red evidence | Green evidence |
| --- | --- | --- |
| CLI calendar operations absent, mailbox read retained | `calendar-cli-red.log`: actual includes `mailboxGetCalendarEventChanges` and `mailboxListCalendars`, expected only `mailboxListMessages` | `calendar-cli-green.log`: both generator tests pass |
| CLI calendar enum value absent, mail value retained | `calendar-cli-enum-red.log`: actual contains `calendar.changed`, expected `message.received` only | `calendar-cli-enum-green.log`: 2 tests pass, zero skipped |
| Go retained labels and opaque nested delivery payload round-trip | `calendar-go-history-red.log`: `[]string` incompatible with old `[]WebhookSubscriptionEventTypesItem` | `calendar-go-history-green.log`: focused Management test passes |
| PHP opaque retained history and withheld new-event label | `calendar-php-history-red.log`: calendar event remains allowable and typed payload loses unknown fields | `calendar-php-history-discriminator-green.log`: 13 tests, 79 assertions pass |
| Every SDK adapter treats calendar planning/dispatch as inapplicable | `calendar-adapter-red.log` | `calendar-plan-withheld-green.log`: all 5 adapters pass, zero skipped |

PHP's first regeneration exposed a vendor normalisation consequence: after removing the calendar member, the remaining `WebhookEventPayload.oneOf` has one member. OpenAPI Generator defaults `SIMPLIFY_ONEOF_ANYOF=true`, replacing that union with its child and dropping the base discriminator. The existing eight mail-discriminator assertions caught it. Management alone now uses the official `SIMPLIFY_ONEOF_ANYOF=false` option. The filtered Management schema has exactly one top-level singleton `oneOf`/`anyOf`, `WebhookEventPayload`; generated changes remain limited to calendar removal and opaque delivery history.

Canonical option: [OpenAPI Generator v7.22.0 normaliser documentation](https://github.com/OpenAPITools/openapi-generator/blob/v7.22.0/docs/customization.md#openapi-normalizer), `SIMPLIFY_ONEOF_ANYOF` description. No generated file is patched by hand.

PHP's new history test compares full JSON values across deserialisation and serialisation. The vendor maps an OpenAPI free-form object to `array<string,mixed>`, retaining nested mixed values. `JSON_THROW_ON_ERROR` makes encoding failures explicit and satisfies the native static checker. Existing mail subtype assertions remain unchanged; their fixture now deserialises the named event directly because retained delivery bodies intentionally have no typed discriminator.

## Focused qualification

- TypeScript mailbox operation count: 63 to 53, exactly the ten calendar operations removed. Management 57 and Sending 8 unchanged. `calendar-ts-operation-proof.log`.
- CLI operation count: 128 to 118, same ten removed and zero added. `calendar-cli-operation-proof.log`.
- TypeScript source build/public API and CLI build pass: `calendar-ts-build.log`, `calendar-ts-public-api.log`, `calendar-cli-build.log`.
- PHP changed-test PHPCS and PHPStan pass: `calendar-php-tests-lint.log`, `calendar-php-tests-types.log`. Native consumer assertions pass as above.
- Surface and live coverage pass: `calendar-surface-coverage-green.log`, `calendar-plan-final-green.log`.
- Runtime text/filename scan finds no calendar bindings in generated TypeScript Mailbox/Management/CLI, Go Mailbox/Management or PHP Mailbox/Management. Negative tests and raw contract/provenance history are intentionally retained.
- `git diff --check` passes. No production request or fixture mutation is used for this source check.

Tests: add CLI input/output regression, Go history round-trip, PHP history/allowable-event checks and five adapter inapplicability cases. Remove calendar lifecycle tests with their retired calendar fixture implementation under rule 12. Other fixture ownership and cleanup assertions remain.

Status: coded, not merged. Exact-head CI, default Skills acceptance, independent review and merge disposition follow the normal PR gates. Package publication remains separately held.

Rollback: normal revert of the source PR. Preserved source remains on `archive/calendar`.
