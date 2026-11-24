# Rust crate name and version plan

For the operator's #1041 decision, measured 20 November 2026, 13:51 AEDT.
This packet proposes names and versions only. It authorises no source
implementation, package upload, yank, tag, environment or release-queue
change. `sendmux 0.6.0` remains held.

The strongest alternative is B: use **3.0.0** for both crates to match the
Ruby umbrella SDK. It provides familiar numbering, but no extra API
compatibility: SDK majors already differ across languages and surfaces.

## Options considered

| Choice | Proposed crates.io publications, in order | Consequence |
| --- | --- | --- |
| **A — recommended and selected** | `qubrics 1.0.0`, then `sendmux 1.0.0` | One canonical implementation, one silent compatibility crate. Establishes the first stable Rust API without suggesting two previous Qubrics Rust majors existed. |
| B | `qubrics 3.0.0`, then `sendmux 3.0.0` | Same implementation and compatibility shape, with deliberate version alignment to Ruby SDK 3.0.0. Skipping version numbers is a product choice, not a Cargo requirement. |
| C | `qubrics-sdk 1.0.0`, then `sendmux 1.0.0` | Same shape with a longer distribution name; Rust normally imports `qubrics_sdk`. Available as a naming alternative if the operator prefers the explicit SDK suffix. |

The operator selected A. B and C remain here as considered alternatives,
not pending questions. Implementation and eventual exact-file publication
return through separate scope, CI, review and operator gates. The
`sendmux 0.6.0` hold remains unchanged. Only this evidence document and
its issue comment are authorised by the follow-on instruction.

Keeping `sendmux` as the only implementation does not satisfy #1041's
Qubrics-name decision. Maintaining two full implementation crates adds
duplicate release and compatibility work without adding a requested API;
the proposed old-name crate forwards to the same implementation instead.
Splitting Core, Sending, Mailbox and Management into separately published
Rust crates is unnecessary for the existing single-crate public surface.

## Registry facts measured read-only

| Request | Result | What it proves |
| --- | --- | --- |
| [sendmux metadata](https://crates.io/api/v1/crates/sendmux) | HTTP 200; latest/newest `0.5.1`; versions `0.1.0`, `0.2.0`, `0.3.0`, `0.4.0`, `0.5.0`, `0.5.1`, all unyanked | No `0.6.0`, `1.0.0` or `3.0.0` appears in the complete returned version list. Existing bytes remain untouched. |
| [sendmux owners](https://crates.io/api/v1/crates/sendmux/owners) | HTTP 200; sole returned owner `roshanjonah`, user ID `425403` | Public ownership of the existing crate; it does not prove current credentials or publish permission. |
| [qubrics metadata](https://crates.io/api/v1/crates/qubrics) | HTTP 404; `crate qubrics does not exist` | Name unregistered when measured, not reserved or owned by us. |
| [qubrics-sdk metadata](https://crates.io/api/v1/crates/qubrics-sdk) | HTTP 404; `crate qubrics-sdk does not exist` | Alternative name unregistered when measured, not reserved or owned by us. |

No name was reserved and no credential was read. Cargo documents names as
[first come, first served](https://doc.rust-lang.org/cargo/reference/publishing.html#before-your-first-publish).
Recheck name availability and ownership at a future approved publication
gate; a third party can take either unregistered name meanwhile.

Raw JSON and response headers are in MAIN
`.claude/artifacts/rebrand-qubrics-sdk344/rust-name-plan-20261120/`:
`sendmux`, `sendmux-owners`, `qubrics`, `qubrics-sdk`. The saved official
Cargo pages are `publishing.html`, `dependencies.html`, `semver.html` and
`manifest.html`. The HTTP headers retain the server response dates.

## Why 1.0.0 rather than automatically 3.0.0

The current public Rust line is `sendmux 0.5.1`. Source metadata still says
`sendmux 0.6.0` at
[`rust/Cargo.toml:2`](../rust/Cargo.toml#L2); that source version is held,
not a crates.io release. Operator 7A in
[#1041](https://github.com/qubrics/qubrics/issues/1041) explicitly forbids
releasing it until this naming/version decision is settled.

Cargo's [default version requirements](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html#default-requirements)
use the leftmost non-zero component for compatibility. A normal `"0.5.1"`
requirement selects `>=0.5.1, <0.6.0`; even `"0"` stays below `1.0.0`.
Neither proposed final pointer version silently moves those pinned users.
Consumers must intentionally select the stable-major release. Unbounded
requirements such as `"*"` do not have that protection.

The existing source already has independent version lines: Ruby SDK
[`3.0.0`](../packages/ruby/sdk/lib/qubrics/sdk/version.rb#L5), Ruby Core
[`2.0.0`](../packages/ruby/core/lib/qubrics/core/version.rb#L5), Python
Mailbox [`3.0.0`](../packages/python/mailbox/pyproject.toml#L7), and the
pending [Go module `/v4`](../go/go.mod#L1). Therefore choosing Rust 3.0.0
would align a label with Ruby, not prove equivalent APIs or a common
compatibility boundary. Choose B only if that alignment is itself wanted.

## Legacy compatibility and bounded implementation plan

The recommendation preserves the current umbrella shape. Its existing
public modules are `core`, `generated`, `mailbox`, `management` and
`sending`, plus the client types and constructor functions exported by
[`rust/src/lib.rs:3`](../rust/src/lib.rs#L3). No per-surface Rust packages
are proposed.

After a separately approved source scope, rename the one implementation
package, lockfile, native metadata and affected Cargo callers/tests to the
chosen identity. Update the Rust package README and root Packages table with factual installation examples;
add no announcement, warning, compiler deprecation or post-install message.
Update the native release configuration only through that agreed source
PR, preserving the current publication and tag holds.

The silent old-name crate would depend on the chosen Qubrics crate's exact
initial version and re-export its public API, rather than copy clients or
convert their types. For A, the proposed dependency is
`qubrics = "=1.0.0"` and the public forwarding statement is
`pub use qubrics::*;`. For B, its dependency version becomes `=3.0.0`.
For C, the dependency can use Cargo's documented
[`package` rename](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html#renaming-dependencies-in-cargotoml)
so the same forwarding shape uses the `qubrics-sdk` distribution.
This is a package implementation to qualify later, not a registry alias.

Existing callers can instead change their dependency declaration to
`sendmux = { package = "qubrics", version = "1" }` under A, preserving
the `sendmux::` import spelling without taking the pointer crate. This is
an opt-in Cargo dependency alias, not an in-place registry rename.

## Readiness

## Undo and limits

Before publication, source and release-config changes can be reverted
normally; there are no such edits in this proposal. Choosing a different
plan now changes prose only.
