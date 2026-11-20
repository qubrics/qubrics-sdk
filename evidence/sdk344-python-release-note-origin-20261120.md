# Python SDK 4 release-note cleanup

The SDK 4.0.0 candidate changelog replaces two announcement lines with
`update native package imports`, retaining the breaking-change heading
and original commit link. Native metadata is unchanged. Package versions,
dependency floors, manifest entries and runtime source match parent
PR358 head `e3f041d9fa401000c1ecf389a4a3a4281206f285` exactly.

The source PR targets
`release-please--branches--main--components--python-sdk`, leaving the
parent body, labels and merge state untouched.

Commit `a326bc923fff448470d908bb527afaaa35f6d739` generates the original
announcement, and the pinned constructor's
[plain-merge warning](https://github.com/googleapis/release-please/blob/v17.6.0/README.md#how-can-i-fix-release-notes)
applies to PR370 because the history adapter associates it with the
original commit and two merge commits. A read-only three-association
replay confirms that a historical body override produces duplicate Python
notes and an unrelated Go breaking entry. No historical PR body was edited.

The cleanup stays provisional. Until the source is merged under the
separately controlled parent release-PR disposition, a later bot refresh
can overwrite the changelog from the historical commit. Workflow and
release configuration remain unchanged.

Publication stays held. Parent PR358 merging, pending-label disposition,
matching release-body cleanup and merged-main proof remain gates. The old
SDK sdist remains blocked. Rebuild and qualify replacement files before
requesting exact-file publication approval.

Qualification receipts are recorded in the source PR and retained under
`/Users/rj/Desktop/GIT-REPOS/sendmux-sdk/.claude/artifacts/rebrand-qubrics-sdk344/pypi1041-source-20261120/`.
