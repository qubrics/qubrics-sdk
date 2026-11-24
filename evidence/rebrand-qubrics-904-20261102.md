# A17 SDK integration contract aliases

Status: initial source committed at `722fbab2f98248d17b4878dd5149a35a711d5a18`; required CI exposed the bounded follow-up recorded below. Not merged, deployed or published. Base: `0dd32a2652f3fd7a9a8f7e2ab8976d79f1b1dc99`. Ticket: qubrics/qubrics#904, acceptance A17. SDK root/package README changes remain owned by #897.

## Source and behaviour

Qubrics environment names take precedence, with retained Sendmux fallbacks. MCP tools expose additive aliases while preserving original handlers. Generated native clients use the existing environment/URL configuration and preserve delegated-upload authentication independently of ordinary bearer credentials. Generators, rather than generated clients alone, own each correction.

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

This section records the prior freeze. All three source dependencies below were resolved; final proof follows.

The pre-commit hook `.githooks/pre-commit:4` unconditionally invokes `pnpm drift:check`, which runs MCP generation and writes frozen `packages/python/mcp/sendmux_mcp/openapi/openapi-app.json`. No hook invocation, bypass, commit or push was attempted while that lease stands.

Frozen paths retain their original SHA256 values:

- `permissions.py`: `aa27f177b17871d954327a8a6d063dfb5b1f87d1a77d661893739137a1d5e2ca`.
- `curation.py`: `ba8e91c99cf203654e25a766db3bb02d1fa2bfa5768ad6a3edb69df03ad9774f`.
- embedded `openapi-app.json`: `dd39d2329fc51098455f499e551ad3e33f14bc9243c793dfa47fc353a57f62ea`.

Full drift/build/required CI remain unqualified until the lease releases and source can commit/push normally. Docs#78 keeps its existing MCP pin and release-facts snippet until a compatible publication is verified. No version is invented and no publication is authorised.

## Source finalisation

- `packages/python/mcp/tests/test_permissions.py` and `test_hosted_proxy.py`: unchanged owner permission-isolation and canonical-route cases.
- `rust/operation-decisions.json`: all nine owner decisions remain `raw-json-only`, with no named method or live certification inferred.

`permissions_for_tool` at permissions.py:109 and the surface lookup at :142 strip exactly one leading `qubrics_`. Both lookups use the same original registries. Unknown/nested aliases still fail; all permission and surface claim checks remain. The earlier authenticated positive red cases now pass alongside denied-token cases. No permission widening or bypass.

Normal MCP generation replaced the released embedded app snapshot with canonical app SHA256 `16439b3c0d9eee73554202cf909af6aade12b6f8d3390ddee922663ba061de1a`; sending remains `3138c5f27e3c0ab8475d1ccaf7378815c12e12918c30a90e77e2115642bc3647`. Guarded generation updated the surface matrix and Rust provenance from these same inputs. Existing environment and delegated-upload source corrections were preserved. The six prior Ruby source/runtime fingerprints still match.

| Command | Result | Parent artifact receipt |
| --- | --- | --- |
| `.tmp/python-venv/bin/python -m pytest packages/python/mcp/tests/test_contract_aliases.py -k authenticated_http -q` | exit 0, 4 passed / 6 deselected | `sdk-mcp-auth-alias-resume-green.log` |
| `OPENAPI_INPUT_DIR=<task-docs> AGENT_TASK=rebrand-qubrics-904 heavy-slot.sh pnpm generate:mcp` | exit 0 | `sdk-resume-generate-mcp.log` |
| `OPENAPI_INPUT_DIR=<task-docs> node scripts/check-surface-coverage.mjs --write --write-provenance` | exit 0, 127 operations | `sdk-resume-coverage-provenance.log` |
| `.tmp/python-venv/bin/python -m mypy packages/python/mcp` | exit 0, 34 source files | `sdk-resume-mcp-mypy.log` |
| `OPENAPI_INPUT_DIR=<task-docs> AGENT_TASK=rebrand-qubrics-904 heavy-slot.sh pnpm drift:check` | exit 0, every normal generator and staleness check | `sdk-resume-drift-check.log` |

Here `<task-docs>` is `/Users/rj/Desktop/GIT-REPOS/sendmux-docs-rebrand-qubrics-904`; `heavy-slot.sh` is `/Users/rj/Desktop/GIT-REPOS/ja-k8s/AA-AI/heavy-slot.sh`. Generated paths were staged before the standard drift proof, as required by the unchanged staleness checker. Handwritten source and this evidence remain for root review/staging. No commit or hook bypass.

Source freeze: 1,105 tracked/staged paths differ from HEAD, with 124,868 insertions and 41,707 deletions; full status contains 1,121 changed/untracked paths, captured in `sdk-resume-final-status.txt`. Staged and unstaged whitespace checks pass. No root/package README change. No source dependency remains. Root owns review, final commit, push, PR and CI; full build/required CI and publication remain unqualified. Docs#78 retains its MCP pin/snippet until a compatible publication is verified. No full build or unchanged focused green was rerun here.

Root's final reviews of the complete handwritten diff returned Standards 0 hard violations / 0 actionable heuristics, and Spec 0 findings. Root also verified the drift tail and staged/unstaged whitespace checks. The worker's source claims were released after evidence finalisation; root owns the normal commit hook.

## Required CI follow-up on PR #345

Candidate reopened for CI blockers. Exact reviewed head `722fbab2f98248d17b4878dd5149a35a711d5a18` finished with 44 checks: 28 success, 14 failure, 2 skipped, none pending. All 14 failures were in [CI run 41458872537](https://github.com/qubrics/qubrics-sdk/actions/runs/41458872537). The complete `gh run view 41458872537 --repo qubrics/qubrics-sdk --log-failed` receipt is `sdk-pr345-ci-failed.log`; `sdk-pr345-failed-job-sweep.log` accounts for every failed job.

| Failed jobs | Confirmed cause and source correction |
| --- | --- |
| Verify, Python language verification, Python 3.10–3.14 (7 jobs) | Shared-test mypy rejected dynamic upload-token keyword dictionaries at test_oauth_retry.py:115 and a general string registry key at test_mcp.py:242. Explicit twin parameters and a `dict[Surface, set[str]]` preserve every assertion and runtime case. |
| PHP language verification, PHP 8.2–8.5 (5 jobs) | Discriminator mapping snakecase generated slash-containing PHP identifiers at WebhookEventPayload.php:237. Template-only discriminator branches were removed; the existing `allowableValues.enumVars` path supplies valid identifiers and exact dotted wire literals. Normal PHP generation changed only this model. |
| Ruby language verification (1 job) | The existing source guard still required a positional legacy upload token. It now checks the intentional required-length/body signature plus both optional token headers; length and existing provider no-read assertions remain. |
| MCP language verification (1 job) | Hosted discovery expected originals only at test_hosted_server.py:457. Expected names now include aliases, and mailbox-target checks run on both original and aliased names. |

Canonical PHP evidence: [official generator 7.22.0 `AbstractPhpCodegen.toEnumVarName`](https://github.com/OpenAPITools/openapi-generator/blob/v7.22.0/modules/openapi-generator/src/main/java/org/openapitools/codegen/languages/AbstractPhpCodegen.java#L854) sanitises identifiers after underscore/uppercase conversion. The real generator `debugModels` probe confirms its existing enum variables include every nine mapped wire values and the configured unknown fallback. Receipts: `sdk-php-official-abstract-codegen.java`, `sdk-php-discriminator-debug-models.log`. No invented lambda, modified mapping key or generated-only patch.

New public regression `ManagementValidationTest::testWebhookDiscriminatorPreservesEveryWireValue` loads the generated model, checks all nine dotted event values survive its public setter/getter, and checks the existing unknown fallback. Red: `ParseError: syntax error, unexpected token "/"` at generated model line 237, exit 2. Green: the whole focused class passes 3 tests / 24 assertions, exit 0. Receipts: `sdk-pr345-php-discriminator-{red,green}.log`. No tests removed or assertions weakened.

Other focused receipts, all exit 0: canonical-input `pnpm generate:php` under heavy-slot (`sdk-pr345-generate-php.log`); mypy on the three changed Python test files, 3 files (`sdk-pr345-python-typing-green.log`); delegated-upload twins, curated discovery and hosted mailbox-target cases, 4 passed (`sdk-pr345-python-focused-green.log`). Ruby runtime source and its earlier public-provider green receipt are unchanged; fresh full CI remains required.

Normal commit gate is the unchanged `.githooks/pre-commit`, which runs `pnpm drift:check` with the same canonical `OPENAPI_INPUT_DIR` under heavy-slot. `sdk-pr345-final-commit.log` records its terminal result. No separate unchanged full drift, local full suite or CI rerun was used. Final two-axis review results are retained in `sdk-pr345-ci-diagnosis.md`. No product/docs push, merge, deploy or publication is authorised for this follow-up worker.

Fresh independent follow-up reviews: Standards 0 findings; Spec 0 findings across the seven source/test/generated files. No source change followed those reviews. The shared active-agent cap required sequential dispatch; both contexts were fresh.

## Downstream CI blockers at ff4bb860

Exact head `ff4bb8601de885703e2cbff4af6a62f1b15d5791` finished with 44 checks: 29 success, 13 failure, 2 skipped, none pending. All 13 failed jobs belong to [CI run 41462820059](https://github.com/qubrics/qubrics-sdk/actions/runs/41462820059); complete failed logs and the per-job accounting are `sdk-pr345-ff4-ci-failed.log` and `sdk-pr345-ff4-failed-job-sweep.log`. The prior PHP parse, Python typing and MCP alias-discovery failure points passed. Three newly reached causes explain every remaining failure:

- PHP five jobs: the new public discriminator test violated PSR12 multiline-control formatting at `ManagementValidationTest.php:16,26`. Formatting alone changed; all nine wire values and the unknown fallback remain asserted.
- Ruby one job: `scripts/check-ruby.mjs:55-95` enforces existing manifest floors when the SDK package changes. Its unchanged gemspec still admitted Mailbox 2.0.0 and Management 2.0.0, below current manifest 2.0.2 and 2.0.1. Only those two lower bounds and their normal `bundle lock --local` entries changed; ceilings and the guard remain intact. The exact-base comparison also rejects the same stale metadata when the SDK is marked changed (`sdk-pr345-ff4-ruby-base-proof.log`).
- Python seven jobs: the intentionally independent LangChain source cohort installs candidate Sending and LangChain with published Core 1.3.1 (`scripts/ci-consumers.mjs:22-25`, `scripts/check-python.mjs:87-122`). Sending eagerly imported the new, unpublished `sendmux_core.environment`; its declared supported floor remains 1.3.1. `writeSurfaceClient` in `scripts/generate-python.mjs` now owns direct package-local environment lookups, and normal generation reproduces all three surface wrappers. MCP keeps the identical resolver in its existing config module; all four MCP importers stay within that distribution. Blank Qubrics values, retained legacy fallbacks and explicit-option precedence remain unchanged. No cohort, dependency floor, package version or release pin changed for Python.

Each downstream diagnosis had zero earlier fixes. The first Python check after this batch passed 179 native tests but correctly rejected stale MCP source hashes in one metadata case before reaching the isolated cohorts. Normal `pnpm generate:mcp` changed only the four source fingerprints for config, CLI, hosted and observability. Tool contracts and both embedded OpenAPI snapshots are unchanged. The failing metadata case then passed, followed by the canonical complete Python check.

| Command | Result | Parent artifact receipt |
| --- | --- | --- |
| Focused PHPCS with the repo ruleset | exit 0 | `sdk-pr345-second-php-phpcs-green.log` |
| `vendor/bin/phpunit --configuration phpunit.xml.dist --filter ManagementValidationTest` | exit 0, 3 tests / 24 assertions | `sdk-pr345-second-php-public-green.log` |
| Existing `checkRubyDependencyFloors` with changed SDK | exit 0, existing manifest floors accepted | `sdk-pr345-second-ruby-floor-green.log` |
| Ruby public environment test | exit 0, 1 run / 18 assertions / 0 skipped | `sdk-pr345-second-ruby-public-green.log` |
| Failed MCP metadata case | exit 0, 1 passed | `sdk-pr345-second-mcp-contract-green.log` |
| Existing MCP environment cases | exit 0, 3 passed / 7 deselected | `sdk-pr345-second-mcp-env-green.log` |
| `heavy-slot.sh node scripts/check-python.mjs` | exit 0, mypy 64 native / 1 SDK / 4 LangChain files; 190 tests: 180 native + 10 LangChain, 0 skipped/xfailed/xpassed | `sdk-pr345-second-python-check-final.log` |
| Canonical-input `pnpm generate:mcp` and `pnpm generate:python` under heavy-slot | exit 0; generated surface wrappers match the tested runtime SHA-256 manifest | `sdk-pr345-second-generate-{mcp,python}.log`, `sdk-pr345-second-python-runtime-sha256.txt` |

The isolated LangChain receipt proves candidate Sending imports and executes with published Core 1.3.1. Native environment tests cover all three source wrappers; no claim is made that all three were dynamically tested against published Core. No assertion was weakened or removed, and no extra harness was introduced: existing public tests and cohort provenance gates caught these failures. Fresh independent reviews, including the generator source and four generated fingerprints: Standards 0 hard / 0 actionable heuristics; Spec 0 findings.

## Terminal CI at 8f4c78f and local Ruby correction

Exact head `8f4c78f050725b6d57a6b71d39178dee40c1774e` finished [CI run 41469429959](https://github.com/qubrics/qubrics-sdk/actions/runs/41469429959) with 32 successful jobs and two failures. Both failed-job logs were read. One transient HTTP/2 log-download failure was retried once; CI was not rerun. Receipts: `sdk-pr345-8f4-ci-terminal.json`, `sdk-pr345-8f4-ci-failed-retry.log`.

- Ruby job `125358795642`: three generated auth overrides exceeded cyclomatic/perceived complexity; the OAuth class exceeded 100 lines; dynamic symbol conversion was unnecessary. `scripts/generate-ruby.mjs:297-327` now extracts the existing upload-header/config fallback body into one private method. The upload-only guard and ordinary bearer branch are unchanged. Normal Ruby generation reproduced all three clients.
- Main verify job `125358795424`: `scripts/check-live-e2e-coverage.mjs:119` rejected nine missing operation IDs in `test/live-e2e/scenarios.json`, plus stale `docs/live-e2e-matrix.md`. This stopped the step before its connection-adapter tests. The canonical metadata writer was run with the same task-docs snapshots; it added all nine scenarios and matrix rows, then exposed two missing fixture-registry entries. Coverage remains blocked.

The first Ruby lint correction put the two existing delegated-upload cases in a second class in the same file and used symbol hash rockets. The effective default `Style/OneClassPerFile` and `Style/HashSyntax` rules rejected that layout. The repo enables new cops at `.rubocop.yml:2`; effective HashSyntax is `ruby19`. The final correction moves both cases unchanged into `packages/ruby/tests/test_delegated_upload.rb` and declares that file in `scripts/check-ruby.mjs:32`, matching the existing explicit runner entries. Fixture and assertions are preserved; no threshold or rule was disabled. Receipts: `sdk-pr345-ruby-rubocop-green.log`, `sdk-pr345-ruby-effective-cops.log`.

| Independent check | Result | Receipt |
| --- | --- | --- |
| Focused RuboCop on all five changed Ruby files | exit 0, no offences | `sdk-pr345-ruby-rubocop-final.log` |
| Existing OAuth/retry and moved upload public tests together | exit 0, 16 runs / 146 assertions / 0 skips | `sdk-pr345-ruby-public-final.log` |
| Exact new canonical runner entry | exit 0, 2 runs / 6 assertions / 0 skips | `sdk-pr345-ruby-runner-entry.log` |
| JavaScript syntax check for `scripts/check-ruby.mjs` | exit 0 | command result retained in worker handoff |
| Historical audit-manifest check | exit 0; historical schema-1 shape only | `sdk-pr345-live-e2e-audit-check.log` |

Fresh independent Ruby reviews: Standards 0 hard violations / 0 heuristic findings; Spec 0 findings across all seven candidate paths. No source change followed review. The metadata writer changed only its two declared outputs; it did not create live-test code, classifications or execution evidence. The historical audit manifest is unchanged.

## Compatibility review batch after 6a350342

Candidate reopened under source-only approval: nine source-proven defects block A17 legacy calls, empty-Qubrics fallback and retained-event field presence. Owner README corrections `5bb29fc` were integrated with main normally as `1619498c`; no README was rewritten. Existing floors, versions and manifests remain unchanged. Prior exact `6a350342` CI [41581583297](https://github.com/qubrics/qubrics-sdk/actions/runs/41581583297) is green but does not qualify this new candidate.

Canonical fixes remain at their origins: shared configuration for environment fallback, generators for native clients and retained-event decoding. Empty Qubrics values fall back to existing legacy/default semantics; explicit inputs, whitespace and empty legacy values retain their meaning. Go keeps the former keyed `XSendmuxUploadToken string` field and rejects mismatched present twins before authentication. PHP and Ruby retain published positional calls and current forms. Both token headers remain optional alternatives on the wire.

| Public regression | Actual red before fix | Green receipt |
| --- | --- | --- |
| TS environment requests | Six authentication failures | `env-model-ts-green.log`: 9 passed, 0 skipped |
| MCP environment resolution | Empty port reached `int("")` | `env-model-mcp-green.log`: 11 passed |
| Python environment requests | Six API-key/bearer validation failures | `compat-python-green.log`: 26 passed, including model/MCP cases |
| Python retained event, direct/nested | Two omitted keys became null; four null/string cases already passed | Same 26-case green includes all six round trips |
| Ruby environment | Key/token rejected; legacy URL became default | `compat-ruby-green.log`: 35 runs, 234 assertions, 0 skips across related public files |
| Ruby old four/five upload arguments | Four String-comparison/arity errors | Same Ruby green covers both methods, supplied options and current calls |
| Go generated upload server | Six conflicting/empty-twin requests returned 201 and invoked authentication/business handlers | `compat-go-green.log`: focused delegated-upload package tests passed |
| Go legacy keyed field | Four compile errors included the former keyed string literal | Same focused Go green compiled and ran both token families and middleware |
| PHP five upload variants | 15 TypeErrors among 40 cases; 25 current forms already passed | `compat-php-green.log`: 40 tests, 480 assertions; `compat-php-oauth-green.log`: 6 tests, 26 assertions |
| PHP non-empty zero env values | Three public factory cases silently selected legacy credentials/URLs | `compat-php-zero-env-green.log`: 6 passed, preserving legacy falsy/default and explicit settings |

Root's adjacent check proved that the actual Go HTTP path normalises padded twin values before the generated handler: `compat-go-whitespace-wire.log` passes without a trim generator change. A single-use verifier then exposed an OR-boundary defect: equal twins returned 401 after two authentication attempts, in direct and middleware cases (`compat-go-single-use-red.log`). The generator now skips the second alternative once the first succeeds; `compat-go-single-use-green.log` passes the whole delegated selection, retaining mismatch/empty-before-provider and missing/invalid-token coverage.

PHP's `?:` lookup additionally discarded non-empty `0`; its generator now tests only false/empty Qubrics values, keeping legacy `?:` semantics and the published Core API. Source survey identified the same empty-value problem in CLI logout and the public Python core helper. Their public reds were implicit logout exit 1 instead of 0 and helper `''` instead of `legacy`. Focused greens: `env-model-cli-profile-green.log` 3 passed/0 skipped; `env-model-core-helper-green.log` 1 passed. CLI `tsc -b` and focused helper mypy exited 0. All original assertions remain. The complete related Python replay, including the helper, is `compat-python-final-green.log`.

Final batch covers nine accepted implementation review findings plus four source-proven siblings: PHP non-empty zero env selection, CLI logout, the public Python helper, and Go OR double validation. The two README findings are fixed only through existing owner history. Remaining Go/Rust env lookups already skip empty Qubrics values and retain non-empty `0`/whitespace (`scripts/generate-go.mjs:597`, `rust/src/core.rs:273`); CLI base/set/operation lookups already use truthy fallback. No new implicit environment surface was added.

Red logs: `env-model-{ts,mcp,python-env,python-model}-red.log`, `ruby-{env,upload}-review-red.log`, `upload-go-php-{go-server,go-keyed,php-arguments}-red.log`. All receipts are under `.claude/artifacts/rebrand-qubrics-904/`.

No original assertion was removed or loosened. PHP's new history fixture needed the same runtime array assertion as `MailboxStreamArgumentsTest.php:51`, because Guzzle's by-reference history annotation also permits ArrayAccess; focused type checking then passed. Ruby's first credential implementation exceeded perceived complexity 9/8; extracting the shared private lookup preserved the two credential tests and cleared lint. An initial Ruby test used the system interpreter; the existing runner's `rbenv exec` corrected it. An initial PHP lint command named the wrong config file; `scripts/check-php.mjs:21` supplied canonical `phpcs.xml`. No dependency, rule, guard or threshold changed.

All four normal native generators exited 0 with canonical docs input. Focused PHP type/lint and RuboCop on six changed handwritten/wrapper files exited 0. First full drift ran all generators/coverage successfully, then staleness rejected only the newly generated MCP config source fingerprint; that exact hash-only output was staged normally and `compat-drift-check-green.log` exited 0. Additional PHP/Go origin changes regenerated normally; final MCP generation exited 0. The mandatory commit hook will re-run full drift on this expanded candidate after its two-axis review. No SDK push/merge, production write, package/Snap publication or deployment performed for this batch.

Fresh independent reviews inspected `git diff 6a350342 --` at HEAD `1619498c`, covering all 37 staged files and the inherited README correction: Standards 0 hard violations / 0 actionable heuristics; Spec 0 missing, unrequested or incorrect behaviours. No implementation changed after review. Final related Python replay passes 27 cases with zero skips; focused mypy passes five source files (`compat-python-final-{green,types}.log`). Expanded-candidate normal commit-hook receipt: `compat-final-normal-commit.log`. Root owns the genuine docs follow-up and subsequent push ordering; publication and production remain held.

## Exact-head CI follow-up at 4910037

Normal push of `491003792dd742cb2c83e4a09501abdf4f4458c9` exited 0 after genuine docs78 follow-up `944a2a2c305dbdad5d687dbf0ee050556e9611e2`. Exact CI run `41587673936` finished with 27 successful and seven failed jobs. Every failed-job log was downloaded and searched; `compat-491-all-terminal-failed.log` accounts for all seven. No CI rerun occurred.

- Go job `125756855068`: all Go tests passed, then `errcheck` rejected unchecked `response.Body.Close()` at `go/sending/upload_token_test.go:75`. The added test now asserts that error; no runtime code changed. Focused Go tests pass. Exact pinned linter passes with zero issues under the repository's declared `go1.27.2` (`compat-ci-go-lint-repopin.log`). The first local lint command encountered shell `GOTOOLCHAIN=local`/Go 1.23.4; `auto` selected the linter's minimum 1.26 toolchain and panicked on 1.27 source. Explicitly selecting the existing repo pin resolves this tool-environment mismatch, without changing any repo config.
- Ruby job `125756855177`: `scripts/check-ruby.mjs:131` expected the former literal upload declaration after the generator intentionally added `legacy_opts = nil` to retain old calls. Only that expected string changed; the upload, twin-header, Content-Length and lower-bound assertions remain unchanged. The existing complete header-contract guard passes (`compat-ci-ruby-guard-green.log`).
- Python runtime jobs `125756855153` (3.10), `125756855167` (3.11), `125756855114` (3.12), `125756855227` (3.13), and `125756855160` (3.14): all stop collecting `test_environment.py:7` because installed-wheel tests use `--import-mode=importlib` and cannot import sibling `test_oauth_retry`. Source-mode tests had missed that isolation signal. The same collection failure was reproduced from an isolated artifact cwd (`env-model-importlib-red.log`).

Canonical per [pytest import-mode and fixture documentation](https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/pythonpath.rst): test modules cannot import each other in importlib mode; shared fixtures belong in auto-discovered `conftest.py`. The existing endpoint fixture moved there unchanged, and the environment module retains its three public client cases directly. No import-path, consumer-provenance or runtime-package change. AST comparison proves the endpoint fixture unchanged (`compat-ci-fixture-preservation.log`). The identical isolated-cwd importlib case now passes 10 tests; its shared environment/OAuth path passes 35 tests, no skips. Focused mypy passes all three changed native test files (`env-model-importlib-green.log`, `compat-ci-importlib-green.log`, `compat-ci-python-types.log`).

The all-surface sweep also found seven new review comments: one repeats the Go close failure, two identify ambient-environment test isolation, and four claim Ruby `Lint/SafeNavigationWithEmpty` warnings. Both test-isolation classes were reproduced without changing assertions: MCP legacy selection failed against an injected Qubrics fixture key; TS request and missing-credential tests failed against injected fake credentials. Tests now clear only the settings under test and restore them through `monkeypatch`/`t.after`. Greens: MCP two parameter cases; TS six environment/validation cases and three single-key validation cases (`compat-ci-{mcp,ts}-ambient-{red,green}.log`, `compat-ci-ts-missing-ambient-{red,green}.log`). Focused MCP mypy and JavaScript syntax checks pass. Review exposed the same setup defect in the older Python configuration case: an ambient access token made all three clients reject ambiguous credentials. Its setup now clears the same six tested settings through `monkeypatch`, retaining every assertion; `compat-ci-python-ambient-{red,green}.log` records that proof.

All four Ruby warning claims are false positives under locked RuboCop 1.87.0: running the named cop against all four reported files finds no offences (`compat-ci-ruby-cop-validation.log`), matching the earlier six-file clean lint. Existing nil/empty environment semantics and Ruby generator/output remain unchanged. No new runtime, generated, schema, version, threshold or assertion change belongs to this CI/test-only follow-up. Full CI and settled review at its eventual exact head remain outstanding.

Fresh bounded reviews, including the final Python ambient-setup delta: Standards 0 hard violations / 0 actionable heuristics; Spec 0 remaining findings. No implementation changed after review. No test or assertion was removed. Normal full-drift commit-hook receipt: `compat-ci-only-normal-commit.log`; ordinary push receipt: `compat-ci-only-normal-push.log`. Existing user-facing `4910037` then genuine docs `944a2a2c` chronology remains unchanged by this CI/test-only follow-up.

## Cleanup

Owned disposable fixtures are stopped. Command guard rejected the prior cache teardown; no deletion workaround attempted. SDK build/test caches remain listed in `sdk-final-handoff.md` for manual removal.
