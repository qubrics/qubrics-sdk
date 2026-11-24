# Python Mailbox replacement candidate

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

## Replacement metadata

Official installed Release Please17.6.0 `Manifest.fromManifest` and
`createPullRequests` created PR380 at
`c15666a0ac68d597aea1f60b5a4be6827e29d452`, scoped only to
`packages/python/mailbox`, explicit releaseAs3.0.0. No persistent release-as
key or workflow changed, and `createReleases` was never called.
The only generated diff was the changelog; versions were already3.0.0.

## Receipts and limits

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

## Bounded correction after the capture qualification

The one A qualification at bfb4ff01,CI44281264413,finished33/34 successful
jobs. Windows22/24 proved three captures before the recorded stop;Windows26
failed the new thread-array assertion. Its first capture took544ms and
explicitly reported truncation with zero threads;later captures had19 each.
The test had wrongly required threads even for permitted truncated records.
Red receipt:MAIN artifacts`pr380-a-qualification-failed.log:77,251-252,267`.
Original command/ownership assertions were not the source of that red.

Ops approved exactly items1–6 of the result packet as one bounded correction
batch and one fresh normal CI/default receipt. The same existing case now
accepts an explicitly truncated capture with controller identity,requires an
observed state in complete captures,and still requires an actual observed
controller state across the three captures. No test case was added or removed.

Private stderr setup precedes controller start. Append errors are retained
as failures while stderr draining,snapshot parsing and owned shutdown continue;
retention is asserted only after confirmation. Failure-retained paths are
reported without file contents. A complete known JSON snapshot can follow
unterminated descendant stderr on the same line;both existing readers now
extract the known record without emitting the preceding bytes.
The later public version log and uploaded probe summary also omit raw stderr;
the in-memory receipts used by every existing assertion remain complete.
The uploaded transaction summary also omits its serialised stdout receipt,
which otherwise embeds child stderr as a string;parsed safe fields remain.

Non-controller Job handles are verified and retained BEFORE cached process
enumeration,then disposed with every cached object. This prevents cached
thread data from being paired with a later process reusing the PID.
Canonical lifetime rule:an open handle retains its process object and PID,
https://devblogs.microsoft.com/oldnewthing/20110107-00/?p=11803%2F .
The .NET cached collection is documented in Process.cs1593–1600 above.

Local syntax/native-exit wiring passed. The next exact source/default/native
receipts remain unclaimed until measured. Command,ownership assertions,20s
deadline and cooperative100ms budget are unchanged. No new harness,observer,
workflow,package source or frozen artifact changed. Original Chocolatey hang
remains UNCONFIRMED. If this one new CI is diagnostically red,Ops requires
STOP with its cause and the option to hold PR380;no further corrections.
Final independent Spec/Standards reviews returned zero remaining findings
after checking both the direct and embedded stderr publication paths.

## Last approved diagnostic correction round

A2 head3487b543 qualified CI44286733673 SUCCESS34/34,zero skipped;
all42PR checks passed and defaultlatestv2.0.5 accepted22 results.
Nine cold captures retained controller identity,including permitted partial
captures on Windows24. Native version commands completed before10s on all
three Windows runners. These controls did not reproduce or explain the
original333b146a20s timeout. Full measurements and six late review traces:
SDK MAIN task`pr380-a2-qualification-result-20261118.md`.

Ops authorises one LAST code round for those six routes,then one normal
CI/default receipt. The existing copied cold-start fixture now records each
controller's PID/workspace/start and its actual scenario release or stop.
Each scenario must match exactly one capture in that controller's lifetime
before its own trigger;the aggregate count is no longer the ordering proof.
Existing output,exit,ownership,partial-capture and actual-state assertions
remain. No scenario,test,harness or observer was added.

Artifact serialization redacts known credential sentinels in every retained
string,including version and child stdout on assertion failure;original
in-memory assertions and config recovery remain unchanged. Stderr append
errors are reported alongside rejection without replacing the original
shutdown error. Private stderr survives owner confirmation and all caller
validation;success removes it only after the whole probe passes. Empty
storage is removed if file setup or controller startup throws.

Held Job identities now use the existing Win32 OpenProcess binding with
QUERY_LIMITED_INFORMATION and verified membership,before the one cached
GetProcesses enumeration. Every held handle is closed in finally.
Canonical trace:official .NET Process.cs1512-1515 calls IsProcessRunning;
ProcessManager.cs219-226 enumerates process IDs for every GetProcessById.
https://raw.githubusercontent.com/microsoft/referencesource/main/System/services/monitoring/system/diagnosticts/ProcessManager.cs
Removing those repeated scans preserves identity without extra enumeration.
It is not evidence that these scans caused the original timeout.

Local syntax,workflow source extraction and native-exit wiring passed.
Independent Spec and Standards reviews returned zero findings for this
four-file batch. Fresh native CI/default results remain unclaimed until
measured. Effective Windows ACLs and targeted prefixed/split-chunk/
slow-reader failure coverage remain unverified under the scope limit.
20s native deadline,cooperative100ms capture budget,ownership guarantees,
workflows,package source and frozen artifacts are unchanged.
Diagnostic-caused red means STOP. New findings from this final push get
in-thread disposition and ONE follow-up issue rather than another code
round,except a confirmed credential leak or break in the diagnostic itself.
Rollback is revert;no merge,tag,upload or publication is authorised.
