# Ruby Mailbox calendar-free source qualification

Status: PR387 source qualification, not merged to main or published. Shared
release metadata is integrated; producers and docs are live and equal.
The initial qualification below used Sending successor `b7dad6ca`.
The final section records the cache-enabled parent refresh and fresh gates.
No tag, queue, environment or registry write occurred.

Goal: qualify Ruby `qubrics-mailbox 3.0.0` without calendar client code for
#344, preserving the operator's separate exact-file publication gate.
Base: `e8d46fa2f91ece4ebab28c7e8ca51e6f1d53b5fa` of
`https://github.com/qubrics/qubrics-sdk.git`.

## Fresh qualification after producer deployment

Docs75's joint runtime receipt proves both producers and docs main
`0775e2f21428b215165fd25a0bf1894dcf339d46` equal. Existing generation ran
against those emitted inputs, with no source snapshot substitution,
workflow pin or fallback. A preliminary invocation selected the local
docs checkout `abdfa0f6`; its two Sending comment differences revealed
that stale local input. Re-running with the verified canonical input
directory restored exact Sending/Management source equality to the new
base. No sibling source change remains in this Mailbox diff.

Fresh native proof: **6 tests, 34 assertions, zero skips**. Existing
calendar-planning checks pass **2/2, zero skips** and the coverage check
passes **128 OpenAPI operations plus 2 custom MCP operations**. JavaScript
syntax checks and focused RuboCop pass. Local Bundler rejects Ruby 3.4.1
against the unchanged CI requirement 3.4.12; direct installed RuboCop
provides the local focused check, while normal CI retains Ruby 3.4.12.
No runtime requirement or assertion changed.

The rebuilt artifact supersedes the earlier provisional archives:
`qubrics-mailbox-3.0.0.gem`, **110,592 bytes**, SHA256
`7577dd99a64aebaac44c517943ca84bc8fd1058ca8b03ff5e9cd692d6226d602`.
Exact file: `/Users/rj/Desktop/GIT-REPOS/sendmux-sdk/.claude/artifacts/rebrand-qubrics-sdk344/ruby-mailbox-live-20261119/gems/qubrics-mailbox-3.0.0.gem`.
A fresh isolated public-dependency install passes the same native **6/34**
checks. All **166 packaged files, including 163 runtime files**, match
source byte-for-byte. No calendar paths/content/methods/constants remain;
ordinary message methods, Core 2.0.0, default
`https://app.qubrics.com/api/v1`, dependency resolution and nil post-install
message pass. Installed archive and public Core archive hashes match.

Fresh raw receipts in MAIN `ruby-mailbox-integration-20261119/`:
`post-producer-generate-canonical.log`, `post-producer-native.log`,
`post-producer-applicability.log`, `post-producer-coverage.log`,
`post-producer-rubocop-direct.log`, `post-producer-install.log`,
`post-producer-installed-proof.json`, `post-producer-installed-native.log`.
`python-stat-from-a326bc92.txt` is empty: `python/` is unchanged from
`a326bc923fff448470d908bb527afaaa35f6d739`.

At initial qualification, default Skills v2.0.5 lacked evidence for 15 of 22
changed producer pairs on the parent source. The owner handoff is MAIN
task `producer-sync-skills-origin-20261119.md`. This candidate still needs
fresh exact-source default acceptance and normal PR CI. Calendar exposure
is **NO**; keeping the gem unpublished remains an option. No publication
approval follows from these proofs; source rollback is normal revert.

## Origin and smallest change

Canonical precedent: `scripts/generate-python.mjs:230` excludes
`/mailbox/calendars` and `/mailbox/calendar-events` at the input-path
selection boundary. Ruby `scripts/generate-ruby.mjs:146` previously selected
all Mailbox API paths. The Ruby generator now applies the same anchored
path exclusion before tag selection; its existing transitive component
pruning removes unreachable calendar models. Generated clients were
produced by the existing `pnpm generate:ruby` command, never hand-patched.

Only the Mailbox generator branch changes. Other surfaces, management's
retained opaque payloads and its plain-string event labels are unchanged.
No runtime request, write, process or dependency was added.

Generated difference: 20 calendar API methods and 22 calendar model files
removed. The method-body comparison found all 107 ordinary methods
byte-identical, zero other methods changed or added. Filtered generator
input has 43 paths and 107 schemas, zero calendar paths/schemas.

Native version and the shared manifest now agree at `3.0.0`. Official
`bundle lock --local` updated only the Mailbox version and the SDK's
Mailbox requirement to `>= 3.0.0, < 4.0`. The SDK's own version is unchanged
for its later release. This local build is not an approved publication artifact.

## Native red and green

Existing runtime test file `packages/ruby/tests/test_mailbox_deprecated_aliases.rb`
adds one case for withheld calendar methods/constants and a retained ordinary
message method. The realistic regression is removing the generator's path
exclusion and regenerating; its pre-fix run was observed red:

```text
test_calendar_clients_are_withheld_while_message_clients_remain
Expected [:mailbox_create_calendar_with_http_info, ...] to be empty.
6 runs, 30 assertions, 1 failures, 0 errors, 0 skips
```

After official regeneration: **6 tests, 34 assertions, zero failures,
errors or skips**. Existing deprecated aliases and real model construction
still pass. No assertion was removed, loosened or skipped.
Focused RuboCop: **5 files inspected, no offences detected**.
`git diff --check`: exit 0.

## Released default acceptance and parent refresh

Skills v2.0.6 is latest at
`9e2659c9dba3efd943190f2541016d0548db7201`; its actual released acceptance
asset SHA256 is
`809a7d4378fb08eed5a0ecd16b59448dc6aebb31c7c6a144e5e29ed7949543c6`.
The unchanged default selection and official release binding passed. Fresh
exact Mailbox candidate `a0ef57d431959257ddb2da30cee6b6e941fba9d3` passed
live equality and all 22 results, candidate digest
`458b9389590b4bb884e3e963fa0d2494d83a5689ba1a21b3f98af6dfe12e7f35`.
Raw MAIN artifacts: `default-v206-mailbox/receipts/` and
`default-v206-b25a7cbc/mailbox-guard.log`. Normal CI `44486055882` attempt 2
passed after the single authorised Maven relief rerun; no further rerun.

After PR385 reached main as `1a833169` with main CI `44492953710` green
35 of 35, this source normally merges the refreshed Sending parent
`ec5fc13f`. It receives the reviewed CI cache and measured evidence without
a force-push. Packaged Mailbox and Sending source remain unchanged from
`a0ef57d4`; the exact frozen Mailbox archive above remains 110,592 bytes,
SHA256 `7577dd99…26d602`. Existing native/source/archive proofs therefore
continue to bind the same bytes. No calendar endpoint or type is added.
Fresh exact-head CI/default acceptance and review remain required on the
successor. No publication approval follows; holding the gem stays available.

## Actual built gem and isolated consumer

Official `gem build qubrics-mailbox.gemspec` produced provisional local file
`qubrics-mailbox-3.0.0.gem`, **110,592 bytes**, SHA256
`257058444967d871398ea4a62f1fb8fed9d6d7a498cf1edf614379fdb0462fea`.
Its name/version come from native package metadata. No upload is authorised.

Installed that actual file into an initially absent task-owned GEM_HOME;
GEM_PATH pointed exclusively to that home. Official public dependency
resolution installed `qubrics-core 2.0.0` and seven other runtime gems.
The installed native test required Minitest, absent from runtime dependencies;
installed the existing lockfile's development `minitest 5.27.0` into the same
isolated home, then the native test passed **6/34, zero skips**. This was an
environment correction, not a source or assertion correction.

Actual installed gem inspection passed:

- All **163 runtime files** are byte-identical to this candidate's source.
- Zero calendar file paths/content, public API methods or generated constants.
- Ordinary `mailbox_list_messages` remains callable; compatibility/model tests pass.
- Exact Mailbox version `3.0.0`, resolved Core `2.0.0`.
- Default base URL `https://app.qubrics.com/api/v1`.
- Cached installed archive SHA256 equals the built file's complete SHA256.
- `post_install_message` is nil; no move announcement exists in package README/changelog.

Two preliminary read-only inspection commands used the wrong RubyGems
representation: installed gemspecs omit the archive file list, and
`Configuration#host` returns only `app.qubrics.com`. Corrected inspection
reads `Gem::Package#spec.files` from the actual cached archive and checks the
public `Configuration#base_url` (`configuration.rb:215`). Both invalid
inspection outputs remain retained; neither was a package failure.

## Receipts and handoff

Raw receipts in SDK MAIN:
`.claude/artifacts/rebrand-qubrics-sdk344/ruby-mailbox-recut-20261119/`:

- `native-red.log`, `native-green.log`, `rubocop.log`, `generate-ruby.log`.
- `ordinary-api-comparison.json`, `filtered-spec-proof.json`.
- `gem-build.log`, `qubrics-mailbox-3.0.0.gem`.
- `isolated-qualification-install.log`, `isolated-qualification-minitest.log`.
- `installed-native-corrected.log`, `installed-gem-final.json/.stderr`.
- Preliminary `installed-native.log`, `installed-gem-proof.stderr`,
  `installed-gem-qualification.stderr` explain corrected measurement setup.

Consumer/spec-cache and local `.tmp/ruby-codegen`/`.codegen` caches are
removed after qualification; source, provisional gem and cited receipts
remain for parent integration. No other owner's work or cache touched.
Parent has requested no push/CI while its documented upstream docs drift
remains unresolved. Fresh integration qualification is still required;
this source proof does not bypass that gate or confer publication approval.

Parked: none. Full #344 and Ruby publication remain incomplete.

## Root integration, 19 November 2026

The neutral Mailbox README and 3.0.0 changelog state calendar exclusion
and the Core 2 dependency. No move announcement or post-install message
was added. Fresh-reader Spec/polish critique passed; the humanize pass
ran once with protected names, versions and claims unchanged.

The rebuild after those packaged documentation changes is:
`qubrics-mailbox-3.0.0.gem`, **110,592 bytes**, SHA256
`1d014427f58ebbcb750858411a5287c3b6b1cf9e302acc2a53eeec06ce26ff78`.
Its absolute path is SDK MAIN
`.claude/artifacts/rebrand-qubrics-sdk344/ruby-mailbox-integration-20261119/qubrics-mailbox-3.0.0.gem`.
It supersedes the earlier provisional archive only for this local integration
proof. Neither archive has publication approval.

A new isolated GEM_HOME installed the rebuilt archive with public Core
2.0.0. All 163 installed runtime files matched this worktree byte-for-byte;
no calendar content, paths, methods or constants remained. Ordinary
`mailbox_list_messages`, version 3.0.0, dependency satisfaction, default
`https://app.qubrics.com/api/v1`, nil post-install message and installed-cache
archive SHA256 all passed. The native test against the actual installed
archive passed **6 tests / 34 assertions, zero skips** after installing the
existing development dependency Minitest 5.27.0 into that isolated home.
Local Ruby is 3.4.1; the unchanged CI toolchain remains 3.4.12, not yet run
against this integrated candidate. No global install or configuration changed.

Focused dependency-floor and native release-guardrail checks passed.
RuboCop passed for all three applicable changed files under the existing
generated-file exclusions. Preliminary commands incorrectly omitted Ruby
load paths, explicitly selected excluded generated files, and invoked gem
build from the workspace root. Corrected invocation setup passed without
any source, assertion or lint-policy change. Those logs are retained.

### Advertised runtime capability correction

Standards review found ten calendar operations still marked Ruby-applicable
by `scripts/check-live-e2e-coverage.mjs:363`. The actual runner trusts that
list (`scripts/run-live-e2e.mjs:324`) before executing the Ruby adapter,
which would reject the removed export (`scripts/live-e2e-ruby.rb:110`).
This is the same calendar-removal cause at its other caller, not extra scope.

The existing Python withholding test was parameterised for Python and
Ruby, preserving every assertion. Before the correction, Python passed and
Ruby failed at `scripts/test-live-e2e-safety.mjs:189`:
`assert.ok(pairs.filter(pair => pair.adapter === adapter).every(pair => pair.applicable === false))`.
The source generator now applies the existing Python exclusion to Ruby
too; its documented `--write` command regenerated exactly ten Ruby
scenario/matrix rows. Other adapters remain applicable. The focused test
then passed **2/2, zero skips**, including ordinary Management applicability,
zero HTTP requests and zero fixture resources for withheld calendar calls.
The official coverage check passed **128 OpenAPI operations + 2 custom MCP
operations**. No live credentials, API mutation, new harness, workflow,
command, ownership assertion or timeout change was used.

Both independent final reviews report zero unresolved Spec/Standards
findings. Code/readability and documentation checks need no further change.

Integration receipts are under SDK MAIN
`.claude/artifacts/rebrand-qubrics-sdk344/ruby-mailbox-integration-20261119/`:
`dependency-floors.log`, `release-guardrails.log`, `native-corrected.log`,
`rubocop-corrected.log`, `build-package-directory.log`, `isolated-install.log`,
`installed-gem-proof.json`, `installed-native.log`,
`applicability-red-after-build.log`, `applicability-green.log` and
`applicability-check.log`. The preliminary applicability run lacked the
workspace SDK build; the official targeted dependency build fixed that
environment prerequisite before the genuine red/green run.

No commit, push or CI retry was attempted while the shared-input hold
remains. The unchanged `.githooks/pre-commit` runs full `pnpm drift:check`;
no hook bypass was used. CI's docs/live-producer disagreement is confirmed
in MAIN task `pr385-docs-origin-blocker-20261119.md`. Do not restore
snapshots, pin an input or repeat that known red. Resume normal
generation/commit/default/PR qualification after docs75
reports producer deployment and emitted-docs sync. Sending remains first
in the ordered publish asks; Mailbox source and this provisional gem remain held.

The fresh isolated GEM_HOME, five targeted TypeScript dependency-build
directories and five incremental build-cache files were removed after
the checks. Absence was verified; source, provisional archive and cited
logs remain because this #344 slice is open. No worktree or shared owner
resource was removed.
