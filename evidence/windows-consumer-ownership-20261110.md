# Windows consumer teardown origin investigation

Ops allocated the Windows consumer-ownership origin blocking Ruby PR368 to SDK343 on 10 November. Scope is one source-only PR from main; sdk344 branches/diagnostics remain unchanged. Homebrew cooldown is a separate hold.

## Measured red and remaining gap

Ruby PR368 head764f0a8daa04e2d5feb5ca8fea37ed990b74edae, CI42814426845: all three Windows Node22/24/26 jobs failed `Prove Windows command control sensitivity`.

- Node22 job129823751073: started-never-ready fixture did not become ready, controller4728 shutdown unconfirmed, then owned workspace removal EBUSY; diagnostic aborted with one result instead of three.
- Node24 job129823751077 and Node26 job129823751445: healthy PowerShell leader-exit scenario recorded leader/descendant absent and separate owned workspace removed, then fixture-root removal EBUSY. Existing lock artifacts say `No matching handles found.`; their CIM snapshots do not prove a holder.

Raw immutable evidence is retained by sdk344 under SDK MAIN `.claude/artifacts/rebrand-qubrics-sdk344/`: `pr368-ci-42814426845-failed.log`, `ruby-windows-{129823751073,129823751077,129823751445}.log`, `windows-fixture-locks-node24.zip`, `windows-fixture-locks-node26.zip`. Routing note: `.claude/tasks/rebrand-qubrics-sdk344/ruby-windows-origin-blocker.md`. Source baseline864a156284f94d5f0888cbf8ca99ef2b02e4557c.

Initial change closes the capture gap only: use the unique directory basename, rather than full8.3-path spelling, as Handle's name fragment; catch owned-workspace EBUSY as well as fixture-root EBUSY. Both paths still throw the original error. No rm retry, sleep, timeout/deadline increase, assertion relaxation or skip. Existing Windows CI/sensitivity workload and14-day lock-artifact retention remain unchanged.

Canonical capture semantics: [Microsoft Sysinternals Handle](https://learn.microsoft.com/en-us/sysinternals/downloads/handle) documents case-insensitive substring matching anywhere in a handle path. [SetCurrentDirectory](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setcurrentdirectory) documents that a running process locks its current directory against deletion, movement and rename. These explain the required evidence and lookup shape; neither proves the unknown EBUSY holder.

Status: investigation in progress. Holder not yet confirmed; no causal fix claimed. Existing issue365 remains open. Required completion: holder PID/image/cmdline/parent and handle/path tied to owning source, origin removed, original assertions retained, Windows22/24/26 sensitivity clean, normal merge and mainCI readback.

PR371's first capture head `22c5b3dd8bc3b750b62ef2cda71f262b531db414` passed normal CI [42820359874](https://github.com/qubrics/qubrics-sdk/actions/runs/42820359874), 34/34 jobs. Each Windows Node22/24/26 job passed 16 sensitivity verdicts, with zero actual fixture-lock captures. This is inconclusive about ownership and does not justify a causal fix or merge.

The next capture calls Handle64 directly before starting PowerShell, removing the cold-PowerShell gap from the first handle lookup. It also maps live handles to recorded PIDs immediately before each existing trigger (or before terminating a started fixture that missed readiness). Files use the existing `fixture-lock-*.log` artifact collection. The original workloads, assertions, cleanup attempts, deadlines and errors remain unchanged. This is observation only; neither an extra live holder nor a later green run alone establishes the EBUSY cause.
