# Rust sendmux 1.0.0 pointer source

Goal: qualify the silent `sendmux 1.0.0` source pointer for normal review
and a root-coordinated merge. Publication requires its own exact-file
approval. This source change performs no registry upload, tag, release
workflow, queue or environment mutation.

## Public API and dependency

The package depends on public `qubrics = "=1.0.0"` and contains only
`pub use qubrics::*;` in its runtime source. Rust 1.82 and the canonical
MIT licence are retained. Constructors, factories, clients and request
types remain the canonical public types, with no copied implementation,
build script, warning or move announcement.

Canonical public bytes were independently verified before this source
work: `qubrics-1.0.0.crate`, 25,962 bytes, SHA-256
`707d4cd9e5fe26dbe4a6f53077c1553c15a9b778e44d0540e11925e5b1e4176b`.
The pointer's native lock records that crates.io checksum and source.
Root README now identifies that public crate and marks the pointer source
as unpublished.

## Public regression

`tests/type_identity.rs:public_types_and_constructors_are_identical`
assigns clients, addresses, attachments and sending requests between
`sendmux::` and `qubrics::`, calls all three constructors and factories,
and retains both attachment constructors. It makes no authenticated
request. Removing the re-export makes the public integration test fail.

Before the implementation, the Rust 1.82 command exited 101:

```text
error[E0432]: unresolved import `sendmux::sending`
error[E0432]: unresolved imports `sendmux::MailboxClient`, `sendmux::ManagementClient`, `sendmux::SendingClient`
error[E0425]: cannot find function `sending` in crate `sendmux`
error[E0425]: cannot find function `mailbox` in crate `sendmux`
error[E0425]: cannot find function `management` in crate `sendmux`
```

After the one-line re-export, both `cargo +1.82.0 test --locked` and
`cargo +stable test --locked`, restricted to `--test type_identity`,
exit 0: one test passed, zero failed or ignored on each toolchain.
No existing assertion was changed or removed.

## Native lock resolution

An initial unbounded Cargo 1.82 resolution selected `idna_adapter 1.2.2`,
which requires edition 2024. Cargo's documented stable `fallback`
resolver then selected packages claiming Rust 1.82 whose transitive
minimum is incompatible: `potential_utf 0.1.6` requires `zerovec ^0.11.7`,
`tinystr 0.8.5` requires `^0.11.9`, and `zerotrie 0.2.5` requires
`^0.11.7`. Public registry metadata marks `zerovec 0.11.6` and later as
Rust 1.83. This explains the second setup failure before test compilation.

The actual public canonical archive and its independently proven floor
consumer use compatible versions. The pointer lock was independently
resolved with native Cargo, without copying either lock, changing the
manifest dependency, mocking a registry or suppressing verification:

```sh
CARGO_RESOLVER_INCOMPATIBLE_RUST_VERSIONS=fallback cargo +stable generate-lockfile --manifest-path release-pointers/cratesio/sendmux/Cargo.toml
CARGO_RESOLVER_INCOMPATIBLE_RUST_VERSIONS=fallback cargo +stable update --manifest-path release-pointers/cratesio/sendmux/Cargo.toml -p potential_utf --precise 0.1.4
CARGO_RESOLVER_INCOMPATIBLE_RUST_VERSIONS=fallback cargo +stable update --manifest-path release-pointers/cratesio/sendmux/Cargo.toml -p tinystr --precise 0.8.2
CARGO_RESOLVER_INCOMPATIBLE_RUST_VERSIONS=fallback cargo +stable update --manifest-path release-pointers/cratesio/sendmux/Cargo.toml -p zerotrie --precise 0.2.3
CARGO_RESOLVER_INCOMPATIBLE_RUST_VERSIONS=fallback cargo +stable update --manifest-path release-pointers/cratesio/sendmux/Cargo.toml -p zerovec --precise 0.11.5
CARGO_RESOLVER_INCOMPATIBLE_RUST_VERSIONS=fallback cargo +stable update --manifest-path release-pointers/cratesio/sendmux/Cargo.toml -p zerovec-derive --precise 0.11.6
```

Cargo documents [Rust-version resolution](https://doc.rust-lang.org/cargo/reference/resolver.html#rust-version)
and native [`update --precise`](https://doc.rust-lang.org/cargo/commands/cargo-update.html).
These are lock-only selections of public unyanked packages.

## Existing verification path

The existing Rust package consumer's commands and assertions remain
unchanged. Its extension formats, lints, tests and packages the pointer
on stable, then extracts the actual pointer archive and runs its public
integration test and doctest command on Rust 1.82. The real registry
dependency is used throughout. No mock, path replacement, `[patch]` or
`--no-verify` is introduced.

Local related checks passed: native release-state and fixtures 41/41,
Rust surface/provenance regressions 4/4, surface coverage for 128 OpenAPI
operations, pointer Rust formatting, JavaScript syntax and diff whitespace.
Full CI owns the existing stable canonical package/independent floor
consumer path and the added pointer archive path.

The README received the required fresh-reader critique, one humanize
pass and protected-set check. Factual reference copy passed unchanged.
The exact docs.rs API URL returned successfully. Package notes contain
no move announcement.

## Scope and receipts

Runtime footprint: one compile-time re-export, no additional process,
durable write, transport or output. Dependency direction is one-way to
the canonical crate. Design diagnostics: clean architecture 10/10,
software design 9/10 (the explicitly requested shallow compatibility
surface), clean code 9/10 (existing CI function shape retained), technical
documentation 10/10. No speculative abstraction was added.

Raw local receipts are under MAIN
`.claude/artifacts/rebrand-qubrics-sdk344/rust-pointer-20261120/`:
`type-identity-red.log`, `type-identity-green-floor.log`,
`type-identity-green-stable.log`, `floor-setup-fallback-failure.log`,
`floor-lock.log`, `lock-*.log`, `zerovec-trace.log`, `release-state.log`,
`rust-surface-test.log`, `surface-coverage.log` and `docs-rs.html`.
Exact-head archive, default Skills acceptance and PR CI receipts bind
their actual candidate commit separately. The merged source will require
fresh exact-merge qualification before any publication ASK.

Status: coded, not merged or published. Root owns the merge window and
publication decision. Existing canonical and historical package bytes
remain unchanged. Parked: adding a general `check:fast` entry is outside
this pointer scope; this repo uses its existing focused checks and CI.
