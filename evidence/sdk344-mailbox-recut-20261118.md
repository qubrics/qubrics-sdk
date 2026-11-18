# Calendar-free Python Mailbox replacement candidate

PR380 prepares the unpublished PyPI `qubrics-mailbox 3.0.0` under operator
1A, 18 November. It does not authorise a release merge, tag, upload, registry
write or environment approval. The later combined ASK also covers the Rust
0.6.0 re-cut, crate identity and the Phase 1 public API contract.

## Qualified source

Source PR378 normally merged at
`7a0bf484344bb68fb9c8508e83e49c80c56cfaf1`, identical tree to independently
reviewed `9773d640714c78dad1c19bc646ee5bee099893c7`.
PR CI44259534505 and main CI44261234996 passed 34/34, zero skipped;
42/42 checks and the final review sweep were clean. Source Spec/Standards
reviews returned zero findings. The fresh default Skills v2.0.5 guard passed
all 22 results and live OpenAPI equality on9773d640. Its candidate digest is
`86ad95d5f5e46033497329ca23bde93632950145bca21024643f372771d2fcf2`.
No claim of exact acceptance for a later candidate is inherited from it.

The Ruby prerequisite PR379 normally merged at
`b272a770c8434e7a9743def964853a4f6712c806`; PR/main CI both34/34 green.
Only CI test workflows and native pins changed to the official vendor action
20eb24b0 / Ruby3.4.12. Release/publish/tag workflows were untouched.
The subsequent stale Python-calendar lifecycle expectation was corrected at
the matrix/runner capability contract: two red receipts, then27/27 focused
tests, all native/runtime main checks green. Full trace is in
`evidence/sdk344-calendar-free-20261118.md`.

## Replacement metadata

Official installed Release Please17.6.0 `Manifest.fromManifest` and
`createPullRequests` created PR380 at
`c15666a0ac68d597aea1f60b5a4be6827e29d452`, scoped only to
`packages/python/mailbox`, explicit releaseAs3.0.0. No persistent release-as
key or workflow changed, and `createReleases` was never called.
The only generated diff was the changelog; versions were already3.0.0.

Generated history repeated move announcements and calendar additions and
duplicated the unreleased3.0.0 section. Before publication, the section and
PR body are consolidated to the already-approved technical import and
calendar-free scope text. Historical2.0.2 and earlier notes remain intact.
The two retained sentences reuse the source PR's completed polish pass,
with their technical terms/claims unchanged. No runtime/package source or
dependency version changes accompany this prose correction.

## Receipts and limits

Raw logs live in SDK MAIN `.claude/artifacts/rebrand-qubrics-sdk344/`:
`mailbox-release-pr-prepare.log`, `pr380-created.json`,
`pr378-main-ci-watch.log`, and `calendar-free-9773d640-default/`.
This file is the source qualification handover before source-worktree removal.
Final candidate native/package/default/CI results and exact artifact hashes
are not claimed by this checkpoint; the combined publication packet must
measure them before asking for GO.

Rollback before publication: close the unmerged replacement PR, or normal
revert after an explicitly authorised merge. No public version can be reused;
PyPI yank is withdrawal rather than a full rollback and needs named GO.
Sending's existing environment hold remains operator-deferred and is not
re-requested. Obsolete PR330/PR326 remain non-pending; old Rust run stays
cancelled. No public release or package was created during preparation.
