# Concurrent CLI registration fixture

Source-only fix for the Management release gate discovered in SDK #343.

## Failure and cause

Management PR337 head `96d26459dc6637be1b698daeabaa5f963307c4e5` failed [CI42558076856](https://github.com/qubrics/qubrics-sdk/actions/runs/42558076856/job/128968178867): Ubuntu Node26.13.0, `Run pnpm check:cli`, reported `concurrent agent:register failed` with HTTP500. The other33 CI jobs passed; CodeQL passed6/6. No rerun or release merge.

`scripts/check-cli.mjs` validates the saved registering profile and idempotency key, then previously delayed the first response by100ms. That delay does not establish that the peer has sent its request. `packages/ts/cli/src/agent-auth.ts` legitimately reuses an already-active profile, or activates it after a successful identity response. A late peer can therefore skip its POST, or arrive after its earlier decision to POST while the profile has become active. The fixture then sees one request, or rejects the active state with500. This is fixture ordering, not an app-server failure. The transport reports a generic500 because the fixture supplies `error` rather than the `error_description` read by `agentAuthFailureMessage()`.

Original CI did not expose which of the fixture's two500 predicates fired. Two unchanged local diagnostic runs passed on Mac Node24.22.1 and26.12.1; neither is claimed as reproduction or repair of Ubuntu26.13.0. A third, explicitly changed scheduling probe removed only the artificial100ms response delay and retained every assertion. Node24.22.1 then failed the existing concurrency assertion with a one-element idempotency-key list: both CLI commands succeeded, but the late peer reused the active profile without another POST. This measured the missing overlap guarantee; the original CI500 predicate remains unmeasured.

Raw receipts: `.claude/artifacts/rebrand-qubrics-sdk343/management-3.0.0/node-ubuntu26-red.log`, `pr-ci-failed.log`, `local-cli-trace.log`, `local-cli26-trace.log`, `local-cli-zero-delay-probe.log`. The scheduling probe and both temporary diagnostic logs in source were removed before the fix.

## Origin change

The fixture now withholds both identity responses until two requests have passed the unchanged saved-profile and matching-key checks. This makes the overlap explicit before either CLI can activate the shared profile. The existing assertions still require two successful CLI results, exactly two requests and one shared nonempty key.

Canonical precedent: `scripts/test-cli-oauth-login.mjs:54` waits for the registration pair after validating persisted state; introduced in801a4262. No production CLI logic, assertion, retry, version or workflow change. The100ms delay is removed, not enlarged. Existing authentication request deadlines and `server.closeAllConnections()` retain failure/cleanup bounds.

## Validation

The original `pnpm check:cli` command passed locally after the barrier change: generator tests and the complete CLI fixture, including both concurrent registrations and matching-key assertions. Log: `management-3.0.0/local-cli-origin-green.log`. This is a new source input; the earlier passing diagnostic runs are not used as repair evidence. Exact-head source PR CI is required before merge and is recorded in the PR checks. No new harness or test, and no assertion removed or relaxed. No npm write, login, deprecation, workflow rerun, job approval or release-PR merge.

Mailbox run42538273966/job128920751174 remains under its already-boarded operator approval; the read-only watch continues. Management remains open and unmerged; its prepared archive and candidate receipts are historical qualification of96d26459, not final tagged publication proof.
