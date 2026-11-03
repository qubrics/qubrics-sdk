# A15 GitHub references and approved A17 README handoff

Part of qubrics/qubrics#897. Final base: 276082cb5e525c0a6fb1e521858846cbd21c8714. Current GitHub consumers, strict repository guards, package repository metadata, generated Ruby homepage source and current installation/support instructions use canonical Qubrics repository identities. Internal package names and service hosts remain unchanged except the separately authorised A17 README handoff, with the explicit SDK-method correction below.

The original handoff was applied verbatim after an independent check and confirmed by reverse check before the later approved SDK-method exception:
`/Users/rj/Desktop/GIT-REPOS/sendmux/.claude/artifacts/rebrand-qubrics-904/sdk-readme-a17.patch`
SHA256: `ec4d09b802194c50acbdd3c5b27bbda12e0a8033a7fa637f3b6e6374478631fc`.
Only the approved SDK-method corrections below subsequently differ from that handoff. Runtime counterparts remain owned by #904.

Strict publication reads now target `qubrics/qubrics-sdk`. PHP split publishing accepts only exact canonical SSH/HTTPS package repository origins. Immutable npm attestations retain the exact former producer identity alongside the current identity; the dependency source must match that same identity and exact producer commit. Unrecognised identities, mixed identities and wrong commits remain rejected. Historical provenance and changelog evidence remain intact.

Existing tests at the guard seams were seen red before the fixes:
- Current Snap release: `Missing producer release tag: ts-cli-v1.2.3`, then `Snap npm provenance does not identify the CLI producer commit`.
- PHP split remote: `Split origin does not identify the expected package repository`.
- Current/historical Snap cases and wrong-commit/unknown/mixed rejection cases pass; official release construction test passes after frozen dependency installation resolved missing release-please.
- PHP split/canary tests: 20 passed, 0 failed/skipped. Existing Snap workflow and Chocolatey package-file checks pass.
- Build-dependent connections tests could not start in the fresh worktree because `@sendmux/sdk/dist/index.js` was absent; they remain for normal SDK CI after its build. No stale dist copied, no assertion weakened.
- `git apply --check`, patch application, reverse check and `git diff --check`: exit 0.

Logs and exact commands: control-plane MAIN `.claude/artifacts/rebrand-qubrics-897/sdk-state.md` and referenced logs. Independent Standards/Spec reviews found no functional source defect in the bounded A15/A17 diff.

The original normal commit was blocked by `ogen failed to infer fields discriminator` on the newer current contract. The separate approved prerequisite fixed the API schema origin, PHP generation and missing Calendar lifecycle inputs: docs80 merged `12ef5105`, API917 merged `e0462ea3`, SDK346 merged `276082cb`, all exact-head CI green. This row4 branch rebased onto `276082cb`; the original 69-file patch is preserved, with its already-shipped CI URL hunk leaving 68 remaining files. README handoff reverse check remains exit0. No older-contract substitution or bypass.

Post-merge Release Please run `41571510043` failed `Unexpected publication repository`: main `scripts/publication-guard.mjs:14,231` still requires `Sendmux/sendmux-sdk`, while GitHub identifies the renamed repo as `qubrics/qubrics-sdk`. This existing row4 origin correction targets canonical reads and preserves strict equality. No rerun, release threshold or guard bypass. Merged PRs labelled `autorelease: pending` were empty before qualification; no package version/manifest changes are in this diff. Publication remains gated separately.

No hook bypass, assertion weakening, publication, release tag or deploy performed. Full normal generation/commit hook and final exact-head CI remain required for this branch; API917 production deployment queues after898 and requires its own slot/GO. Rows2/5 stay held902.

After rebasing onto the merged generation prerequisite, focused guard/canary/PHP fixtures passed: 87 tests, no skips, exit0 (`row4-guards-green.log`); existing Snap workflow check exit0 (`row4-snap-green.log`). That phase's independent Standards/Spec reviews found zero issues. The original handoff reverse-check exited0 before the later approved SDK-method exception.

Ops requested the Ruby generator path for #904's A17 upload-auth guard. Its one-line canonical homepage hunk is committed separately at `a2073b17568512abfdf004c1bd99eadeb541b8a4`, with normal full drift hook exit0; only that lease was released. The first isolated-commit attempt correctly detected the MCP provenance hash derived from other uncommitted `pyproject.toml` edits. Temporarily isolating those edits let the Ruby-only commit qualify against matching inputs; all remaining changes were then restored. The regenerated MCP contract hash accompanies its changed package metadata in the remaining commit. No current-input substitution, provenance bypass or generated-file hand edit.

The generated MCP contract was committed normally in `688af4ae13e537690ac0376ce2bfde15fefde7e2` and its lease released to #904; no other derived Python/MCP output remains claimed. Normal full drift hook exit0 is recorded in `row4-commit.log`.

CI run `41572995229` selected the stale matching docs branch `42e4027` through the existing current-input resolver (`.github/workflows/ci.yml:25-46,142-164`). That branch lacked merged docs80: Go failed discriminator inference, MCP lacked `mailboxDeleteCalendar`, and PHP lacked the two named webhook payload models. The clean owned docs branch was merged with current main and pushed at `f363ed53`; its OpenAPI inputs byte-match main `12ef5105`. Resolver and assertions remain unchanged.

The same run's Python matrix and Ruby checks enforced existing changed-package dependency floors after this PR edited their metadata (`scripts/python-release-guardrails.mjs:53-66,118-123`; `scripts/check-ruby.mjs:55-95`). LangChain's mailbox floor is corrected to the manifest's `2.0.2`; Ruby SDK mailbox/management floors to `2.0.2`/`2.0.1`, with `Gemfile.lock` regenerated by `rbenv exec bundle lock --local` (exit0). Both existing floor validators were seen red, then all Python and Ruby package floors passed (exit0 each; `row4-{python,ruby}-floor-{red,green}.log`). No policy or test weakened, no new harness. Every failed job is retained in `row4-ci-all-failed.log`.

## Operator-approved SDK method correction

Ops Watch 2026-11-03 15:07 chose A: the approved README handoff may change only generated Python/Ruby SDK method names to existing symbols. Repository URLs, QUBRICS environment names, MCP aliases and branding stay as approved. Adding SDK operation aliases is new public API and is Parked/out of scope. Generated-symbol citations for each corrected example follow below.

Python: 19 references in four READMEs. Generated-source method audit red exit1 (`19/19 documented generated-method references unsupported`) then green exit0; exact non-method preservation and mapping checks exit0. Local runtime import stopped at missing `dateutil` before method lookup; no dependency substitute or API call. Normal CI supplies the installed-package runtime qualification. Per-example command/source details: MAIN artifact `python-method-example-map.md`.

| Generated symbol and definition | Corrected examples (all SDK-relative) |
| --- | --- |
| `MailboxAPIApi.mailbox_list_messages` — `packages/python/mailbox/sendmux_mailbox/api/mailbox_api_api.py:14606` | `packages/python/mailbox/README.md:52`, `packages/python/mailbox/README.md:171`, `packages/python/mailbox/README.md:205` |
| `MailboxAPIApi.mailbox_get_connection` — `packages/python/mailbox/sendmux_mailbox/api/mailbox_api_api.py:7201` | `packages/python/mailbox/README.md:72`, `packages/python/sdk/README.md:55` |
| `MailboxAPIApi.mailbox_get_message` — `packages/python/mailbox/sendmux_mailbox/api/mailbox_api_api.py:8970` | `packages/python/mailbox/README.md:80`, `packages/python/mailbox/README.md:93` |
| `MailboxAPIApi.mailbox_upload_attachment` — `packages/python/mailbox/sendmux_mailbox/api/mailbox_api_api.py:21799` | `packages/python/mailbox/README.md:102` |
| `MailboxAPIApi.mailbox_send_message` — `packages/python/mailbox/sendmux_mailbox/api/mailbox_api_api.py:19438` | `packages/python/mailbox/README.md:108` |
| `MailboxAPIApi.mailbox_list_thread_messages` — `packages/python/mailbox/sendmux_mailbox/api/mailbox_api_api.py:16110` | `packages/python/mailbox/README.md:177` |
| `DomainsApi.management_list_domains` — `packages/python/management/sendmux_management/api/domains_api.py:1172` | `packages/python/management/README.md:52` |
| `DomainsApi.management_get_domain` — `packages/python/management/sendmux_management/api/domains_api.py:623` | `packages/python/management/README.md:76` |
| `ConnectionApi.management_get_connection` — `packages/python/management/sendmux_management/api/connection_api.py:42` | `packages/python/sdk/README.md:45`, `packages/python/sdk/README.md:54` |
| `MetaApi.sending_get_connection` — `packages/python/sending/sendmux_sending/api/meta_api.py:42` | `packages/python/sending/README.md:38`, `packages/python/sdk/README.md:56` |
| `EmailsApi.sending_send_email` — `packages/python/sending/sendmux_sending/api/emails_api.py:45` | `packages/python/sending/README.md:66`, `packages/python/sending/README.md:121`, `packages/python/sdk/README.md:84` |

Ruby: 32 references in five READMEs, 13 generated methods. Runtime reflection against the generated classes was red exit1 for every prefixed name, then green exit0 for all 32 corrected occurrences using `source_location`; no API calls. Exact non-method preservation and diff checks exit0. Receiver wrappers/imports and commands: MAIN artifact `ruby-method-example-map.md`.

| Generated instance method and definition | Corrected examples (all SDK-relative) |
| --- | --- |
| `MailboxAPIApi#mailbox_list_messages` — `packages/ruby/mailbox/lib/sendmux_mailbox_generated/api/mailbox_api_api.rb:3495` | `packages/ruby/core/README.md:67`, `packages/ruby/mailbox/README.md:78`, `packages/ruby/mailbox/README.md:118`, `packages/ruby/mailbox/README.md:129`, `packages/ruby/mailbox/README.md:143`, `packages/ruby/sdk/README.md:101` |
| `MailboxAPIApi#mailbox_list_thread_messages` — `packages/ruby/mailbox/lib/sendmux_mailbox_generated/api/mailbox_api_api.rb:3847` | `packages/ruby/mailbox/README.md:38`, `packages/ruby/mailbox/README.md:73`, `packages/ruby/sdk/README.md:77` |
| `MailboxAPIApi#mailbox_get_me` — `packages/ruby/mailbox/lib/sendmux_mailbox_generated/api/mailbox_api_api.rb:2017` | `packages/ruby/mailbox/README.md:117`, `packages/ruby/mailbox/README.md:128` |
| `MailboxAPIApi#mailbox_get_message` — `packages/ruby/mailbox/lib/sendmux_mailbox_generated/api/mailbox_api_api.rb:2081` | `packages/ruby/mailbox/README.md:130`, `packages/ruby/mailbox/README.md:168` |
| `MailboxAPIApi#mailbox_send_message` — `packages/ruby/mailbox/lib/sendmux_mailbox_generated/api/mailbox_api_api.rb:4628` | `packages/ruby/mailbox/README.md:131`, `packages/ruby/mailbox/README.md:158` |
| `MailboxAPIApi#mailbox_list_threads` — `packages/ruby/mailbox/lib/sendmux_mailbox_generated/api/mailbox_api_api.rb:3940` | `packages/ruby/mailbox/README.md:132` |
| `MailboxAPIApi#mailbox_upload_attachment` — `packages/ruby/mailbox/lib/sendmux_mailbox_generated/api/mailbox_api_api.rb:5189` | `packages/ruby/mailbox/README.md:133`, `packages/ruby/mailbox/README.md:158` |
| `MailboxesApi#management_list_mailboxes` — `packages/ruby/management/lib/sendmux_management_generated/api/mailboxes_api.rb:609` | `packages/ruby/management/README.md:94`, `packages/ruby/management/README.md:116`, `packages/ruby/management/README.md:144`, `packages/ruby/sdk/README.md:181` |
| `DomainsApi#management_list_domains` — `packages/ruby/management/lib/sendmux_management_generated/api/domains_api.rb:291` | `packages/ruby/management/README.md:95`, `packages/ruby/management/README.md:116` |
| `MailboxesApi#management_create_mailbox` — `packages/ruby/management/lib/sendmux_management_generated/api/mailboxes_api.rb:92` | `packages/ruby/management/README.md:116` |
| `WebhooksApi#management_create_webhook` — `packages/ruby/management/lib/sendmux_management_generated/api/webhooks_api.rb:28` | `packages/ruby/management/README.md:116`, `packages/ruby/management/README.md:123` |
| `EmailsApi#sending_send_email` — `packages/ruby/sending/lib/sendmux_sending_generated/api/emails_api.rb:28` | `packages/ruby/sending/README.md:65`, `packages/ruby/sending/README.md:77`, `packages/ruby/sending/README.md:87`, `packages/ruby/sending/README.md:99` |
| `EmailsApi#sending_send_email_batch` — `packages/ruby/sending/lib/sendmux_sending_generated/api/emails_api.rb:103` | `packages/ruby/sending/README.md:77` |

SDK `docs/` and the owned canonical docs checkout contain no additional prefixed Python/Ruby method invocations. No new test/harness file, runtime API or operation alias was added.

Fresh independent Standards and Spec reviews of the full PR from base `276082cb` through this correction both found zero issues. All 51 generated-symbol citations were independently checked; exact method-only preservation passed (`row4-sdk-example-preservation.log`). Final normal commit hook/current-input generation and new-head CI remain required before the delegated source merge.

## Parked with #904: retained runtime/contract examples

Ops explicitly deferred these compatibility dependencies and approved merging this ticket without reverting them. Each location remains unchanged; #904 owns environment/CLI runtime aliases and MCP runtime discovery plus normally generated contract verification. Explicit `os.environ`/`process.env` reads passed into SDK factories are ordinary caller-defined variables and do not need runtime alias support.

| Location | Retained token/dependency |
| --- | --- |
| `README.md:138` | MCP `qubrics_management_get_connection` |
| `README.md:139` | MCP `qubrics_mailbox_get_connection` |
| `README.md:140` | MCP `qubrics_sending_get_connection` |
| `README.md:178` | MCP wait/get-attachment aliases |
| `packages/ts/cli/README.md:55` | `QUBRICS_ACCESS_TOKEN` / `QUBRICS_API_KEY` runtime credentials |
| `packages/python/mcp/README.md:62` | Standalone Mailbox `QUBRICS_API_KEY` |
| `packages/python/mcp/README.md:63` | Standalone Management `QUBRICS_API_KEY` |
| `packages/python/mcp/README.md:64` | Standalone Sending `QUBRICS_API_KEY` |
| `packages/python/mcp/README.md:70` | Combined `QUBRICS_MCP_SURFACES` |
| `packages/python/mcp/README.md:71` | Combined `QUBRICS_MAILBOX_API_KEY` |
| `packages/python/mcp/README.md:72` | Combined `QUBRICS_SENDING_API_KEY` |
| `packages/python/mcp/README.md:79` | Combined `QUBRICS_MCP_SURFACES` |
| `packages/python/mcp/README.md:80` | Combined `QUBRICS_MAILBOX_API_KEY` |
| `packages/python/mcp/README.md:81` | Combined `QUBRICS_MANAGEMENT_API_KEY` |
| `packages/python/mcp/README.md:82` | Combined `QUBRICS_SENDING_API_KEY` |
| `packages/python/mcp/README.md:93` | Explicit stdio `QUBRICS_API_KEY` |
| `packages/python/mcp/README.md:99` | HTTP `QUBRICS_API_KEY` |
| `packages/python/mcp/README.md:100` | HTTP `QUBRICS_MCP_HTTP_BEARER_TOKEN` |
| `packages/python/mcp/README.md:141` | `QUBRICS_MCP_SURFACES` configuration |
| `packages/python/mcp/README.md:142` | `QUBRICS_API_KEY` configuration |
| `packages/python/mcp/README.md:143` | `QUBRICS_MAILBOX_API_KEY` configuration |
| `packages/python/mcp/README.md:144` | `QUBRICS_MANAGEMENT_API_KEY` configuration |
| `packages/python/mcp/README.md:145` | `QUBRICS_SENDING_API_KEY` configuration |
| `packages/python/mcp/README.md:146` | `QUBRICS_APP_BASE_URL` configuration |
| `packages/python/mcp/README.md:147` | `QUBRICS_SENDING_BASE_URL` configuration |
| `packages/python/mcp/README.md:148` | `QUBRICS_MCP_TRANSPORT` configuration |
| `packages/python/mcp/README.md:149` | `QUBRICS_MCP_HOST` configuration |
| `packages/python/mcp/README.md:150` | `QUBRICS_MCP_PORT` configuration |
| `packages/python/mcp/README.md:151` | `QUBRICS_MCP_PATH` configuration |
| `packages/python/mcp/README.md:152` | `QUBRICS_MCP_HTTP_BEARER_TOKEN` configuration |
| `packages/python/mcp/README.md:153` | `QUBRICS_MCP_ALLOW_UNAUTHENTICATED_HTTP` configuration |
| `packages/python/mcp/README.md:154` | `QUBRICS_MCP_ALLOWED_ORIGINS` configuration |
| `packages/python/mcp/README.md:155` | `QUBRICS_MCP_OPENAPI_INPUT_DIR` configuration |
| `packages/python/mcp/README.md:156` | `QUBRICS_MCP_APP_OPENAPI` configuration |
| `packages/python/mcp/README.md:157` | `QUBRICS_MCP_SENDING_OPENAPI` configuration |
| `packages/python/mcp/README.md:158` | `QUBRICS_MCP_TIMEOUT_SECONDS` configuration |
| `packages/python/mcp/README.md:159` | `QUBRICS_MCP_RETRY_MAX_ATTEMPTS` configuration |
| `packages/python/mcp/README.md:160` | `QUBRICS_MCP_RETRY_MAX_ELAPSED_SECONDS` configuration |
| `packages/python/mcp/README.md:195` | MCP `qubrics_mailbox_wait_for_message` |
| `packages/python/mcp/README.md:199` | MCP `qubrics_mailbox_read_attachment` |
| `packages/python/mcp/README.md:202` | MCP `qubrics_mailbox_get_attachment` |
| `packages/python/mcp/README.md:204` | MCP `qubrics_mailbox_upload_attachment` |
| `packages/python/mcp/README.md:211` | MCP `qubrics_mailbox_send_message` |
| `packages/python/mcp/README.md:213` | MCP Sending upload/create-upload/send aliases |

API917 production deploy remains queued behind #898; the sendmux slot is frozen. No tag, package/image publication or deploy is authorised by this source-merge instruction.

Polish pass: skipped — exact technical-token corrections and approved verbatim handoff with the explicit SDK-method exception.
