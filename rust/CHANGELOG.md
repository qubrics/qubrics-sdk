# Changelog

## [0.6.0](https://github.com/qubrics/qubrics-sdk/compare/rust-v0.5.1...rust-v0.6.0) (2026-11-11)


### Features

* add compatible Qubrics integration aliases ([dff5cb8](https://github.com/qubrics/qubrics-sdk/commit/dff5cb89bccb5840d55071d23f79ff88c7e58040))
* **mailbox:** expose durable drafts and agent-email workflows ([bb2f462](https://github.com/qubrics/qubrics-sdk/commit/bb2f462447affd43b3b175b9625068f1a02e3172))
* **mailbox:** expose durable drafts and agent-email workflows ([7e867c5](https://github.com/qubrics/qubrics-sdk/commit/7e867c5bd7b7c85add27c7c04e036997ae57dbc4))
* **mailbox:** expose permitted sender choices to consumers ([#317](https://github.com/qubrics/qubrics-sdk/issues/317)) ([7ac3dc1](https://github.com/qubrics/qubrics-sdk/commit/7ac3dc1c08915ec12477171a49edb87b3d482f39))
* preserve integration contracts with Qubrics aliases ([722fbab](https://github.com/qubrics/qubrics-sdk/commit/722fbab2f98248d17b4878dd5149a35a711d5a18))
* **rust:** add named calendar operations ([1228b59](https://github.com/qubrics/qubrics-sdk/commit/1228b59b0cddf12062c6ea7da7a4b3dfdcbd3b86))
* **rust:** add named calendar operations ([8211d31](https://github.com/qubrics/qubrics-sdk/commit/8211d31a55206ba1ad64a5c27df7f8c7b87f8e85))


### Bug Fixes

* preserve webhook variants and own calendar lifecycle fixtures ([49d4604](https://github.com/qubrics/qubrics-sdk/commit/49d4604235528b2fd56ac0bb51d55c244a18f771))
* regenerate SDKs from current calendar and webhook contracts ([276082c](https://github.com/qubrics/qubrics-sdk/commit/276082cb5e525c0a6fb1e521858846cbd21c8714))
* regenerate SDKs from current calendar and webhook contracts ([d728ea8](https://github.com/qubrics/qubrics-sdk/commit/d728ea87ac3f0aeebdb6380ad3bd515bac63d413))
* sync generated Qubrics API defaults ([#351](https://github.com/qubrics/qubrics-sdk/issues/351)) ([388a410](https://github.com/qubrics/qubrics-sdk/commit/388a4107d25e6cf94a7c7704b094f8765f851be3))

## [0.5.1](https://github.com/Sendmux/sendmux-sdk/compare/rust-v0.5.0...rust-v0.5.1) (2026-09-21)


### Changed

* **OpenAPI provenance:** `sendmux::generated::APP_OPENAPI_SHA256` is now `b42ce87003ae8d4ac80024ce9796cd96db97c5439c5e99d957682f6b6a1f5999`, the SHA-256 of the app OpenAPI snapshot deployed as v1.8.250, instead of `09b00ae13c88fe4ecc1bb3fd965bb30efd79447d5ea68b5334816a7452d40b58`. That public constant is the only source change since 0.5.0: no client, request, response, model, error, feature flag or dependency changed, and the packaged file list is the same 13 files ([628b161](https://github.com/Sendmux/sendmux-sdk/commit/628b161d2692775ac1f4830c1d64c024ba04ed83)).

Decision for ROOT: ship 0.5.1 with this lead (recommended — release-please will keep re-proposing 0.5.1 while the `fix:` merge 628b161 sits in the Rust window, and docs.rs then advertises the constant the repo actually pins), or close #261 as bot noise and accept that the published constant stays `09b00ae1…` until the next real Rust change.

### Bug Fixes

* regenerate SDKs from the deployed flattened response schemas (docs 86b0f45) ([628b161](https://github.com/Sendmux/sendmux-sdk/commit/628b161d2692775ac1f4830c1d64c024ba04ed83))

## [0.5.0](https://github.com/Sendmux/sendmux-sdk/compare/rust-v0.4.0...rust-v0.5.0) (2026-09-19)


### Changed

* **Breaking:** `Attachment` is an enum: `Inline(InlineAttachment)` or `Uploaded(UploadedAttachmentRef)`. Replace struct literals and direct field access with `Attachment::base64(filename, content)` / `Attachment::uploaded(attachment_id)` or match the variants ([3703a89](https://github.com/Sendmux/sendmux-sdk/commit/3703a899cd234bee362bb51f52af15f85e9c1388)). See [0.5.0 Rust contract changes](README.crates.io.md#050-rust-contract-changes).
* **Breaking:** `Response<T>` gains `pagination: Option<CursorPagination>`; add `pagination: None` to response fixtures without cursor metadata ([3703a89](https://github.com/Sendmux/sendmux-sdk/commit/3703a899cd234bee362bb51f52af15f85e9c1388)).
* **Breaking:** `Error` gains the `InvalidRequestPath` variant; exhaustive `match` arms must add it ([3703a89](https://github.com/Sendmux/sendmux-sdk/commit/3703a899cd234bee362bb51f52af15f85e9c1388)).

### Added

* Single and batch sends accept one delivery group or a list of groups (`delivery_group`) that narrows the eligible provider pool ([94f52d4](https://github.com/Sendmux/sendmux-sdk/commit/94f52d4e9f6157e197308541cc5987517bac7a4a)).
* Six list methods accept cursors through `*_with_cursor` variants; pass `pagination.next_cursor` while `has_more` is true ([3703a89](https://github.com/Sendmux/sendmux-sdk/commit/3703a899cd234bee362bb51f52af15f85e9c1388)).
* Single and batch sends accept `Attachment::uploaded(attachment_id)` for existing Sending attachment references ([3703a89](https://github.com/Sendmux/sendmux-sdk/commit/3703a899cd234bee362bb51f52af15f85e9c1388)).

### Security

* Raw Mailbox and Management requests reject absolute URLs, authority paths, and backslash paths before resolving credentials or sending HTTP requests; supply paths relative to the configured API base ([3703a89](https://github.com/Sendmux/sendmux-sdk/commit/3703a899cd234bee362bb51f52af15f85e9c1388)).


### Features

* integrate combined provider variables and delivery routing ([81bbf22](https://github.com/Sendmux/sendmux-sdk/commit/81bbf221a357bf5d588eba654184ff34491473df))
* **sdk:** add provider variables and delivery group routing ([94f52d4](https://github.com/Sendmux/sendmux-sdk/commit/94f52d4e9f6157e197308541cc5987517bac7a4a))


### Bug Fixes

* **sdk:** adopt final provider contract description and provenance ([a9bdaf5](https://github.com/Sendmux/sendmux-sdk/commit/a9bdaf58f0db684328458e269ba8aff515334d0b))
* **sdk:** adopt final provider contract description and provenance ([815278e](https://github.com/Sendmux/sendmux-sdk/commit/815278e76587dcba314c51202b8e764250e51ef3))
* **sdk:** verify Rust contracts and installed runtime consumers ([3703a89](https://github.com/Sendmux/sendmux-sdk/commit/3703a899cd234bee362bb51f52af15f85e9c1388))

## [0.4.0](https://github.com/Sendmux/sendmux-sdk/compare/rust-v0.3.0...rust-v0.4.0) (2026-09-11)


### Features

* add REST OAuth clients and CLI token lifecycle ([cc4a3aa](https://github.com/Sendmux/sendmux-sdk/commit/cc4a3aa6110378641418a94455ed5b9a986e65ff))

## [0.3.0](https://github.com/Sendmux/sendmux-sdk/compare/rust-v0.2.0...rust-v0.3.0) (2026-09-08)


### Features

* add connection checks across SDKs, CLI and MCP ([77f449e](https://github.com/Sendmux/sendmux-sdk/commit/77f449e2c8cba49bc8bc84c49c35baa61120866a))
* **sdk:** add connection checks across clients, CLI and MCP ([3e02c67](https://github.com/Sendmux/sendmux-sdk/commit/3e02c67dcab45e37dad7abbdd4c4e1bd0b1fbbe6))

## [0.2.0](https://github.com/Sendmux/sendmux-sdk/compare/rust-v0.1.0...rust-v0.2.0) (2026-07-01)


### Features

* allow owner-approved agent tokens for sending ([9d1cb7d](https://github.com/Sendmux/sendmux-sdk/commit/9d1cb7df3df5aef1f59a4990dc087178ba3a7b21))

## 0.1.0

- Initial Sendmux Rust SDK crate.
