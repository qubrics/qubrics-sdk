# Ruby Sending 2.0.0 qualification

Current-main successor of stale release PR331 for #344 A18. Base is
`e8d46fa2f91ece4ebab28c7e8ca51e6f1d53b5fa`. This preparation authorises no
main merge, upload, tag, release-queue or environment action.

## Cause and source correction

PR331 at `f8c3dd3f04d5e082e8f7924036dffd46574b8c33` conflicts with current
main and still requires Core `>=1.3.0,<2.0`. Main already fixed Sending's
native Core requirement to `>=2.0.0,<3.0` in PR384. This successor preserves
that fix, every unrelated manifest entry and all generated Sending runtime.
Only Sending's native version and manifest entry advance to the specified
2.0.0. The dependent SDK's Sending requirement advances to `>=2.0.0,<3.0`
so the monorepo can resolve the candidate. The SDK itself remains unpublished.

Canonical per SDK AGENTS.md release rules: language-native versions,
dependency floors and committed lockfile must agree. Official
`RBENV_VERSION=3.4.1 rbenv exec bundle lock --local` exits 0 and changes only
Sending's version and the SDK dependency row. It preserves the CI Ruby
3.4.12 requirement and all other lock entries. The first invocation without
the local interpreter selector found 3.4.12 absent on this Mac; no machine
Ruby installation or runtime requirement change was made.

New release text is neutral. It states the Core 2.x/Ruby 3.1 requirements and
retains the existing delivery-group feature entry. The packaged README's
temporary unpublished-install paragraph is removed. No move announcement,
post-install message, generator logic, test or workflow changes are added.

## Native and exact-package proof

Existing Ruby release guardrails exit 0. A fresh isolated GEM_HOME/GEM_PATH
installs the exact replacement gem and public Core 2.0.0, then its silent
pointer. Existing Core, environment and OAuth/retry tests execute with
Sending loaded from the installed artifact: **30 tests, 213 assertions,
zero failures, errors or skips**. Mailbox/Management/SDK are source fixtures
for these existing cross-surface tests; those fixtures are not packaged.

All 44 archive files, including 41 runtime Ruby files, match source and
installed bytes. Public installed Core's cached archive matches approved
SHA256 `736fd1ed4c613f8dfe5c2cc4f81741c5e42f18bb19dd44aeffd4163b71971e79`.
Native dependencies resolve. Import/version, canonical homepage and default
`https://smtp.qubrics.com/api/v1` pass. Runtime paths and contents contain
zero calendar matches. The pointer has zero files/extensions, nil
post-install message and exactly the intended replacement dependency.

The provenance command's initial `gem/package` require typo was corrected
to RubyGems' `rubygems/package`; the corrected read-only assertion exits 0.
No application source, assertion or test was altered to obtain the proof.

Fresh-reader metadata critique passes Truth, with all other metadata rubric
rows N/A. One humanize pass leaves the factual entry unchanged: em dashes,
semicolons, curly quotes, banned words, comparative and negation framing
all 0. Protected `qubrics-core`, 2.x, Ruby 3.1, 2.0.0 and `delivery_group`
remain exact. No announcement is present.

## Frozen files, not approved for publication

Files live under SDK MAIN
`.claude/artifacts/rebrand-qubrics-sdk344/ruby-sending-qualification-20261119/gems/`.

| Registry | File | Bytes | SHA256 |
| --- | --- | ---: | --- |
| RubyGems | qubrics-sending-2.0.0.gem | 36,352 | `1223c7da331411a2459805248062a8dc2b92c9becd4c5159d8dee15387e8d00c` |
| RubyGems | sendmux-sending-2.0.0.gem | 4,096 | `81a26c3c44eae8575900376c3795aba455e615fd992d8a01ede296ed060766c5` |

Both exact-version RubyGems APIs returned 404 at qualification. This is no
claim of name ownership/reservation. Calendar exposure for both is **NO**.
Holding them unpublished remains the alternative. The operator requested
asks in order: Sending replacement, Mailbox, SDK, then pointers; qualifying
the pointer here does not grant permission or move it earlier in that order.

Raw native/build/install/provenance logs are under MAIN
`.claude/artifacts/rebrand-qubrics-sdk344/`, prefixed `ruby-sending-` and
suffixed `-20261119.log`. Registry responses are
`ruby-sending-{qubrics,sendmux}-version-20261119.json`.

Exact-head CI, default Skills acceptance and independent review remain
required; this pre-commit evidence does not claim they have completed.
Source undo is a normal revert. Published RubyGems versions cannot be
overwritten or reused. A separately authorised yank limits new resolution
but cannot recall downloads or provide a full rollback. No agent upload.
