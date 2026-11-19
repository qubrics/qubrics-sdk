# Management 3.0.0 calendar-free candidates

Operator 1A, 19 November 2026, authorises preparing and qualifying
`qubrics-management 3.0.0` for PyPI and RubyGems. Uploads, tags, publication,
environment approvals and all other held releases remain unauthorised.

## Cause and correction

Both Management generators followed `WebhookEventPayload.oneOf` and its
`calendar.changed` discriminator into two calendar-specific models. The
Management API has no calendar endpoint, but those models and event enum
values exposed calendar clients through its webhook surface.

Canonical per local SDK AGENTS.md: filter at the generator input and
regenerate. Both generators now call `withholdManagementCalendar` before
their existing reachability pruning. The filter removes the calendar union
branch, discriminator mapping and request event enum value. Response labels
remain plain strings so an existing subscription or delivery record does
not break a mixed list. No calendar-specific response type is generated. Raw snapshots,
the live API, other language surfaces and mail webhook fields are unchanged.

Management versions and the manifest agree on 3.0.0. Python generated runtime
versions come from the existing generator. Both umbrella SDK dependency
metadata files follow Management 3.0.0, without releasing either umbrella.

Ruby's former Core range `>= 1.3.0, < 2.0` excluded the intended Core 2.0.0.
Its new range is `>= 1.3.0, < 3.0`: it accepts Core 2.0.0, retains compatibility
with the unchanged workspace Core 1.3.0 and rejects Core 3.0.0. The official
Bundler lock command updates only Management's version and the two affected
dependency entries. No Core source or other surface dependency is changed.

## Red and green

Review identified that removing the response enum value rejected existing
subscriptions. The public subscription round-trip first failed with a Pydantic
`ValidationError` for `calendar.changed`. Filtering now removes response enum
restrictions, retaining string typing and existing record labels without
calendar-specific client code. The adjacent mail label round-trip remains.

Python's public-import regression was red with
`AssertionError: assert not ['CalendarWebhookEventData', 'CalendarWebhookEventPayload']`.
Ruby's public constant regression was red with the same two exported models.
The native gem dependency check separately failed with
`Core 2.0.0 excluded by >= 1.3.0, < 2.0`.

After generation, Python webhook tests pass 7/7. Ruby Management validation
passes 6 tests / 31 assertions, zero failures or skips. The adjacent mail
boundary round-trips the canonical payload unchanged, and mail subscriptions
remain available. Calendar query enum validation rejects the withheld event.
Core 2.0.0 is accepted and 3.0.0 excluded by the actual gem specification.

The first Ruby assertion incorrectly expected the generated array constructor
to enforce item enums. The existing generator does not promise that behaviour;
the regression instead invokes the public API's existing enum validation.
Local Minitest also auto-loaded unrelated installed Rails plugins, creating a
`Rails` module without a logger. TracePoint located the source in installed
`railties-8.0.1/lib/rails/test_unit/`. The documented Minitest
`MT_NO_PLUGINS=1` isolates the local invocation. No SDK runtime workaround or
CI change was made. Official CI retains Ruby 3.4.12; local probes use installed
Ruby 3.4.1. Local RuboCop's new class-length finding is fixed by shortening
the new assertion, without changing thresholds.

## Publication boundary

No new README or release note announces the brand move. Package installation
instructions and calendar capability exclusions are factual usage guidance.
Both pre-publication README notices were removed. The changelog states the
import/require form and withheld capability without a move announcement.
No gem post-install message or Python install hook is added.

Candidate CI, default Skills acceptance, clean native artifact installs and
the exact file manifest will be recorded in the operator packet under SDK
MAIN `.claude/tasks/rebrand-qubrics-sdk344/`. Until then candidates are not
publish-ready. Source rollback is a normal revert. Once published, PyPI and
RubyGems versions cannot be overwritten or reused; yank is withdrawal only,
requires separately named approval and is not a complete rollback.

Raw logs: SDK MAIN `.claude/artifacts/rebrand-qubrics-sdk344/management-*`.
This evidence does not claim #344 completion or authorise any public write.
