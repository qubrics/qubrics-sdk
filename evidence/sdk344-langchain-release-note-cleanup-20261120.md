# LangChain 1 release-note cleanup

The LangChain 1.0.0 candidate changelog replaces two announcement lines
with `update native package imports`, retaining the breaking-change
heading and original commit link. Package versions, dependency floors,
manifest entries and runtime source match parent PR355 head
`905273fa908bb403aa959127729b33146660f3e9` exactly.

This source PR targets
`release-please--branches--main--components--python-langchain`, leaving
the parent body, labels and merge state untouched.

Commit `a326bc923fff448470d908bb527afaaa35f6d739` still supplies the
historical generator input. The separate
[SDK source cleanup](https://github.com/qubrics/qubrics-sdk/pull/412)
records why a historical PR370 body override is unsuitable: actual
three-association replay duplicates Python notes and adds an unrelated
Go breaking entry. No historical PR body was edited.

The cleanup stays provisional. Until the exact source is merged under
the separately controlled parent release-PR disposition, a later bot
refresh can overwrite these lines from the historical commit. Workflow
and release configuration remain unchanged.

Publication stays held. Parent PR355 merging, pending-label disposition,
matching release-body cleanup and merged-main proof remain gates. Qualify
the exact candidate files and request separate publication approval before
any upload.

Receipts remain in the source PR and
`/Users/rj/Desktop/GIT-REPOS/sendmux-sdk/.claude/artifacts/rebrand-qubrics-sdk344/pypi1041-source-20261120/`.
