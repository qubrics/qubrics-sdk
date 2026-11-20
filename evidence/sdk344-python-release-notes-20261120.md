# Pending Python release-note producer correction

Prepared under the away adviser's option A, 20 November 2026. This PR is
source preparation only. Merge and activation require the operator's morning
decision. No release PR, tag, public file, label or registry was changed.

## Cause and scope

PR358 at `36108a03109ec8eeb329b71e41f95aa6c746483c` and PR355 at
`47955f81a0782507749775bf114812ff3b3ce486` regenerated the historical
`a326bc923fff448470d908bb527afaaa35f6d739` summary in their breaking-change
and feature sections. The source-child edits in PR412 and PR413 did not
survive the next bot refresh. The operator permits the move announcement
only in the docs changelog; pending SDK release notes use the approved
technical wording, `update native package imports`.

Canonical extension: Release Please's documented `ManifestPlugin.run`
post-processes generated candidates before `Manifest.createPullRequests`
emits them. The existing action's documented `skip-github-pull-request`
input separates PR creation from release creation:

- https://github.com/googleapis/release-please/blob/v17.6.0/docs/manifest-releaser.md#plugins
- https://github.com/googleapis/release-please/blob/v17.6.0/src/manifest.ts
- https://github.com/googleapis/release-please-action/blob/0dfd8538845b8e92600d271a895a5372865d4062/src/index.ts
- https://github.com/googleapis/release-please-action/blob/0dfd8538845b8e92600d271a895a5372865d4062/README.md

The helper uses the already locked official `release-please` 17.6.0.
The pinned action declares `release-please: ^17.6.0`. No new dependency,
fork, vendor edit, history rewrite or ineffective plain-merge commit
override is used.

Only SDK 4.0.0 and LangChain 1.0.0 candidates change. Their generated
changelog entry and matching PR-body notes receive the same replacement;
historical changelog content is left to the official updater. Versions,
breaking headings, links, native metadata and all other notes stay intact.
Other versions and components pass through unchanged. The helper fails if
a selected candidate lacks the official changelog updater.

The pinned action still creates releases and supplies the same release
outputs. Existing preflight and actual-tag verification remain unchanged.
After verification, the helper performs the normal official pending-PR
construction, labels and update lifecycle, with the plugin installed.
There is no separate branch-write implementation. Workflow execution is
still restricted to main pushes; no workflow dispatch or PR event is added.
The helper rejects direct execution outside that repository's main-push
Actions context. This PR has not activated that path.

## Verification

Focused regression first failed with the identity plugin:
`AssertionError: candidate 0 body must preserve neutral release notes`.
The same case then passed with the correction. It exercises actual
`PullRequestBody`, `Version` and `Changelog` objects, including historical
content, matching body/file output, unrelated path/version boundaries,
header/footer/extra preservation and idempotence.

The existing CI command `pnpm test:release-state` includes the changed test:
42 tests passed, zero failures, zero skipped. YAML parsing, JavaScript
syntax and `git diff --check` passed. No full build was repeated locally;
normal PR CI supplies the broader gates.

An offline replay of the archived official constructor output processed
18 candidates: exactly two changed, 16 unchanged, all versions preserved,
second pass identical. Comparison checked the complete serialised bodies
and each generated changelog entry against the original input with only
the approved literal replacement. This is a captured-input proof, not a
claim that a live bot refresh has run.

Raw logs under MAIN `.claude/artifacts/rebrand-qubrics-sdk344/`:

- `python-note-producer-red-20261120.log`
- `python-note-producer-green-20261120.log`
- `python-note-producer-release-state-20261120.log`
- `python-note-producer-replay-20261120.log`
- Original `pypi1041-source-20261120/before-candidates.json`

README public-facts check found the newly public Rust pointer still
described as source-only. That pre-existing documentation row is outside
this calendar/copy producer scope and remains a follow-up.

## Status and undo

Prepared, not merged or activated. PR CI and review results are recorded
in the task's `python-release-note-producer-qualification-20261120.md`.
Undo: revert this branch commit. After a separately approved activation,
a revert restores the former producer; it cannot retract existing public
versions. The four held PyPI versions, release PR merges, tags, queue and
registry operations retain their separate gates.
