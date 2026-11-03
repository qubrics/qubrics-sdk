# Calendar event lifecycle factories

Status: source/tests only; three event factories ready for #904 to cherry-pick. Calendar-create lifecycle remains blocked. No push, credential read, live run, send, production change or publication.

## Scope and ownership

The existing runner now prepares `mailboxCreateCalendarEvent` (`create_cleanup`), `mailboxUpdateCalendarEvent` (`update_restore`) and `mailboxDeleteCalendarEvent` (`destructive_cleanup_only`). Each requires the dedicated, preflight-verified mailbox and discovers one calendar with `limit=1`. Each creates one event with an immutable random UID; no attendees or sending fields are supplied.

Update and delete scenarios create their own event rather than changing discovered events. Mutation requests carry the ETag returned by GET. Update verifies the canonical `{id, updated: true}` acknowledgement, reads back the new title and ownership, and restores the original title. Cleanup reads the captured event ID, checks UID and mailbox, deletes with its current ETag, then requires a not-found readback. The existing recovery ledger accepts `event_id` paths.

An uncertain create is never replayed. Its teardown fails loudly when no confirmed result is available. A returned foreign UID prevents deletion; uncertainty is not reported as cleanup success.

## Review findings fixed at origin

- PATCH response: `MailboxCalendarEventUpdatedResponse` at `packages/python/mcp/sendmux_mcp/openapi/openapi-app.json:3029` contains `id` and `updated`, not the full event. The factory now verifies the acknowledgement and GET readback. The local HTTP fixture returns that canonical acknowledgement.
- Child recovery: `scripts/live-e2e-contract.mjs:7` deliberately restricts journals to selected identifiers. The runner registers cleanup from the recovered event ID before processing full child output. Full-result validation remains in the factory, and cleanup checks UID/mailbox immediately before deletion. No journal fields or child harness were added.

Both independent review axes verified their findings resolved, with no remaining findings. Reviewers performed static checks only; the execution evidence below is the owner-run proof.

## Verification

Artifacts: `/Users/rj/Desktop/GIT-REPOS/sendmux-sdk/.claude/artifacts/calendar-api-sdk-tracer/`.

- Initial RED: `calendar-factories-red.log`, three failures before factory registration (`0/3` passed).
- PATCH contract RED: `calendar-patch-contract-red.log:43-46`, canonical successful update incorrectly reported `failed` instead of `passed`.
- Child journal RED: `calendar-journal-contract-red.log:47-51`, real Python child failed with `Calendar create UID mismatch` before cleanup registration.
- GREEN: `node --test --test-reporter=spec --test-name-pattern='calendar lifecycle' scripts/test-live-e2e-safety.mjs`, exit 0, `7/7`, zero skipped (`calendar-review-fixes-green.log`). Covers create through TypeScript and a real Python child, update/restore, delete, lost update response, uncertain create, and foreign-UID refusal.
- Static plan: `calendar-factories-static-plan-904-green.log`, exit 0, using #904's generated scenario registry read-only. The three event operations have owned factories and remain gated by default; calendar creation remains blocked. No assertions or safety gates were weakened. The first probe (`calendar-factories-static-plan.log`) failed because this WIP intentionally lacks the generated calendar scenarios owned by #904; that failed probe is retained, not a product failure or a green receipt.
- `node --check` for all three changed scripts and `git diff --check`: exit 0. The canonical pre-commit hook runs `pnpm drift:check`.

The first commit hook stopped before generation because its default `sendmux-docs/` input was absent (`calendar-factories-commit.log`). `normalize-openapi-for-codegen.mjs:8,69-76` supports `OPENAPI_INPUT_DIR`. The one commit retry uses the clean retained `/Users/rj/Desktop/GIT-REPOS/sendmux-docs-calendar-tracer-v6-release` checkout at `27787b3e`, with both hashes matching the earlier SDK evidence exactly. Native retry log: `calendar-factories-commit-with-input.log`; no hook bypass or snapshot change.

Loopback HTTP servers and test directories were closed/removed and verified by the test helper. No build was run and no build cache was created by this batch. Previously retained caches stay recorded in the task plan.

## Blocking fourth factory

Canonical OpenAPI exposes GET/POST `/mailbox/calendars` and only GET `/mailbox/calendars/{calendar_id}` (`openapi-app.json:14574,14908`). It has no `mailboxDeleteCalendar` operation. Calendar creation cannot truthfully satisfy `create_cleanup` using the supported public API.

Do not register a no-op factory, claim all four complete, alter `blocked === 0`, leak a calendar, delete the mailbox, or call a private backend to conceal the gap. The minimal dependency is a supported empty-calendar DELETE capability in the API and generated clients; that capability is not implemented by this source/tests handoff. Its scope/sequence goes back to Ops Watch.

README package/install/public-interface facts are unchanged by these internal runner factories. Existing rebrand inconsistencies remain with #904.
