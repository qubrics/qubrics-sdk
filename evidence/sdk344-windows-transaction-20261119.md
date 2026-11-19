# Windows config-transaction measurement

Goal: retain safe inner-wait phase receipts and sanitized native-probe JSON
for the next Windows failure. This is diagnostic instrumentation, not a
confirmed fix for the original native wait. No package, registry, tag,
release queue or production workflow is changed.

## Origin and scope

Main run44499302232 at ddfae6ba initially passed34/35 jobs. Windows24
job135474519843 terminated the installed Chocolatey config transaction at
its unchanged20s deadline. Version probing passed. The complete job API
log (2329 lines/362314 bytes) contained a deliberately truncated pre-stop
snapshot, only the controller PID. No run artifact contained the private
native stdout/stderr or sanitized JSON. Same-code Windows22/26 passed.

The single operator-authorised job rerun is labelled **relief**, not fix:
job135484510371 passed; main now35/35. Native transaction completed2232ms,
before the10s snapshot. This does not identify the original inner wait.
No further rerun is authorised or performed.

The failed path reads CI/Chocolatey workflow helpers, uses controlled
synthetic credentials and restores the runner's Chocolatey config. It
does not read or build Ruby Sending gem contents. Its frozen36352-byte
archive remains SHA256
`8dd5350aebf55dd588cc2c350dc906c3bb635f608b20dc7f71f0774455bee462`.
Ops explicitly cleared that independent upload gate; only the operator's
separately boarded publication decision remains.

## Smallest change

The existing installed probe emits six enum/PID phases: child started,
child exited, stdout read, stderr read, config restore started/completed.
The existing stderr line parser exports only those whitelisted names and
positive safe-integer PIDs. Timing reuses the existing monotonic stage
receipt. Native stdout/stderr and configuration bytes remain private.

Restore markers are inserted into the existing extracted helper's runtime
copy only; no release/publish/tag workflow changes. Native commands,
arguments, asynchronous reads, assertions,20s bound and ownership remain
unchanged. The existing CI uploader follows the native step and includes
only its already-sanitized installed-chocolatey-probe.json, with its
existing always condition and14-day retention. No harness, observer,
test case, threshold or public runtime behaviour is added.

## Verification

Local JavaScript syntax and git diff whitespace checks exit0. Existing
Windows command-shim and Chocolatey workflow-order tests exit0. No new
test or assertion was added, removed or weakened. Native Windows execution
is unavailable on this Mac; the single normal PR CI supplies that proof.
Independent review found raw child/version stdout in the exported copy
and a restore-completed marker outside finally. Both were corrected:
all stdout/stderr keys are omitted recursively, and completion is recorded
inside finally after successful byte restoration and staging cleanup.
Private assertions remain unchanged. Both independent reviewers then
reported zero findings. Fresh exact-source default receipt and normal CI
are pending at this source checkpoint.

MAIN task receipts are under `.claude/artifacts/rebrand-qubrics-sdk344/`:
`pr386-main-windows24-failed.log`, the22/26 control logs,
`pr386-windows24-relief-full.log`, and `windows-transaction-*-20261119.log`.
Detailed cause/approval state is in the corresponding MAIN task files.

Rollback: normal revert. Future failure evidence measures the native wait;
a green diagnostic run alone does not establish its root cause. Deferred
issue381 receipt-I/O/timestamp work is untouched.
