# Calendar-free Python Mailbox replacement candidate

PR380 prepares the unpublished PyPI `qubrics-mailbox 3.0.0` under operator
1A, 18 November. It does not authorise a release merge, tag, upload, registry
write or environment approval. The later combined ASK also covers the Rust
0.6.0 re-cut, crate identity and the Phase 1 public API contract.

## Qualified source

Source PR378 normally merged at
`7a0bf484344bb68fb9c8508e83e49c80c56cfaf1`, identical tree to independently
reviewed `9773d640714c78dad1c19bc646ee5bee099893c7`.
PR CI44259534505 and main CI44261234996 passed 34/34, zero skipped;
42/42 checks and the final review sweep were clean. Source Spec/Standards
reviews returned zero findings. The fresh default Skills v2.0.5 guard passed
all 22 results and live OpenAPI equality on9773d640. Its candidate digest is
`86ad95d5f5e46033497329ca23bde93632950145bca21024643f372771d2fcf2`.
No claim of exact acceptance for a later candidate is inherited from it.

The Ruby prerequisite PR379 normally merged at
`b272a770c8434e7a9743def964853a4f6712c806`; PR/main CI both34/34 green.
Only CI test workflows and native pins changed to the official vendor action
20eb24b0 / Ruby3.4.12. Release/publish/tag workflows were untouched.
The subsequent stale Python-calendar lifecycle expectation was corrected at
the matrix/runner capability contract: two red receipts, then27/27 focused
tests, all native/runtime main checks green. Full trace is in
`evidence/sdk344-calendar-free-20261118.md`.

## Replacement metadata

Official installed Release Please17.6.0 `Manifest.fromManifest` and
`createPullRequests` created PR380 at
`c15666a0ac68d597aea1f60b5a4be6827e29d452`, scoped only to
`packages/python/mailbox`, explicit releaseAs3.0.0. No persistent release-as
key or workflow changed, and `createReleases` was never called.
The only generated diff was the changelog; versions were already3.0.0.

Generated history repeated move announcements and calendar additions and
duplicated the unreleased3.0.0 section. Before publication, the section and
PR body are consolidated to the already-approved technical import and
calendar-free scope text. Historical2.0.2 and earlier notes remain intact.
The two retained sentences reuse the source PR's completed polish pass,
with their technical terms/claims unchanged. No runtime/package source or
dependency version changes accompany this prose correction.

## Receipts and limits

Raw logs live in SDK MAIN `.claude/artifacts/rebrand-qubrics-sdk344/`:
`mailbox-release-pr-prepare.log`, `pr380-created.json`,
`pr378-main-ci-watch.log`, and `calendar-free-9773d640-default/`.
This file is the source qualification handover before source-worktree removal.
Final candidate native/package/default/CI results and exact artifact hashes
are not claimed by this checkpoint; the combined publication packet must
measure them before asking for GO.

Rollback before publication: close the unmerged replacement PR, or normal
revert after an explicitly authorised merge. No public version can be reused;
PyPI yank is withdrawal rather than a full rollback and needs named GO.
Sending's existing environment hold remains operator-deferred and is not
re-requested. Obsolete PR330/PR326 remain non-pending; old Rust run stays
cancelled. No public release or package was created during preparation.

## Windows diagnostic reopening

Candidate333b146a CI44266029118 completed33/34 successful, with the real
installed `choco.exe --version` probe stopped by its existing20-second
deadline on Windows22. Same-code preceding main22 passed in2.768s;
this run's Windows24/26 passed in5.005s/2.413s. Root cause is unconfirmed.
Earlier intentional sensitivity/syntax failures are expected test cases;
the final installed-version assertion is the actual failure.

Ops19:34 authorised stage timing and owned process/thread wait-state
capture in the existing native probe before the unchanged deadline.
The diagnostic preserves the original command,assertions and Windows Job
ownership; it does not fix the failure or authorise a rerun-as-fix.
Read-only process inspection follows Microsoft Get-Process documentation
and ProcessThread.WaitReason's requirement that ThreadState be Wait:
https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.processthread.waitreason .

Detailed trace and unchanged-code controls: SDK MAIN task
`pr380-windows22-cause-20261118.md`; raw logs in MAIN artifacts
`pr380-windows22-failed.log`, `pr380-windows24-success.log`,
`pr380-windows26-success.log` and `pr378-main-windows22-success.log`.
The diagnostic requires a fresh Windows22 run; no later candidate PASS
or confirmed origin fix is claimed here. Python package source/metadata
remain unchanged by this diagnostic.

Pre-push Spec/Standards review found and removed an independently owned
observer draft. Capture now runs inside the existing Job controller,
using current Job members and held-handle membership checks; no new child,
timer,wait or ownership-error suppression remains. Both final reviews
returned zero findings. Local JavaScript syntax,unchanged-workflow source
extraction and native-exit wiring checks passed; native execution awaits CI.

Diagnostic head092d1154 CI44270195093 completed34/34 successful jobs.
Windows22 job134684578463 returned Chocolatey2.7.5 with command PID at901ms,
first output2634ms,controller close2740ms and confirmed ownership2742ms.
The10s snapshot did not fire; this passing control does not identify or
remove the original hang's cause. Raw stages are in MAIN artifacts
`pr380-092d1154-windows22.log:2675-2687`.

Review corrections remove the incomplete-snapshot marker stage and name
controller closure accurately. The existing100ms enumeration deadline is
shared across process/thread collection,with stop checks and an explicit
truncation marker; a partial controller PID entry survives enumeration
failure or expiry. Thread CPU sampling is omitted: .NET Framework's
ThreadState/WaitReason use the enumerated record,but TotalProcessorTime
reopens the thread by ID,which could have been reused:
https://github.com/microsoft/referencesource/blob/main/System/services/monitoring/system/diagnosticts/ProcessThread.cs .
No command,assertion,20s deadline or shutdown ownership change accompanies
these diagnostic corrections. Native capture and exact-head CI remain
unqualified until their own receipts exist; no original-hang fix is claimed.
Independent Spec/Standards reviews returned zero findings for these
corrections. The capture budget is cooperative: synchronous local OS reads
finish between deadline/stop checks; no stronger native bound is claimed.
Existing JavaScript syntax, workflow-source extraction and native-exit
wiring checks passed locally; no new harness or test was added.

## Approved capture qualification

Ops approved items1–4 of the bounded diagnostic continuation on18November
at20:46AEDT. Review comments4611562950 and4611577058 establish the two
diagnostic defects: an unchecked Job PID could survive truncation,and a
shutdown rejection discarded the in-memory stderr receipt. These defects
do not establish the cause of the original Chocolatey timeout.

The collector now obtains one cached `Process.GetProcesses()` collection,
filters current Job IDs,and verifies held-handle membership before emitting
any non-controller entry. Every process object is disposed,including filtered
objects. The controller PID remains present even when collection truncates.
Canonical cached enumeration is documented in the .NET Framework reference
source `Process.cs:1593-1600`:
https://github.com/microsoft/referencesource/blob/main/System/services/monitoring/system/diagnosticts/Process.cs .

Native probes append raw stderr to mode0600 files in a mode0700 OS-temporary
directory outside uploaded evidence. Successful probes remove that directory;
failed probes retain it only for the runner's lifetime. Complete
newline-delimited snapshot records are emitted
as they arrive,with the synthetic credentials redacted; arbitrary stderr,
arguments and environment are not dumped publicly. Shutdown rejection cannot
erase already-retained snapshot bytes. The existing cold-controller-start
case arms the same optional capture and records its actual stderr and stop
time in its copied fixture. Assertions require three complete captures with
controller identity and thread states,all completing before stop. Existing
ownership,output,exit and cleanup assertions remain intact.

This adds no test case,harness,observer,workflow or package-source change.
The100ms cooperative capture budget,the20-second native probe deadline,and
all shutdown guarantees remain unchanged. Local syntax,workflow extraction
and native-exit wiring passed. Native capture/stop ordering and the new
exact-head CI/default receipts still require measurement; their raw results
will live in SDK MAIN artifacts`pr380-a-qualification-*` and the MAIN task
checkpoint. No passing control is described as a fix of the original hang.
Final independent Spec/Standards reviews returned zero remaining findings
after the raw-stderr upload boundary and pre-enumeration stop guard were
corrected. No assertion,bound or workflow was weakened to settle review.
