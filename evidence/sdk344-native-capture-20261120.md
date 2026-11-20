# Native Windows capture receipts

Scoped measurement under #344, approved by Ops 20 November 2026. This
diagnostic does not claim to fix the installed Chocolatey wait.

Main CI 44678320912 at Rust source merge 873369bb failed only Windows22
job 136095389651. Its public artifact 14603971155 records an installed
`choco.exe --version` timeout at the unchanged 20 s bound, successful Job
shutdown/configuration recovery, and no orphan. The safe pre-stop snapshot
was truncated and retained only controller PID 6684. The native process's
inner wait remains unconfirmed.

The receipt gap has two origins:

- `windows-consumer-command.mjs` already emits the spawned native child
  PID, but `runCapturedProcess` did not retain it separately from the
  PowerShell controller PID.
- The Windows snapshot retained confirmed identity handles privately,
  then appended process details only after enumeration. An exhausted
  capture budget could therefore leave only the fallback controller row,
  without showing which existing capture phase consumed that budget.

The two-file change preserves the existing native event's validated PID,
the already-public state object, capture phase timestamps, Job query IDs
and handle-confirmed partial identities in the existing sanitized JSON.
No command line, environment value, raw stdout or raw stderr is newly
published. The existing output/synthetic-credential sanitizer remains.

Command, every existing assertion, native 20 s bound, cooperative 100 ms
capture budget, single cached enumeration and ownership operations are
unchanged. No observer, test case, harness, dependency or workflow added.
Installed version and transaction remain the existing native cases.

The previous artifact's metadata proof was red before this change:
`jq -e '.version_process | has("native_child_pid") and has("windows_probe_state")'`
returned `false`, exit 1. This proves missing diagnostic metadata, not a
reproduction/fix of the native wait. Fresh Windows CI owns the positive
native artifact proof. Local JS syntax, existing command-shim/workflow
wiring and whitespace checks passed; no native Windows result is claimed
from macOS.

Raw receipts are in SDK MAIN
`.claude/artifacts/rebrand-qubrics-sdk344/native-capture-20261120/`:
`prior-artifact-metadata-red.log`, `focused-wiring.log`, install/commit
logs, PR/main watcher logs and downloaded Windows artifacts. The preceding
full failure trace is in the owner task's
`rust-main-windows22-blocker-20261120.md` and linked raw files.

Required path: independent review and exact-head normal CI; normal green
merge; one authorised failed-main-Windows22 rerun labelled
**relief:+measurement**, then actual wait trace and origin repro red→green.
The relief run is not a fix. Release Please PR359/380 labels remain
unchanged until their separate cited proposal is decided. No upload,
tag, release queue, registry or publication action is included.

Rollback: normal revert of this diagnostic PR. #381 remains deferred.
