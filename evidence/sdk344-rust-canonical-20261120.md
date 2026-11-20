# Canonical Rust source qualification

Operator board 1A, 20 November 2026, approves canonical `qubrics 1.0.0`
source preparation and normal green merge under #344/#1041. It authorises
no crate upload, tag, release-workflow or queue action. The later silent
`sendmux 1.0.0` re-export waits for separately approved canonical publication
and passing public consumer evidence.

## Scope and retained contract

One existing umbrella crate; no new runtime layer or requests. Cargo name,
native version, independent floor consumer and release metadata agree on
`qubrics 1.0.0`. Sending defaults to smtp.qubrics.com/api/v1; Mailbox and
Management default to app.qubrics.com/api/v1. TLS, request validation,
error variants/fields, secret redaction, credential wire prefixes and
QUBRICS-over-SENDMUX environment precedence are retained. Only error display
words and user-agent identity change alongside the defaults/package name.

The existing public modules, clients, constructors, non-calendar methods,
raw JSON helpers, payloads and authentication APIs remain. No named
calendar endpoint, schema or client is introduced. Raw producer snapshots
and operation decisions retain truthful withheld-operation accounting and
are outside the Cargo archive include list.

## Red and green

Added one existing-seam public contract test, `default_hosts_use_qubrics`.
It compiled against the old crate before changing any host. Native result:

```text
assertion `left == right` failed
 left: ["https://app.sendmux.ai/api/v1", "https://app.sendmux.ai/api/v1", "https://smtp.sendmux.ai/api/v1"]
right: ["https://app.qubrics.com/api/v1", "https://app.qubrics.com/api/v1", "https://smtp.qubrics.com/api/v1"]
test result: FAILED. 0 passed; 1 failed
```

Origin is the three public DEFAULT_BASE_URL constants. Updating those
constants passed the same test; the canonical-name checkout also passes.
No assertion was weakened. Existing tests retain their assertions and
only change crate imports. No test or harness was removed or added beyond
this one promised-behaviour regression.

Focused native release-state checker passed. Four existing Rust negative
release fixtures passed with zero failures/skips, preserving version,
ownership and independent-floor-lock enforcement. Surface coverage passed
for all 128 producer operations. Formatting and diff whitespace passed.
Full native floor/stable/package consumer and required CI remain the
normal PR gates; these local results do not claim those future results.

Independent spec review found the README's inherited count of 30 named
operations unsupported; corrected to the measured 20 of 128. Standards
review traced stale provenance PATH constants to the existing writer,
which updated hashes without paths. The ordinary gate rejected both
surfaces with `Rust openapi-app.json provenance path drift` and
`Rust openapi-sending.json provenance path drift` before regeneration.
The existing writer now emits and checks canonical repository-relative
paths. Regeneration changed only the two exported PATH values, retaining
their names/types, both hashes and every operation constant.

Extended the existing provenance fixture to seed both stale paths while
retaining the metadata-only hash-change case. With the path writer fix
absent, it failed with actual `sendmux_mcp/openapi` versus expected
`qubrics/mcp/openapi` paths (exit 1). Restoring the origin fix passed all
three existing surface/provenance tests, zero failures or skips. Final
surface, native release-state, Rust release-fixture, syntax and Rust fmt
checks passed. Standards follow-up reports zero findings.

Copy received independent critique, one humanize pass and protected-set
check. Package/version names, URLs, credentials, API identifiers, examples
and source counts are retained. Changes describe current behaviour and
make no move announcement. Local fast gate is composed from the focused
checks above because this repository has no `check:fast` script; full
floor/stable/package suites stay in the existing CI jobs.

## Evidence and pending publication gate

Raw command logs live in SDK MAIN
`.claude/artifacts/rebrand-qubrics-sdk344/rust-canonical-20261120/`:
`default-hosts-red.log` (failure lines 106–108), `default-hosts-green.log`,
`canonical-hosts-green.log`, `release-state.log`,
`rust-release-fixtures.log`, `surface-coverage.log`, `pnpm-install.log`.
Review fix logs: `provenance-path-red.log`, `provenance-write.log`,
`provenance-path-green.log`, `provenance-writer-red.log`,
`provenance-tests-green.log`, `release-state-final.log` and
`rust-release-fixtures-final.log`. Review dispositions: `spec-review.md`
and `standards-review.md` in the same raw directory.

Automated PR review found an additional path/hash pairing escape: a
different `OPENAPI_INPUT_DIR` could supply bytes unlike the canonical
repository file whose path was recorded. The original fixture copied no
repository snapshot, so it tested hashes without proving that pairing.
A new case in the existing fixture failed pre-fix with
`provenance accepted different repository snapshot bytes` (exit 1).
The shared loader now compares actual canonical-file bytes with the input
in both check and writer modes, rejecting mismatch before any writes.
Fixtures carry the repository snapshots as well as inputs, matching the
real MCP-generation sequence. All four tests pass, zero skips, including
atomic refusal in both modes and the original route/pin protections.
The real docs checkout and SDK snapshots have identical current hashes.
Logs: `provenance-bytes-red.log`, `provenance-bytes-green.log`,
`surface-final.log`. The first PR head's CI passed 35/35; the review-fix
head still requires its own exact-source checks and publication archive.

Exact candidate/default Skills receipt, independent review, PR/main CI,
actual archive filename/bytes/SHA and archive inspection will be recorded
when measured. No package is claimed public by this source PR. Root README
distinguishes public `sendmux 0.5.1` from prepared `qubrics 1.0.0` source.
Public text contains no move announcement; historical changelog entries
remain historical. Rollback before publication is a normal PR revert.

Release Please's existing multi-source pending-record failure remains
separately held; this PR does not change its labels, refs, jobs or policy.
Published historical versions remain unchanged. App/gateway calendar
endpoint removal remains behind its infrastructure gate.
