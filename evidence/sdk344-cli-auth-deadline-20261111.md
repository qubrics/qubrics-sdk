# CLI authentication body deadline origin

## Failure and scope

PR326's unchanged Mailbox candidate `4f699ae351825c8e6e61fb4afbe833292168d962` failed [CI43007744817, macOS22 job130479349976](https://github.com/qubrics/qubrics-sdk/actions/runs/43007744817/job/130479349976). Only failed job/step: `node-runtime (macos-latest,22)` / `Run pnpm check:cli`. `failed.log` reports `Agent token exchange stalled during response body exceeded its request deadline`, through `check-cli.mjs:1628→1591`. Header stall passed in15014ms. The strict test requires both operation rejection and server-side response close before20000ms.

CLI source and this test have no changes in `2fee94d4...4f699ae3`; `agent-auth.ts`'s existing lifetime change originated in `b3f0129b` (2026-09-15). This separate fix starts from main `2fee94d413783d3b28528f6ec41448d3e8d05664`. Mailbox source, Python metadata, archives, workflow and remote release branch are untouched.

## Prior-run audit

`gh run list` records plus `gh run view --json jobs` for the20 preceding completed success/failure records show18 executions with54 macOS jobs, all SUCCESS. Two records42968121608/42961917572 contain no runtime jobs. No earlier same macOS stall was observed; passing history does not prove absence of an intermittent defect.

The18 executions:42983125000,42980734859,42967562873,42964860994,42961464785,42959741943,42958723285,42958705218,42957784360,42956612892,42956275209,42954543429,42952316994,42847014216,42844242009,42841371906,42838016157,42836644057. Existing reds in42958723285/42954543429 were Windows ownership-control steps; their macOS jobs passed. No rerun was used as a fix or as relief.

## Confirmed mechanism

The real exported `resolveAgentSendingToken` was looped against an HTTP fixture returning200, one `{`, and no end, using official Node22.23.4 macOS arm64 (bundled Undici6.29.1). Timings distinguish signal, pending `read`, `cancel`, operation rejection and server close:

- Baseline: signal abort15007ms; read remains pending; original20000ms guard fails. Only fixture teardown makes read/cancel reject at20013ms; operation and close finish20014ms.
- Forced GC reproduces the same result. External signal abort listeners fall2→1 before abort: the diagnostic listener remains, fetch's follower disappears. Timeout still fires, so this is not a timer deadline or close-event bookkeeping problem.
- Official immutable [Node22.23.4 Undici request source](https://github.com/nodejs/node/blob/v22.23.4/deps/undici/src/lib/web/fetch/request.js#L35) removes the external abort listener when the inner controller is finalised; lines425–457 retain that controller only through the request object and weakly follow the external signal. After headers, our consumer awaits the body without its own cancellation binding. GC can therefore leave the body read without a live abort follower.
- The same real OAuth body reader reproduced abort15005ms/read pending beyond20000ms, settling only on teardown. Header waits differ because the fetch request promise is still pending. GC timing explains intermittent platform/runtime occurrence and the preceding green runs.

The cause is at body consumption. Canonical primitives: [Node addAbortListener](https://nodejs.org/docs/latest-v22.x/api/events.html#eventsaddabortlistenersignal-listener) safely subscribes to the original signal; [reader.cancel](https://nodejs.org/docs/latest-v22.x/api/webstreams.html#readablestreamdefaultreadercancelreason) cancels pending reads and the underlying source. Both readers now own that binding and dispose it in `finally`. Agent registration/invite, exchange and readiness use the same agent reader and original per-request signal.

Cancellation resolves pending reads as done, so complete JSON in an unfinished HTTP body needs an explicit abort check before acceptance. A real OAuth probe saw `unexpected success` at15012ms without that check; `signal.throwIfAborted()` inside the existing safe-error catch prevents it. Existing15s auth timeout, readiness budget,256KiB limit, redirect rejection, safe error text, request count and retry policy remain intact.

## Verification

- Regression-first: existing `node --expose-gc scripts/check-cli.mjs` with GC during deadline waits failed on the original strict token-exchange assertion, exit1 (`regression-red.log`). No assertion or deadline was relaxed.
- Initial corrected token exchange under forced GC:3/3 operation+close completions15013,15005,15004ms, exit0. OAuth partial JSON:15015ms, exit0. Both signal and read/cancel/close boundaries were measured.
- Complete JSON boundary: red `unexpected success`; final abort guard makes OAuth reject with its existing safe message and close at15009ms, exit0 (`complete-json-green.log`). Permanent adjacent regression uses valid token JSON with an unfinished body through the existing agent-exchange seam; original partial-JSON test remains.
- Final normal `pnpm check:cli` on Node22.23.4 PASS, exit0:23/23 node:test cases, zero skipped; every CLI journey assertion passes. The strict header, partial-JSON body and valid-JSON unfinished-body cases reject and close at15004,15003,15002ms. TypeScript project build and `git diff --check` pass. Exact-head CI remains pending.
- Independent final Spec review:0 findings. Standards:0 hard breaches,0 heuristic smells. Test-only OAuth private import was removed; diagnostic proof remains local. No extra package export or dependency was introduced.

Raw outputs live in SDK MAIN `.claude/artifacts/rebrand-qubrics-sdk344/cli-auth-origin/`: `body-close-baseline.log`, `body-close-gc.log`, `body-close-listeners.log`, `oauth-body-red.log`, `regression-red.log`, `body-close-fixed.log`, `oauth-body-fixed.log`, `complete-json-red.log`, `complete-json-green.log`, `cli-final.log`, and immutable Node source files. Run inventory: `pr326-cli-recent200-runs.json` in the parent artifact directory. Temporary probe instruments only test fixtures and is not shipped.

## Release boundary

This fixes the already-specified bounded CLI operation; it adds no new command, public option, error contract or package version. Rollback is a normal revert. Source merge, exact-head CI and main gates remain to be measured. No tag, upload, publication, environment approval, registry mutation, force update or change to sdk343 occurred.

README check: current main still describes Python Sending as pending; its already-prepared correction is in held Mailbox4f699ae3, so this CLI-only PR leaves that owned release change intact. #344 remains3/24 public; all other publication and Go holds remain.
