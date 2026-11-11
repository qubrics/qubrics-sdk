# Changelog

## Unreleased

## [2.0.0](https://github.com/qubrics/qubrics-sdk/compare/python-sending-v1.6.0...python-sending-v2.0.0) (2026-11-11)


### ⚠ BREAKING CHANGES

* **python:** move SDK packages into the Qubrics namespace

### Features

* add compatible Qubrics integration aliases ([dff5cb8](https://github.com/qubrics/qubrics-sdk/commit/dff5cb89bccb5840d55071d23f79ff88c7e58040))
* preserve integration contracts with Qubrics aliases ([722fbab](https://github.com/qubrics/qubrics-sdk/commit/722fbab2f98248d17b4878dd5149a35a711d5a18))
* **python:** move SDK packages into the Qubrics namespace ([a326bc9](https://github.com/qubrics/qubrics-sdk/commit/a326bc923fff448470d908bb527afaaa35f6d739))


### Bug Fixes

* preserve legacy SDK compatibility with dual aliases ([4910037](https://github.com/qubrics/qubrics-sdk/commit/491003792dd742cb2c83e4a09501abdf4f4458c9))
* preserve Python environment compatibility with published core ([8f4c78f](https://github.com/qubrics/qubrics-sdk/commit/8f4c78f050725b6d57a6b71d39178dee40c1774e))


### Documentation

* use generated SDK method names in examples ([5bb29fc](https://github.com/qubrics/qubrics-sdk/commit/5bb29fc309bae1013da2802210a5b23ccf9dbfd0))

## [1.6.0](https://github.com/Sendmux/sendmux-sdk/compare/python-sending-v1.5.1...python-sending-v1.6.0) (2026-09-16)


### Features

* Add one delivery group or a list of `delivery_group` IDs to email send requests.
* integrate combined provider variables and delivery routing ([81bbf22](https://github.com/Sendmux/sendmux-sdk/commit/81bbf221a357bf5d588eba654184ff34491473df))
* **sdk:** add provider variables and delivery group routing ([94f52d4](https://github.com/Sendmux/sendmux-sdk/commit/94f52d4e9f6157e197308541cc5987517bac7a4a))


### Bug Fixes

* correct generated client contracts ([dd31abe](https://github.com/Sendmux/sendmux-sdk/commit/dd31abed8e264e05f4717388a0d4ada83e47d7e3))

## [1.5.1](https://github.com/Sendmux/sendmux-sdk/compare/python-sending-v1.5.0...python-sending-v1.5.1) (2026-09-15)


### Bug Fixes

* preserve attachment idempotency across composite sends ([5549549](https://github.com/Sendmux/sendmux-sdk/commit/554954947126eb2bdf56e1bf675ebc2b908a8216))
* **sending:** bound attachment file reads before upload ([83cb780](https://github.com/Sendmux/sendmux-sdk/commit/83cb7802a0e35d0779dad2f2c7d69e21c6d3d8d3))
* **sending:** reject excess files before attachment uploads ([3a1deca](https://github.com/Sendmux/sendmux-sdk/commit/3a1deca72f3fac51bb3843fce175ba2cd367e7c7))
* **sending:** preserve API errors during context-manager cleanup with a `sendmux-core` minimum of `1.3.1`

## [1.5.0](https://github.com/Sendmux/sendmux-sdk/compare/python-sending-v1.4.0...python-sending-v1.5.0) (2026-09-10)


### Features

* add REST OAuth clients and CLI token lifecycle ([cc4a3aa](https://github.com/Sendmux/sendmux-sdk/commit/cc4a3aa6110378641418a94455ed5b9a986e65ff))

## [1.4.0](https://github.com/Sendmux/sendmux-sdk/compare/python-sending-v1.3.0...python-sending-v1.4.0) (2026-09-08)


### Features

* add connection checks across SDKs, CLI and MCP ([77f449e](https://github.com/Sendmux/sendmux-sdk/commit/77f449e2c8cba49bc8bc84c49c35baa61120866a))
* **sdk:** add connection checks across clients, CLI and MCP ([3e02c67](https://github.com/Sendmux/sendmux-sdk/commit/3e02c67dcab45e37dad7abbdd4c4e1bd0b1fbbe6))

## [1.3.0](https://github.com/Sendmux/sendmux-sdk/compare/python-sending-v1.2.0...python-sending-v1.3.0) (2026-07-08)


### Features

* **sdk:** add sending attachment upload surfaces ([#96](https://github.com/Sendmux/sendmux-sdk/issues/96)) ([b8f9d5f](https://github.com/Sendmux/sendmux-sdk/commit/b8f9d5fe3c1ae510db82ce05c55cbcad92b43b44))

## [1.2.0](https://github.com/Sendmux/sendmux-sdk/compare/python-sending-v1.1.0...python-sending-v1.2.0) (2026-07-03)


### Features

* **sdk:** add zero-context attachment uploads ([a4352ec](https://github.com/Sendmux/sendmux-sdk/commit/a4352ecfd6f2da37c908387450fea141363d0b81))
* **sdk:** make mailbox attachments agent-ready ([6a145ab](https://github.com/Sendmux/sendmux-sdk/commit/6a145ab1f2735d77783fb36e84aeeeb9bc747827))

## [1.1.0](https://github.com/Sendmux/sendmux-sdk/compare/python-sending-v1.0.4...python-sending-v1.1.0) (2026-07-01)


### Features

* allow owner-approved agent tokens for sending ([9d1cb7d](https://github.com/Sendmux/sendmux-sdk/commit/9d1cb7df3df5aef1f59a4990dc087178ba3a7b21))

## [1.0.4](https://github.com/Sendmux/sendmux-sdk/compare/python-sending-v1.0.3...python-sending-v1.0.4) (2026-06-19)


### Bug Fixes

* **python:** add package metadata classifiers ([9a79f5d](https://github.com/Sendmux/sendmux-sdk/commit/9a79f5d118766c5a59fdc9e568f4cf08874f1486))

## [1.0.3](https://github.com/Sendmux/sendmux-sdk/compare/python-sending-v1.0.2...python-sending-v1.0.3) (2026-06-18)


### Documentation

* update Sendmux docs links ([24b89cb](https://github.com/Sendmux/sendmux-sdk/commit/24b89cb851dd8f37dd1304eb292681892bad077d))

## [1.0.2](https://github.com/Sendmux/sendmux-sdk/compare/python-sending-v1.0.1...python-sending-v1.0.2) (2026-06-17)


### Bug Fixes

* keep generated python package versions current ([#26](https://github.com/Sendmux/sendmux-sdk/issues/26)) ([3405116](https://github.com/Sendmux/sendmux-sdk/commit/3405116d0ee8ec538de2b09897ebae101a714b28))
* **python:** derive generated runtime version dynamically ([#30](https://github.com/Sendmux/sendmux-sdk/issues/30)) ([2c2100b](https://github.com/Sendmux/sendmux-sdk/commit/2c2100ba5e069229dc5bf4ea62056c3c479a5152))

## [1.0.1](https://github.com/Sendmux/sendmux-sdk/compare/python-sending-v1.0.0...python-sending-v1.0.1) (2026-06-17)


### Bug Fixes

* **python:** publish dists with supported metadata ([e5506e7](https://github.com/Sendmux/sendmux-sdk/commit/e5506e71410a61a7ddcf547f67f863ff2cfc60d6))

## 1.0.0 (2026-06-01)


### Features

* **python-sdk:** add generated Python packages ([82c4a84](https://github.com/Sendmux/sendmux-sdk/commit/82c4a84976b4d9802f993b07302430546a323543))
