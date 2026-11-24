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
claim of name ownership/reservation.
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

## Qualification after deployed-producer sync

Docs75's joint receipt proves SMTP v1.2.128 and App v1.8.363 live and equal
to docs main `0775e2f21428b215165fd25a0bf1894dcf339d46`. Existing generators
consumed those exact emitted inputs in producer-sync commit `c8549be2`.
See `evidence/sdk344-producer-sync-20261119.md`. The normal PR385 CI on
that commit completed **34/34 successful jobs, zero skipped jobs** in run
`44483116772`; no rerun, pin, fallback or workflow change was used.
Independent source reviews found zero Spec defects and one Standards
documentation defect: the root Ruby table now says “Target version” to
avoid presenting unpublished majors as current native source versions.
That one-label fix is `6a9e8dde`; no packaged Sending file changes with it.

Rebuilt exact files supersede the earlier frozen table above:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| qubrics-sending-2.0.0.gem | 36,352 | `8dd5350aebf55dd588cc2c350dc906c3bb635f608b20dc7f71f0774455bee462` |
| sendmux-sending-2.0.0.gem | 4,096 | `fc1ad0170f578ddfeb5156c5c5a893f0bfa5d029a45f082ec11b02ffddc02c6f` |

The unchanged default selector resolves reviewed Skills v2.0.5 at
`05e24366cebc2caf2b5c395727414e634ba7bf8c`; release receipt binding passes.
The live OpenAPI stage passes, but exact-source compatibility fails on
new producer contract fingerprints. Fifteen of 22 pairs need Skills-origin
review evidence. First failure: `published/email-for-ai-agents` contract
`f81288de22ec063dabed513a35ae2898641de1517a3ca321ab2eb02b0ce9b9f6`.
`producer-sync-skills-origin-20261119.md` in MAIN task state routes the
origin to the Skills owner. No guard override or unchanged-input retry.
Fresh exact-candidate default acceptance and Sending PR CI remain gates.
The gem may remain unpublished.
No merge, upload, tag, queue or environment action is authorised here.

## Default gate cleared and source refresh

On 19 November 2026 the Skills owner published reviewed v2.0.6 at
`9e2659c9dba3efd943190f2541016d0548db7201`. The unchanged default selection
downloaded its sole actual acceptance asset, whose SHA256 is
`809a7d4378fb08eed5a0ecd16b59448dc6aebb31c7c6a144e5e29ed7949543c6`.
Official release-receipt binding passed. Fresh exact Sending candidate
`729ae54ac9b78926f7a32732ddf939bee6795f8b` then passed live equality and
all 22 results, digest
`a95d06d1568b98008bede98c6835b3dae30c9ffe54058e25ae355e2bf363316f`.
Logs/receipts are in MAIN artifacts `default-v206-b25a7cbc/sending-guard.log`
and `default-v206-sending/receipts/`. No pin, fallback or same-input retry.
Normal exact-head CI `44485864018` also completed successfully.

After authorised parent PR385 reached main as `1a833169`, this source
normally merges that main commit without a force-push. It gains the approved
checksum-verified CI cache and its measured evidence. Packaged Sending
source and metadata remain byte-identical to `729ae54a`; the frozen gem
remains 36,352 bytes with SHA256 `8dd5350a…bee462`. Fresh default acceptance,
normal exact-head CI and review on the resulting successor remain required.
No exact-file publication approval exists.
