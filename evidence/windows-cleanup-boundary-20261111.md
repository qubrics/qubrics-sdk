# Windows cleanup sensitivity boundary

Ops assigned the source cause blocking SDK344 after PR374 merged as 6dc1bb45. One source-only PR; normal merge on green with revert rollback. No package/release/Homebrew change or sdk344 branch/evidence mutation.

## Observed failure

[Main CI42954543429](https://github.com/qubrics/qubrics-sdk/actions/runs/42954543429), Windows26 job130306416973, fails `Prove Windows command control sensitivity` in the `swallowed-cleanup-error` mutation. Raw SDK MAIN evidence remains under .claude/artifacts/rebrand-qubrics-sdk344/pr374-windows26-130306416973.log, lines2039-2113. The persistent row has command_closed=true and holder_pid6560, but no lock_confirmed/error; cleanup_elapsed_ms is null, then `Do not mistake startup failure for filesystem behavior`. Test-owned recovery proves holder and directory absent. Earlier mutation failures have detected=true and are expected; injected OAuth EBUSY receipts are unrelated.

The affected callback is `test-windows-workspace-cleanup.mjs`'s readiness/liveness/rmdir boundary before lock_confirmed. It uses an independent explicit directory-lock holder. PR371's completed consumer command precedes that boundary; this trace does not prove its retained-member EBUSY recurrence and does not meet issue365's reopen trigger.

## Confirmed observation gap

The sensitivity mutation changes the workspace finally cleanup to `catch (error) { if (error.code === "EBUSY") return; throw error; }`. A callback error before lock_confirmed can therefore be discarded before the fixture's outer catch. Canonical per [MDN try/finally](https://github.com/mdn/content/blob/main/files/en-us/web/javascript/reference/statements/try...catch/index.md), researched via Context7 /mdn/content: a return from finally overrides a pending throw.

The first change saves/logs that exact boundary error before workspace finally runs, rethrows it and preserves every original assertion and timeout. Existing14day artifact upload gains only the failed cleanup sensitivity results glob; successful fixtures still remove their scratch. This is observation, not an asserted startup/lock cause fix. Native readiness/lock cause remains unknown until the original assertion is captured; no sleep, retry, widened deadline, relief rerun or guessed readiness change is the fix.

## Qualification

Pending focused local syntax/shim/wiring checks, then existing normal PR CI on actual Windows22/24/26. No native Windows proof can be obtained from this Mac, and no platform emulation is claimed. No new CI job or standalone harness. No tests or assertions removed.
