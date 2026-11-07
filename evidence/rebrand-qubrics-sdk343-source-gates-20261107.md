# SDK #343 source release-gate correction

The core publisher run [42326579235](https://github.com/qubrics/qubrics-sdk/actions/runs/42326579235) failed in `pnpm build` before the publication script ran. Its PHP folder-delete compatibility test imported `Sendmux\Mailbox\Model`, while the renamed PHP package's Composer mapping and generated classes use `Qubrics\Mailbox\Model`.

The test now uses Qubrics in its three PHP references. Alias identity, response identity and JSON round-trip assertions remain intact. No compatibility alias, skip, threshold or package version changed.

Source CI's existing verify job now runs the publisher's complete `pnpm build` chain: core verification, native language checks, folder-delete compatibility, static live-E2E coverage and connection adapters. The separate runtime preparation and live-E2E invocations were already covered by that chain and are removed. Existing language and runtime matrix jobs remain.

## Verification

- The unchanged PHP regression failed at `b79c9bed` with `Class "Sendmux\Mailbox\Model\MailboxFolderDeletedResponseAllOfData" not found` (PHP255, Node assertion failure). The publisher's four-case suite had3pass/1fail.
- After the namespace correction, `node --test --test-name-pattern='PHP preserves' scripts/mailbox-folder-delete-compat.test.mjs` passed1/1, no skips. The test still checks the original deprecated model alias, type, response and round-trip behaviour.
- `git diff --check` passed. A scan of scripts, workflows and PHP tests found no remaining stale PHP Sendmux namespace reference of this form.
- The PR's verify check runs the full root build before merge. The immutable source candidate also receives a fresh live/Skills guard check; its exact receipts are attached to the PR qualification rather than substituted with the historical core receipt.

## Scope and candidate boundary

A11 covers Packagist/PHP namespaces. Python's distribution/import rename belongs to A18; current `packages/python/mailbox/pyproject.toml` still declares `sendmux-mailbox` and `sendmux_mailbox`. The passing Python imports remain unchanged.

`scripts/publication-guard.mjs:82–97` validates the supplied checkout SHA, snapshots, release tag/native version when supplied, live contract and Skills acceptance. It does not inspect previous Actions conclusions. Preflight selects merged `autorelease: pending` sources at lines252–254. Core's historical failed workflow therefore does not become an input to a later candidate.

The published core2.0.0 is accepted on registry integrity and fresh installation. Its historical workflow remains red; no rerun, retag, replacement version or npm write is part of this source correction. Sending's own publication run must later prove the already-published skip path. This source PR neither merges a release PR nor publishes a package.
