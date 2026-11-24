# Management 3.0.0 candidate qualification

Operator 1A, 19 November 2026, authorises preparing and qualifying
`qubrics-management 3.0.0` for PyPI and RubyGems. Uploads, tags, publication,
environment approvals and all other held releases remain unauthorised.

## Cause and correction

Management versions and the manifest agree on 3.0.0. Python generated runtime
versions come from the existing generator. Both umbrella SDK dependency
metadata files follow Management 3.0.0, without releasing either umbrella.

Ruby's former Core range `>= 1.3.0, < 2.0` excluded the intended Core 2.0.0.
Its new range is `>= 1.3.0, < 3.0`: it accepts Core 2.0.0, retains compatibility
with the unchanged workspace Core 1.3.0 and rejects Core 3.0.0. The official
Bundler lock command updates only Management's version and the two affected
dependency entries. No Core source or other surface dependency is changed.

## Red and green

Ops subsequently approved the explicit Management-only root correction. Both
generators now complete (exit 0), restoring the mail exports. Focused Ruby
public tests pass 7 runs / 35 assertions with zero failures, errors or skips.
Focused RuboCop reported one trailing EOF blank line in
`packages/ruby/tests/test_management_validation.rb:122`; `git diff --check`
confirmed it. Ops classified it as lint and approved removing only that
blank line. Both checks now exit 0. No assertion was weakened.

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

Candidate CI, default Skills acceptance, clean native artifact installs and
the exact file manifest will be recorded in the operator packet under SDK
MAIN `.claude/tasks/rebrand-qubrics-sdk344/`. Until then candidates are not
publish-ready. Source rollback is a normal revert. Once published, PyPI and
RubyGems versions cannot be overwritten or reused; yank is withdrawal only,
requires separately named approval and is not a complete rollback.

Raw logs: SDK MAIN `.claude/artifacts/rebrand-qubrics-sdk344/management-*`.
This evidence does not claim #344 completion or authorise any public write.
