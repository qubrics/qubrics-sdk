# Windows consumer teardown origin fix

Ops allocated the Windows consumer-ownership origin blocking Ruby PR368 to SDK343. One source-only PR371; sdk344 branches/diagnostics and Homebrew cooldown remain unchanged. Current qualification is the confirmed retained holder removed at source, measured limit0 acceptance, original assertions/2000ms/final ActiveProcesses check, real Windows22/24/26 sensitivity, normal merge and mainCI. The earlier-terminating-before-snapshot race is an explicitly accepted residual, not a gate for this observed fix.

## Confirmed holder and source trace

Ruby PR368 head764f0a8daa04e2d5feb5ca8fea37ed990b74edae, CI42814426845, failed sensitivity on Windows22/24/26. Node22 also reported an unconfirmed controller shutdown; Windows24/26 reported process absence/workspace removal before fixture-root EBUSY. Immutable raw evidence remains under SDK MAIN .claude/artifacts/rebrand-qubrics-sdk344/, including ruby-windows-origin-blocker.md's routing pointers. No sdk344 file was changed.

PR371's changed capture heads22c5b3dd and d4af0a94 passed CI42820359874 and42824638501, each34/34, without recurrence. Those green runs were inconclusive. Historical capture head65a28f70e5bbcc1d43a6ae6838275b52ea622a12, [CI42827249823](https://github.com/qubrics/qubrics-sdk/actions/runs/42827249823), failed Windows22 job129867680340 at the original healthy PowerShell leader-exit cleanup; Windows24/26 passed.

SDK MAIN artifact windows-origin-history-node22.zip contains windows-consumer-trace/fixture-history.csv (line numbers include header):

- 3357:13:50:25.0801868, powershell.exe6592 starts, parent8600, cwd sendmux-windows-ownership-WLUsr7. Its encoded command writes descendant.json with its PID and sleeps45s, matching the diagnostic Start-Process descendant.
- 3358:13:50:25.0850616, PID6592 opens the fixture directory with Execute/Traverse,Synchronize, sharing Read/Write without Delete.
- 3758:13:50:25.6743875, diagnostic owner5708's Delete-capable open fails SHARING VIOLATION.
- 3820-3822: PID6592 exits at13:50:26.1925116 and closes the directory at13:50:26.1926833, 518.2958ms after the failed deletion.

Raw windows-origin-history-node22.log:2033-2039 ties the process to the fixture and records both PIDs absent and the owned command workspace removed before EBUSY. Source owner is scripts/diagnose-windows-consumer-ownership.mjs's Start-Process -WorkingDirectory call. The controller previously called TerminateJobObject then trusted accounting0/bootstrap exit before completion. That receipt preceded the confirmed descendant's cwd-handle rundown. Late empty Handle/CIM snapshots miss a holder which disappears during observer startup.

## Origin change and canonical contracts

scripts/windows-consumer-job.ps1 now sets JOB_OBJECT_LIMIT_ACTIVE_PROCESS with ActiveProcessLimit=0, preserving kill-on-close/no-breakaway. SetInformationJobObject rejection throws a labelled error; there is no limit1 fallback. A successful native call logs windows_job_admission_limit=0/accepted=true; the complete PID list is logged as windows_job_shutdown_snapshot.

The controller retains verified member process handles before termination, confirms membership to avoid recycled PID ownership, and waits each retained handle to signal before writing completion. Freed PIDs and recycled non-members do not abort interrupted shutdown; other native errors throw. The same2000ms deadline covers limit setting, enumeration and waits. Final ActiveProcesses/bootstrap confirmation, stdout/exit semantics, orphan/deadline rejection, and every sensitivity assertion remain.

Canonical per [TerminateJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject): termination acts as TerminateProcess for each member. [TerminateProcess](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess) is asynchronous and prescribes a process-handle wait. [Terminating a process](https://learn.microsoft.com/en-us/windows/win32/procthread/terminating-a-process) lists kernel objects closed and the process object signalled.

[ActiveProcessLimit](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information) rejects associations exceeding the limit; failed associations retain their active count until termination and all process handles close. The final count check covers those rejected associations. [PROCESS_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-process_information) keeps a PID valid until all process handles close and its object is freed; [Job objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects) says established association cannot be broken.

Temporary always-on Procmon capture is removed after identifying the holder. Error-only Handle/CIM capture and14-day artifact retention remain. Direct Handle lookup uses the unique basename, covering short/long path spellings and owned-workspace errors as well as fixture errors, and falls back to handle64.exe when the existing Chocolatey caller omits its env path. A missing executable remains an inspectable spawnSync error so CIM/snapshot capture survives; original cleanup errors still rethrow.

## Known residual and reopen trigger

The bootstrap's native exit is confirmed with only the remaining original deadline; its ID/exit code are cached and its process handle is closed before final accounting confirmation. This prevents an admission-rejected bootstrap's retained handle from keeping the failed-association active count nonzero. Exceptions still dispose the handle, and rejection creates no completion receipt.

A member already terminating before the shutdown snapshot may be missing from it while native rundown continues. This reasoned race was not observed in the confirmed retained-member failure. Ops explicitly accepted it outside this fix's gate.

Record in issue365: any post-fix EBUSY whose confirmed holder PID is absent from the matching windows_job_shutdown_snapshot reopens the issue. Preserve actual holder identity/path and snapshot; post-wait EBUSY alone does not establish external ownership. No retry, sleep, widened deadline, skip or relaxed assertion is the fix.

## Qualification

Before native qualification: pnpm test:windows-command-shims, node --check scripts/diagnose-windows-consumer-ownership.mjs and git diff --check exit0. Focused log: SDK MAIN .claude/artifacts/rebrand-qubrics-sdk343/windows-origin-limit0-local.log. No Mac emulation or measured limit0 acceptance claimed.

Static Spec and Standards reviews passed with no actionable findings, including the bootstrap handle correction. Next: one normal PR CI on corrected head; read actual limit0 success/rejection and Windows22/24/26 sensitivity. Rejection or red means stop/report, no fallback/rerun. Green permits normal merge with revert rollback, then mainCI readback. No release/package/API version change, publication or sdk344 mutation. README publication statement/table remain accurate for this task's seven published npm packages.
