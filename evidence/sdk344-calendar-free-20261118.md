# Calendar-free Python Mailbox and Rust candidates

Operator 1A, 18 November 2026, authorises re-cutting the unpublished PyPI
`qubrics-mailbox 3.0.0` and crates.io `sendmux 0.6.0` without calendar-specific
client code. No tag, upload, registry mutation or environment approval is
authorised by this source change. Other #344 releases stay held.

## Release safety

Before any source merge, the obsolete merged PR330's `autorelease: pending`
label was removed. GitHub REST readback returned `labels: []`; old Rust run
43317298621 remains `completed/cancelled`. PR326 is also not pending. Neither
old merge source may be relabelled or resumed to release calendar code.
Replacement release PRs must be prepared sequentially and stay unmerged until
the exact-source/file/hash publication decision permits tags.

The existing Sending run 42983124898 remains operator-owned and deferred.
This change does not approve, cancel or re-ask its environment step.

## Source correction and tests

Canonical per SDK local AGENTS.md: change generated clients at the generator,
then regenerate. `scripts/generate-python.mjs` excludes `/mailbox/calendars`
and `/mailbox/calendar-events` before existing component reachability pruning.
Raw OpenAPI inputs and the live API are unchanged. Ten operations and their
unreachable models disappear; all 53 other Mailbox operations remain.
An AST comparison against b98681f1 reports 40 removed calendar methods and
variants, 213 retained methods, zero changed retained method bodies.

`test_environment.py::test_mailbox_withholds_calendar_bindings_and_preserves_mail_clients`
was red before the filter: `AssertionError: assert not
['_mailbox_create_calendar_event_serialize', ...]`. After regeneration the
environment file passes 14/14. The test checks the imported API/model exports
and retained mail/folder/draft methods. Existing runtime tests cover requests,
auth, defaults and streams.

Rust removes 12 calendar methods, three path helpers, their only transport
helper and ten named-operation constants. The ten coverage decisions become
honest `raw-json-only` entries. Generic raw HTTP access and non-calendar
clients retain auth, retry and validation. The calendar-only lifecycle test
is removed because the operator explicitly withheld that feature. Its
adjacent mail/cursor/auth/path tests remain.

`named_mailbox_surface_withholds_calendar_bindings` was red before removal
(exit 101), then public-contract tests pass 7/7, zero ignored. The existing
coverage writer/check passes for all 128 snapshot operations. Cargo dry-run
passes and explicitly aborts upload. Archive inspection found 13 members,
six Rust sources and zero calendar source matches. The provisional archive
predates final prose and is not a publish-approved hash.

## Qualification boundaries

Operator ruling, 18 November 2026: only the docs changelog announces the
brand move. A18's Ruby post-install deprecation message is cancelled by the
operator. All five pointer gemspecs now have no `post_install_message`.
Seven Python pointers retain replacement dependencies and Inactive metadata,
with neutral descriptions and no executable install hook. Pointer versions
and dependency bounds are unchanged. The native Ruby metadata check was red
with `Unexpected install message: sendmux-core`, then green for all five.
The Mailbox release notes use the import instruction without a move
announcement. Already-published immutable package bytes are not replaced.

Fresh native Python build/dists check exits 0. Its source cohorts, installed
MCP artifact check and Twine checks run through existing repo commands. Final
candidate SHA, exact-head CI, default Skills acceptance, final archive hashes
and clean artifact installs must be recorded before the publish ASK.

Independent Spec review: zero findings. Independent Standards review: zero
findings. Fresh-reader prose critique corrected the Rust semicolon. One
humanize pass retained the short factual wording and protected versions,
calendar exclusions, mail functionality and generic raw JSON claims. Final
changed prose has zero em dashes, semicolons, curly quotes or banned terms.

Rust remains named `sendmux` with legacy default hosts. A18 names no Rust
replacement. Naming options, fresh crates.io availability and Phase 1 API
compatibility citations belong to the final combined publication ASK, not an
invented rename in this source PR.

## Receipts and undo

Machine-local raw outputs retained in SDK MAIN
`.claude/artifacts/rebrand-qubrics-sdk344/`:

- `calendar-free-python-{red,green,generate,dists,selector}.log`
- `calendar-free-rust-{red,green,coverage,package,package-inspection}.log`
- `calendar-free-canary.log`
- `pointers-{silent-red,silent-green,python-silent}.log`

Source rollback is a normal revert. Keep calendar publication held through
any revert. Public registry versions cannot be overwritten or reused, and
yank would be withdrawal only; no publication or yank occurred here.
