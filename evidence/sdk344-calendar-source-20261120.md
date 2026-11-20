# Calendar-free SDK source

Goal: remove remaining calendar bindings from SDK source under the operator's 20 November rule 12. Published versions stay unchanged. No upload, tag, registry, release queue or environment action is authorised here.

## Preservation and scope

- `archive/calendar` preserves SDK main `086e6c40d2d0fb349d06811120aca504555ab6c6` before source removal.
- Reuse `withhold-mcp-calendar.mjs` and `withhold-management-calendar.mjs` on TypeScript, Go and PHP generator inputs. Raw OpenAPI producer snapshots remain unchanged while the App/gateway runtime awaits its infrastructure gate.
- Generated CLI omits the same ten calendar operations and the calendar event enum value. Coverage reports distinguish withheld bindings from missing implementations. Retired calendar fixture creation/cleanup code and discovery records are removed.
- Existing subscription/delivery labels stay strings. Retained webhook delivery payloads stay opaque maps, preserving unknown nested values. Mail webhook variants remain available.
- Relative to integrated main `29ebc94f`, Python, Ruby, Rust and MCP source, package versions, release metadata and workflows have no calendar-removal diff. The branch normally incorporates the already-merged Ruby SDK release source from that main commit. Separate PHP repositories follow the forthcoming immutable canonical output. No announcement copy is added.

## Origin and regression evidence

Raw command logs live in MAIN `.claude/artifacts/rebrand-qubrics-sdk344/`.

| Signal | Red evidence | Green evidence |
| --- | --- | --- |
| CLI calendar operations absent, mailbox read retained | `calendar-cli-red.log`: actual includes `mailboxGetCalendarEventChanges` and `mailboxListCalendars`, expected only `mailboxListMessages` | `calendar-cli-green.log`: both generator tests pass |
| CLI calendar enum value absent, mail value retained | `calendar-cli-enum-red.log`: actual contains `calendar.changed`, expected `message.received` only | `calendar-cli-enum-green.log`: 2 tests pass, zero skipped |
| Go retained labels and opaque nested delivery payload round-trip | `calendar-go-history-red.log`: `[]string` incompatible with old `[]WebhookSubscriptionEventTypesItem` | `calendar-go-history-green.log`: focused Management test passes |
| Go public mail models and all eight mail discriminators remain usable | `calendar-go-mail-models-red.log`: existing public mail types undefined | `calendar-go-mail-models-green.log`: mail round-trip and opaque retained-history tests pass |
| PHP opaque retained history and withheld new-event label | `calendar-php-history-red.log`: calendar event remains allowable and typed payload loses unknown fields | `calendar-php-history-discriminator-green.log`: 13 tests, 79 assertions pass |
| Every SDK adapter treats calendar planning/dispatch as inapplicable | `calendar-adapter-red.log` | `calendar-plan-withheld-green.log`: all 5 adapters pass, zero skipped |

PHP's first regeneration exposed a vendor normalisation consequence: after removing the calendar member, the remaining `WebhookEventPayload.oneOf` has one member. OpenAPI Generator defaults `SIMPLIFY_ONEOF_ANYOF=true`, replacing that union with its child and dropping the base discriminator. The existing eight mail-discriminator assertions caught it. Management alone now uses the official `SIMPLIFY_ONEOF_ANYOF=false` option. The filtered Management schema has exactly one top-level singleton `oneOf`/`anyOf`, `WebhookEventPayload`; generated changes remain limited to calendar removal and opaque delivery history.

Canonical option: [OpenAPI Generator v7.22.0 normaliser documentation](https://github.com/OpenAPITools/openapi-generator/blob/v7.22.0/docs/customization.md#openapi-normalizer), `SIMPLIFY_ONEOF_ANYOF` description. No generated file is patched by hand.

PHP's new history test compares full JSON values across deserialisation and serialisation. The vendor maps an OpenAPI free-form object to `array<string,mixed>`, retaining nested mixed values. `JSON_THROW_ON_ERROR` makes encoding failures explicit and satisfies the native static checker. Existing mail subtype assertions remain unchanged; their fixture now deserialises the named event directly because retained delivery bodies intentionally have no typed discriminator.

Independent Spec and Standards reviews of `27c2cd1b` found one shared blocker: ogen generates operation-reachable models only. Preserving the `WebhookEventPayload` component as a pruning root did not preserve the public Go mail models after delivery payloads became opaque. The generator now runs the vendor's [standalone JSON Schema generator](https://github.com/ogen-go/ogen/blob/v1.14.0/cmd/jschemagen/main.go) on that retained root after normal Management generation. It reuses the three already-generated wrappers `NilBool`, `NilString` and `OptNilString`. No synthetic operation or changed delivery shape is introduced. A native public consumer test first failed on missing mail types, then round-tripped all eight mail discriminators after the origin correction. `calendar-go-mail-models-generate.log` records generation.

## Focused qualification

- TypeScript mailbox operation count: 63 to 53, exactly the ten calendar operations removed. Management 57 and Sending 8 unchanged. `calendar-ts-operation-proof.log`.
- CLI operation count: 128 to 118, same ten removed and zero added. `calendar-cli-operation-proof.log`.
- TypeScript source build/public API and CLI build pass: `calendar-ts-build.log`, `calendar-ts-public-api.log`, `calendar-cli-build.log`.
- PHP changed-test PHPCS and PHPStan pass: `calendar-php-tests-lint.log`, `calendar-php-tests-types.log`. Native consumer assertions pass as above. Recursive singleton audit finds only `WebhookEventPayload.oneOf`: `calendar-php-singleton-unions.log`.
- Surface and live coverage pass: `calendar-surface-coverage-green.log`, `calendar-plan-final-green.log`.
- Runtime text/filename scan finds no calendar bindings in generated TypeScript Mailbox/Management/CLI, Go Mailbox/Management or PHP Mailbox/Management. Negative tests and raw contract/provenance history are intentionally retained.
- `git diff --check` passes. No production request or fixture mutation is used for this source check.

Tests: add CLI input/output regression, Go history round-trip, PHP history/allowable-event checks and five adapter inapplicability cases. Remove calendar lifecycle tests with their retired calendar fixture implementation under rule 12. Other fixture ownership and cleanup assertions remain.

Status: coded, not merged. First exact default Skills v2.0.8 check of `27c2cd1b` passed live OpenAPI equality but failed because its new CLI command digest has no reviewed compatibility record. `calendar-source-default-27c2cd1b.log` records the failure. Skills owner must settle that evidence at origin before a new released checker/default recheck. No retry, pin, fallback or workflow change. Exact-head CI and merge disposition follow normal PR gates. Package publication remains separately held.

Rollback: normal revert of the source PR. Preserved source remains on `archive/calendar`.

## Post-review PHP metadata correction

Standards review found an unintended public consumer regression in the four surviving historical Management models. `WebhookSubscription::EVENT_TYPES_MESSAGE_RECEIVED` raised `Error: Undefined constant` (PHP exit 255). The generic calendar filter removed historical-field enums to keep arbitrary stored labels readable. The pinned vendor template uses the same `isEnum` metadata to generate both constants/allowable-value methods and closed validation, so enum deletion also removed mail metadata symbols. All four fields share this origin; adjacent new-subscription request models must remain closed.

Canonical per the pinned [OpenAPI Generator 7.22.0 templating guide](https://github.com/OpenAPITools/openapi-generator/blob/v7.22.0/docs/templating.md): customise the existing Mustache template and its vendor-extension data. The pinned [PHP model template](https://github.com/OpenAPITools/openapi-generator/blob/v7.22.0/modules/openapi-generator/src/main/resources/php-nextgen/model_generic.mustache) gates public enum metadata and validation together. `scripts/generate-php.mjs` now preserves the original non-calendar enum metadata for only `WebhookSubscription`, `WebhookSubscriptionWithSecret`, `WebhookDeliveryAttempt` and `WebhookDeliveryPayload`, marking their properties `x-sendmux-open-label`. Four guards in the existing local model template omit closed setter/property validation for those marked historical fields. There is no unknown-label fallback, generated hand patch, dependency change or new template copy.

- Exact native public-consumer red: `calendar-php-mail-metadata-consumer-red.log`, exit 255. The existing `WebhookEventPayloadTest` seam reproduced missing metadata before the correction (`calendar-php-mail-metadata-native-red.log`).
- Green: `calendar-php-mail-metadata-consumer-green.log` prints `message.received`, exit 0. `calendar-php-mail-metadata-native-green.log`: 15 tests, 109 assertions, zero skipped; includes all eight mail discriminators, opaque nested history, all four metadata methods, exact arbitrary historical strings and rejection of a new calendar subscription.
- `calendar-php-mail-metadata-symbol-parity.json`: all 206 pre-existing non-calendar public symbols remain (47/49/67/43 per model); only the four named calendar constants disappear. The nine existing mail/unknown-default metadata values remain; `calendar.changed` is absent from them.
- `calendar-php-correction-unrelated-output-diff-stat.log` is empty: Mailbox/Sending output and new-subscription create/update models are unchanged by this correction. `calendar-php-go-runtime-scan-final.log` is empty: no calendar runtime binding remains in generated PHP/Go Mailbox/Management source.
- Focused PHPCS and max-level PHPStan pass in `calendar-php-mail-metadata-lint.log` and `calendar-php-mail-metadata-static.log`. Two line-length warnings in the new test were corrected by wrapping only those assertions.

## Post-review Go opaque-value correction

CodeRabbit finding `4637031067` is confirmed. A nil or empty raw JSON value in the new opaque webhook map produced malformed JSON; an existing `BalanceResponseMetaAdditional` map reproduced the same failure. The pinned [ogen 1.14.0 map template](https://github.com/ogen-go/ogen/blob/v1.14.0/gen/_template/json/encoders_map.tmpl#L14) and [struct template](https://github.com/ogen-go/ogen/blob/v1.14.0/gen/_template/json/encoders_struct.tmpl#L16) write `FieldStart(k)` before the shared [raw-value nonempty guard](https://github.com/ogen-go/ogen/blob/v1.14.0/gen/_template/json/encode.tmpl#L106). An empty value therefore writes a name/colon without a JSON value. Both observed parser errors (`invalid character '}' looking for beginning of value` and `invalid character ':' after object key:value pair`) follow from map iteration order around that dangling field.

The existing checked generator postprocessing seam now moves the key write inside that same guard for the exact traced pattern. Empty raw values remain omitted under the vendor's existing policy; nonempty raw bytes and all public symbols remain unchanged. No codec generalisation, schema change, pin/fork or generated hand patch is used.

- `calendar-go-empty-raw-both-red.log`: new opaque map and existing metadata map both fail for nil and empty raw values before the origin correction. The regression extends the existing native `webhook_history_test.go` seam, with JSON null/nonempty nested data as the adjacent boundary.
- `calendar-go-empty-raw-green.log`: focused Management native tests pass, including both maps, nil/empty omission, unchanged JSON null/nested data, historical payload round-trip and all eight mail discriminators.
- Exactly 162 occurrences share this template defect: 78 Mailbox, 83 Management and 1 Sending. [The tracked inventory](sdk344-go-empty-raw-map-types-20261120.json) lists every affected receiver/method and file.
- `calendar-go-empty-raw-exact-delta.json` proves each of the three generated JSON files equals the prior file with only that exact replacement applied, with zero old-pattern occurrences left. `calendar-go-empty-raw-symbol-parity.json` proves no function signature removed or added.

The previous immutable `4416e3ce` remains reachable. Main `29ebc94f` was integrated normally before these corrections. Coverage and shared-test-helper origin corrections, all red/green receipts and the local Ruby setup limit are recorded in [the coverage evidence](sdk344-calendar-coverage-origin-20261120.md).

Independent Spec and Standards reviews of the complete correction batch each found zero issues. The reviewed source-only diff SHA-256 is `c5a242bdd0e3c6e7500a2797562b8dc18230a0425f37450ad82d86854630d1b9`, excluding appendable evidence, verified unchanged after both reviews. Focused safety checks pass 9/9 and surface checks pass 3/3, with zero skipped in those commands. The complete multi-language suite remains a normal CI gate; Ruby 3.4.12 is unavailable locally and no runtime fallback or pin change was made.

`git diff --quiet 4416e3ce -- packages/ts/cli` exits 0: the correction leaves the CLI path byte-identical to the already-inspected candidate. Published `sendmux-cli` contract digest remains `46af45d935f17006bec9b7cd4745eeabdf192aa7e008357ba924cedc8ae93d51`; proposed `qubrics-cli` remains `173d494f78667ca69a49f233e5fcbdb79a178f9df274ec537b67a9af52a878b3`. The official inspection is MAIN `calendar-source-go-final-inspection.json`; this identity comparison is not an acceptance retry.

Normal drift-hook commit, exact-head CI and fresh default acceptance after the Skills origin input changes remain pending. Source publication/tag/queue/environment holds remain unchanged.
