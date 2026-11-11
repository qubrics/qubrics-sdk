# Windows cleanup sensitivity boundary

Ops assigned the source cause blocking SDK344 after PR374 merged as 6dc1bb45. One source-only PR; normal merge on green with revert rollback. No package/release/Homebrew change or sdk344 branch/evidence mutation.

## Observed failure

[Main CI42954543429](https://github.com/qubrics/qubrics-sdk/actions/runs/42954543429), Windows26 job130306416973, fails `Prove Windows command control sensitivity` in the `swallowed-cleanup-error` mutation. Raw SDK MAIN evidence remains under .claude/artifacts/rebrand-qubrics-sdk344/pr374-windows26-130306416973.log, lines2039-2113. The persistent row has command_closed=true and holder_pid6560, but no lock_confirmed/error; cleanup_elapsed_ms is null, then `Do not mistake startup failure for filesystem behavior`. Test-owned recovery proves holder and directory absent. Earlier mutation failures have detected=true and are expected; injected OAuth EBUSY receipts are unrelated.

The affected callback is `test-windows-workspace-cleanup.mjs`'s readiness/liveness/rmdir boundary before lock_confirmed. It uses an independent explicit directory-lock holder. PR371's completed consumer command precedes that boundary; this trace does not prove its retained-member EBUSY recurrence and does not meet issue365's reopen trigger.

## Confirmed observation gap

The sensitivity mutation changes the workspace finally cleanup to `catch (error) { if (error.code === "EBUSY") return; throw error; }`. A callback error before lock_confirmed can therefore be discarded before the fixture's outer catch. Canonical per [MDN try/finally](https://github.com/mdn/content/blob/main/files/en-us/web/javascript/reference/statements/try...catch/index.md), researched via Context7 /mdn/content: a return from finally overrides a pending throw.

The first change saves/logs that exact boundary error before workspace finally runs, rethrows it and preserves every original assertion and timeout. Existing14day artifact upload gains only the failed cleanup sensitivity results glob; successful fixtures still remove their scratch. This closes the observation gap; historical exception attribution remains unavailable. The controlled Windows proof below establishes a readiness-publication defect at this same boundary. No sleep, retry, widened deadline or relief rerun is the fix.

## Qualification

Focused local syntax/shim/wiring checks pass. The instrumentation head `5f83abe7` passed CI42956275209 34/34 without recurrence. Normal corrected-head CI on actual Windows22/24/26 is required before merge. No platform emulation, new CI job or standalone harness; no tests or assertions removed.

## Readiness discriminator

The instrumentation run does not establish the discarded original exception.

Microsoft's [.NET Framework File source](https://github.com/microsoft/referencesource/blob/main/mscorlib/system/io/file.cs#L884-L891) implements WriteAllText by constructing a StreamWriter, then writing and disposing. [StreamWriter's source](https://github.com/microsoft/referencesource/blob/main/mscorlib/system/io/streamwriter.cs#L224-L227) creates the file with FileShare.Read before those contents are flushed. The fixture currently treats file existence as complete JSON publication. That permits a reader to parse incomplete JSON while the independent lock holder is live.

The existing swallowed-cleanup sensitivity fixture now pauses that same StreamWriter between creation/buffered write and disposal, using test-owned barrier files. Its parent observes this boundary within the unchanged ten-second readiness deadline, releases the writer in finally, and retains every existing lock/cleanup/recovery assertion. No production hook, extra job, workload retry or deadline increase is added. Expected red on the current direct writer: SyntaxError at the retained lock-confirmation boundary and the original startup assertion, with the exact holder recovered. This tests the leading mechanism rather than asserting it was the lost historical exception.

Alternatives: early holder exit predicts nonzero/abnormal recovery, whereas the original holder recovered normally after less than one second; unexpected rmdir behavior remains distinguishable in the new exact boundary capture. PR371's command had already closed before this independently spawned holder. Historical attribution remains limited by the discarded assertion and missing artifact.

## Confirmed red and origin correction

[CI42958723285](https://github.com/qubrics/qubrics-sdk/actions/runs/42958723285), head `8cef5770`, reproduced the defect on all three native Windows versions. Node22 job130319919353 logs the two boundary SyntaxErrors at lines2500/2517; Node24 job130319919393 at2075/2092; Node26 job130319919425 at2077/2094. Each says `Unexpected end of JSON input`. Both fixture modes then report `Do not mistake startup failure for filesystem behavior`, no lock_confirmed, holder_absent=true, path_absent_after_recovery=true and no cleanup_error. The other15 sensitivity mutations are detected. Raw logs: SDK MAIN .claude/artifacts/rebrand-qubrics-sdk343/cleanup375-buffered-red-node{22,24,26}.log.

This explains how the independent holder can be live while JSON parsing fails before lock confirmation and the intentional finally return discards that error. It is a mutation-fixture readiness-publication defect, not a demonstrated PR371 process-rundown recurrence. The original run's exact exception is irrecoverable; this counterexample demonstrates the same failure pattern, not recovery of the lost exception.

Canonical correction: write to an adjacent `.pending` path, let WriteAllText close it, then publish it with File.Move. [.NET Framework File.Move](https://github.com/microsoft/referencesource/blob/main/mscorlib/system/io/file.cs#L1262-L1268) invokes Win32 MoveFile; source and destination share the same directory. The polled path is absent throughout the unflushed write. No parser retry, new polling, deadline increase, removed assertion or PR371 change. The same paused-writer regression remains in the sensitivity test and must now reach every existing lock/cleanup assertion.

Local syntax, mutation-injection compilation, Windows command-shim and workflow wiring checks pass. Corrected native CI and settled Spec/Standards review remain required. README still accurately states seven published npm packages; no package metadata or public SDK surface changes.
