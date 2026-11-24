# Ruby Mailbox source qualification

Status: PR387 source qualification, not merged to main or published. Shared
release metadata is integrated; producers and docs are live and equal.
The initial qualification below used Sending successor `b7dad6ca`.
The final section records the cache-enabled parent refresh and fresh gates.
No tag, queue, environment or registry write occurred.

Goal: qualify Ruby `qubrics-mailbox 3.0.0` for
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

Fresh raw receipts in MAIN `ruby-mailbox-integration-20261119/`:
`post-producer-generate-canonical.log`, `post-producer-native.log`,
`post-producer-applicability.log`, `post-producer-coverage.log`,
`post-producer-rubocop-direct.log`, `post-producer-install.log`,
`post-producer-installed-proof.json`, `post-producer-installed-native.log`.
`python-stat-from-a326bc92.txt` is empty: `python/` is unchanged from
`a326bc923fff448470d908bb527afaaa35f6d739`.

## Origin and smallest change

Only the Mailbox generator branch changes. Other surfaces, management's
retained opaque payloads and its plain-string event labels are unchanged.
No runtime request, write, process or dependency was added.

Native version and the shared manifest now agree at `3.0.0`. Official
`bundle lock --local` updated only the Mailbox version and the SDK's
Mailbox requirement to `>= 3.0.0, < 4.0`. The SDK's own version is unchanged
for its later release. This local build is not an approved publication artifact.

## Native red and green

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

The rebuild after those packaged documentation changes is:
`qubrics-mailbox-3.0.0.gem`, **110,592 bytes**, SHA256
`1d014427f58ebbcb750858411a5287c3b6b1cf9e302acc2a53eeec06ce26ff78`.
Its absolute path is SDK MAIN
`.claude/artifacts/rebrand-qubrics-sdk344/ruby-mailbox-integration-20261119/qubrics-mailbox-3.0.0.gem`.
It supersedes the earlier provisional archive only for this local integration
proof. Neither archive has publication approval.

Focused dependency-floor and native release-guardrail checks passed.
RuboCop passed for all three applicable changed files under the existing
generated-file exclusions. Preliminary commands incorrectly omitted Ruby
load paths, explicitly selected excluded generated files, and invoked gem
build from the workspace root. Corrected invocation setup passed without
any source, assertion or lint-policy change. Those logs are retained.

### Advertised runtime capability correction

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
