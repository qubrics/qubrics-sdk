# Calendar-free MCP 3.0.0 candidate

Owner approved source preparation under #344, option A in
`mcp3-calendar-free-source-ask-20261119.md`. No merge, upload, tag, release
queue, environment approval or registry write is authorised by this work.
Public #344 count remains 14/24, Ruby 6/10. The whole issue is incomplete.

## Source and package boundaries

The existing generator retains full producer snapshots at the unchanged
publication-guard paths. It also writes runtime_openapi projections with
the existing Management calendar payload/label policy, five Mailbox
calendar paths, 22 calendar schemas and two OAuth scope definitions removed.
Only runtime projections ship. Hatch excludes raw producer JSON in both
wheel and sdist, and the strict artifact checker rejects accidental raw
inclusion. Contract provenance binds every shipped runtime source and
projection. No guard, workflow, Skills source, fallback or pin changed.

Ten calendar tools and ten aliases are removed. Ordinary Mailbox and
Sending tool contracts are unchanged; Management schema differences are
limited to the already-approved opaque payload/plain-string label policy.
Credential precedence, legacy environment compatibility, tool aliases,
annotations and output-schema checks remain. Raw producer snapshots match
main byte-for-byte. This source split preserves genuine live equality
without packaging the held calendar API.

Canonical sources: local SDK AGENTS.md generator-origin/quality rules;
scripts/publication-guard.mjs:13,46-62; contract.py source_hashes/load_contract;
scripts/check-mcp-artifacts.py source-byte and installed-contract checks;
Hatch official docs/config/build.md via context7:/pypa/hatch (artifact
patterns bypass exclusions, so only runtime JSON is marked as an artifact).

## Measured checks

- New public-discovery/spec regression fails before filtering, with the
  calendar-name assertion false (mcp3-calendar-red-20261119.log, 1 failed).
- Initial existing native suite: 197 passed, one stale count failed, no
  skipped tests. Removal of ten tools and ten aliases changes the exact
  count from 150 to 130. Updated that count and affected calendar presence
  expectations to approved absence behaviour, preserving quality checks.
- Focused final metadata and calendar-absence checks: 2 passed in 2.64s.
  An initially over-tight new permission assertion was corrected because
  the public connection tool intentionally needs no scope; calendar names
  remain absent even with calendar.*. No permission rule was weakened.
- Mypy: no issues in 35 source files. Node contract tests: 19 passed,
  zero skipped. Syntax and git diff --check pass.
- The normal commit hook caught ten missing MCP include/exclude decisions
  after tool removal. Added the approved calendar exclusions at the
  existing coverage-policy origin and regenerated its matrix. No runtime
  code or frozen archive changed for this integration correction.
- Both archives build and pass Twine plus the existing strict native
  artifact checker, including installed-contract verification outside
  the checkout and process/fixture teardown confirmation.
- Final archive scan found inert calendar operation names in annotation
  lookup sets, despite zero exposed calendar tools. Removed those unused
  names, regenerated contract provenance and rebuilt. Final discovery,
  metadata and absence checks pass 3/3. Both final archives contain 25
  Python/JSON members, zero calendar text, and zero raw producer JSON files.
- Initial exact-head CI44523364859 passed 34/35 jobs; verify alone failed
  static live-E2E coverage because ten scenarios still named removed MCP
  adapters (failed log:29350-29361). Regenerated scenarios and matrix with
  the existing writer; only those adapters become null. SDK/CLI scenarios,
  assertions and safety gates remain. Direct coverage passes128 API plus
  two custom operations. Full static safety/audit check requires built
  workspace SDK exports; initial local invocation lacked them, corrected
  by the documented dependency build. Final check is running separately.
- Fresh isolated no-cache wheel install resolves public qubrics-core
  2.0.0. pip check passes. Installed load_contract equals the real factory
  tools/list result: 130 tools, no calendar tools, paths or schema names;
  app/sending defaults are app.qubrics.com/api/v1 and
  smtp.qubrics.com/api/v1. Import is from the isolated consumer.
  Initial smoke mistakenly called the source-only build_contract entry
  point, which requires pyproject.toml. The corrected installed proof uses
  load_contract plus the real tools/list collector; no source fix or
  replacement receipt was used. Both command logs are retained.
- Independent Spec and Standards reviews: zero findings. Fresh-reader
  changelog critique and one humanize pass preserve version/technical
  terms. No move announcement, registry announcement or install message.

Raw logs and files: SDK MAIN/.claude/artifacts/rebrand-qubrics-sdk344/,
prefix mcp3-final checks and mcp3-final-20261119/consumer-*.log. The first
archives are superseded evidence of the inert-name finding, never publish files.
Normal exact-head CI and default released Skills acceptance are the
remaining qualification gates; no inherited receipt claims this candidate.

## Frozen files for review, not publication permission

Directory: SDK MAIN/.claude/artifacts/rebrand-qubrics-sdk344/
mcp3-final-20261119/dist/.

| File | Bytes | SHA256 |
| --- | ---: | --- |
| qubrics_mcp-3.0.0-py3-none-any.whl | 231101 | 9ea85ab0acca29dfa638a8a6d54bc00dd06df38ecca8296e4158d0081ea47c31 |
| qubrics_mcp-3.0.0.tar.gz | 212794 | 4357427c8f90e7352245284597bf1be406c08179528a42ad7a7cf13c42f70b5d |

Calendar exposure: NO. Holding the whole release remains an option.
Source undo: normal revert. Eventual PyPI versions cannot be replaced or
reused; a separately approved yank cannot recall existing copies. The
silent sendmux-mcp pointer and MCP Registry remain separate later asks.
Release/publication holds are unchanged.
