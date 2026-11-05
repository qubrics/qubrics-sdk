# TypeScript SDK and CLI rename (#343)

Status: source preparation in progress. Packages are not published by this change. All npm publication and deprecation actions require the exact-version operator packet and operator execution.

## Scope and release targets

Implements A10 and A12 in the parent rebrand spec. Operator-approved additive correction includes sending, consistently with A11 and A18. Feedback-widget has no approved replacement and is excluded; its owner is `qubrics/website-feedback-widget`.

| Package | Target version |
| --- | --- |
| `@qubrics/core` | `2.0.0` |
| `@qubrics/sending` | `2.0.0` |
| `@qubrics/mailbox` | `3.0.0` |
| `@qubrics/management` | `3.0.0` |
| `@qubrics/sdk` | `3.0.0` |
| `@qubrics/ai-sdk` | `1.0.0` |
| `@qubrics/cli` | `2.0.0` |

Source package versions remain equal to the existing release manifest. Seven `release-as` overrides instruct release-please to update package metadata, manifest and changelog together in the intended release PRs. The overrides must be removed once those initial PRs exist. A release PR merge can publish automatically and remains an operator action.

## Behaviour and compatibility

- Package imports and dependency edges use the seven approved names. Public SDK identifiers, credential prefixes, environment/header aliases and historical changelogs remain compatible.
- Handwritten Mailbox/Management factories use `app.qubrics.com`; Sending uses `smtp.qubrics.com`. CLI OAuth and agent defaults use their qualified Qubrics hosts.
- `qubrics` runs the CLI directly. For one major, `sendmux` prints `sendmux is deprecated. Use qubrics instead.` before invoking the same runner. Existing profile storage stays available and credentials remain private.
- Native archives stage the current local packed SDK dependencies. A preparation hook restores registry version metadata, removes local overrides and replaces the generated legacy symlink with portable compatibility launchers. Native packaging does not require the new packages to be published first.
- Homebrew's updater targets the Qubrics formula and package; Homebrew #14 owns the legacy formula alias. Existing Chocolatey package identities remain unchanged while both executable names are required.

## Measured checks

The new public-factory tests first failed for all three surfaces: actual `https://app.sendmux.ai` versus expected `https://app.qubrics.com` for Mailbox/Management, and the analogous SMTP mismatch. After changing the factory origins, all three passed.

| Check | Result |
| --- | --- |
| Recursive TypeScript build | Exit 0 |
| Public factory default-host regressions | 3 red, then 3 green |
| TypeScript helpers | 50 passed |
| AI OAuth and tool-set checks | 3 passed, self-check passed |
| Packed consumer provenance | 2 red, then 2 green |
| OAuth, sender and session contracts | 30 passed |
| Connection defaults | 3 passed |
| Release-state checks | 32 passed |
| Full CLI gate | Passed |
| CLI version, notice ordering, existing profiles and native argv/exit tests | Passed |

The native-pack origin regression was observed as `npm error E404` for the renamed SDK before publication. Staging local packed siblings removes that registry prerequisite. Full native packing and real Windows install/uninstall proof remain required in CI.

The packed dependency negative test still rejects a different installed instance. Its old registry fixture could not exist under the new package namespace, so the replacement fixture installs a separate local tarball and preserves the negative and positive assertions.

Raw logs are retained in the task's local artifacts: `ts-default-hosts-{red,green}.log`, `ts-helpers-green.log`, `ts-ai-sdk-green.log`, `consumer-rename-{red,green}.log`, `connection-defaults-green.log`, `release-state-current.log`, `check-cli-current.log`, `cli-rename-current.log` and `cli-pack-red.log`.

## Outstanding verification and release boundaries

- Rebased on merged #351 (`388a410`), which owns docs `03210aa9` regeneration and the two PHP default assertions. No duplicate generated edits.
- Observe the Windows Chocolatey regression through the real install smoke, then fix installation/uninstallation at the templates and verify both commands and cleanup.
- Complete required CI and settle review on the final source head. Refresh Skills #34 compatibility acceptance for the renamed CLI metadata against that exact candidate.
- Fresh-checkout live safety initially passed 65/75. Ten failures traced to missing Python/MCP runtime prerequisites, including `.tmp/python-venv/bin/python`. Prepare the existing prerequisites and obtain a complete green check. No assertion was weakened.
- After operator publication, freshly install each exact registry version outside the workspace, verify dependency resolution and default-host calls, then read back all approved old-version deprecation warnings. No send or production mutation is needed for these read-oriented smokes.

Read-only registry inventory found 70 old versions across the seven replacement packages. Only CLI `1.3.0` already had a broken-release warning; the operator packet preserves that warning while adding the replacement pointer. Feedback-widget and unscoped MCP are excluded.

Publication has no true rollback: npm name/version pairs cannot be overwritten. Existing packages remain available, and fixes require a separately approved forward release. Deprecation metadata can be restored by the operator from the captured baseline under separate authorisation.

Independent Standards review found no actionable issue. Spec review identified the Windows shim gap described above; its real Windows proof remains open. Snap remains on its existing package pin; migrating that separate distribution requires preserving its npm provenance checks.
