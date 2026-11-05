# Canonical PHP rename qualification

Goal: A11 PHP rename released through all five Composer packages, with A17 compatibility retained. This PR qualifies canonical source only; merge, split synchronisation, approved tags and registry verification remain separate steps.

## Source and scope

- Base: `388a4107d25e6cf94a7c7704b094f8765f851be3`.
- Spec: [A11 and A17](https://github.com/qubrics/qubrics/blob/main/specs/rebrand-qubrics/spec.md), tracked by [PHP issue 4](https://github.com/qubrics/qubrics-php-sdk/issues/4).
- Generated clients come from `scripts/generate-php.mjs`, using the committed OpenAPI snapshots. No generated PHP file was hand-edited.
- Preserve newer canonical API operations/models, discriminator handling, HTTP dependency security floors, Qubrics-first environment lookup, both message-ID maps, credential prefixes, OAuth, retries and validation.
- Copy split public contracts and CI into canonical packages. Standalone tests use local closures and wrapped lines to pass existing PSR-12 checks without changing assertions.
- Ops approved subsequent normal-commit removal of split agent docs and historical evidence, preserving strict publisher parity. SDK local `AGENTS.md:5` forbids publishing agent rules. No history rewrite or publisher exclusions.

## Measured local checks

- Composer/public interface red: `QubricsPackagesTest` failed because `qubrics/*` was not installed and the renamed model could not load.
- Generator-origin upload-header red: corrected A17 expectations failed 35 of 40 existing public call forms. Legacy and current parameter forms now emit both headers. Configured-key forms are covered too. The new configured-key fixture initially leaked default configuration across cases; each case now receives its own Configuration.
- Publisher red: a Qubrics Composer identity was rejected as `Split Composer identity/version metadata mismatch`.
- Release-state red: `packages/php/core Composer identity`, actual `qubrics/core`, expected `sendmux/core`. Corrected only PHP identity assertions.
- PHP suite: 141 tests, 1084 assertions, exit 0.
- OAuth/environment tests: 16 tests, exit 0.
- Five actual Composer path installs and all five split public contracts: exit 0. These are local fixtures, not public Packagist resolution.
- Publisher tests: 12 tests, exit 0. They include exact-source parity, live mismatch rejection, immutable annotated target, clean worktree, sole push destination and legacy Composer-identity rejection. Test tags exist only in disposable fixture repositories.
- PHPStan max level, PSR-12, PHP adapter syntax and release-state check: exit 0.
- External locked Composer dependencies are unchanged. Five local Qubrics fixture versions are 3.0.0.
- Docs: fresh-reader critique corrected API-key environment guidance so it cannot imply OAuth tokens are optional. One humanise pass preserved identifiers, URLs, versions and migration requirements.

Raw logs: SDK MAIN `.claude/artifacts/rebrand-qubrics-php4-canonical/` (`packages-red.log`, `upload-red.log`, `publisher-red.log`, `release-state-red.log`, `phpunit.log`, `oauth-env.log`, `split-contracts.log`, `publisher-green.log`, `phpstan.log`, `phpcs.log`).

## Publication limits

The red live canary blocks PHP split qualification directly: `publish-php-split.mjs:89` calls `checkSource`; `publication-guard.mjs:50-52` runs the canary before any tag is created or pushed. Main run [42020582253](https://github.com/qubrics/qubrics-sdk/actions/runs/42020582253) failed because the app snapshot URL was `app.qubrics.com` while live schema used `app.sendmux.ai`. Ops assigns the origin fix and app deployment to issue 972 after the 927 window. This PR does not edit or bypass that gate.

Read-only non-PHP trace found independent optional header names in Python, Ruby and Go, and in TypeScript's public named-header path. Raw generated TypeScript generic `auth` can fill both schemes independently; sdk343 owns that caveat. No other-language change is included.

No live API run, production mutation, real release tag, Packagist submission or abandonment write occurred. All next-major tags need a later exact-SHA operator ASK.
