# Python package facts in the SDK README

Scope: README publication, installation and import facts for #344. Base is
`1449b51e1decd1fe6ebb17d203e726363002f0f8`. No runtime, package metadata,
generator, dependency, workflow, tag or registry change.

The package table names `qubrics-mailbox` and `qubrics-management` and uses
their direct install commands. The availability text lists their public
3.0.0 versions alongside `qubrics-core` and `qubrics-sending` 2.0.0. SDK,
MCP and LangChain replacement targets remain explicitly unpublished.

The Mailbox attachment example uses
`qubrics.mailbox.send_mailbox_message_with_files(...)`. Public Mailbox 3.0.0
exports that helper; the final old-name pointer supplies no legacy import.
The section title is neutral. No move announcement is added.

## Fact sources and verification

- Public version metadata: `https://pypi.org/pypi/qubrics-core/2.0.0/json`,
  `https://pypi.org/pypi/qubrics-sending/2.0.0/json`,
  `https://pypi.org/pypi/qubrics-mailbox/3.0.0/json`, and
  `https://pypi.org/pypi/qubrics-management/3.0.0/json`.
- Retained exact public-file and clean-consumer receipts in SDK MAIN task
  state: Core public receipt, `sending-public-20261111.md`,
  `sendmux-mailbox-pointer-public-20261119.md`, and
  `management-public-20261119.md`. These prove the published bytes, imports,
  versions, default hosts and dependency resolution. No unchanged consumer
  proof was rerun for this documentation edit.
- Read-only inspection of the retained public Mailbox wheel's
  `qubrics/mailbox/__init__.py` confirms the attachment helper export; exit0.
- `git diff --check`: exit0. No new tests: no runtime behaviour changes.
- Required fresh-reader polish critique: no failed applicable rubric rows.
  One humanize pass and protected-set check preserve names, versions, paths,
  auth prefixes and URLs. No detector or new release note.

Existing commit and PR CI gates remain required. Source prepared on an
isolated task worktree; this pre-commit record makes no merge or publication
claim. Public #344 tally remains 7/24; Ruby Management stays held on separately
approved/public Ruby Core 2.0.0. Source rollback is normal revert of this PR.
