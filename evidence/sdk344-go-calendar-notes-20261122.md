# Scoped Go release-note producer correction

Status: source PR preparation only. Merge and publication remain held.

Extend the existing Go 4.0.0 producer branch with six exact replacements for
seven captured note occurrences. Both generated outputs use the same helper.
Prior neutral mappings, path/version guards, runtime, package versions,
history and commit links remain unchanged.

Canonical trace at base `58840370d58a75da71cc0f65fb98ffafd6e039cd`:
`scripts/python-release-notes.mjs:8–21` updates the generated entry and body;
`.github/workflows/release-please.yml:99–102` invokes that producer.
The approved scope is the Ops 22 November rule 12 source correction.

Validation:

- Existing captured Go fixture is extended; no duplicate fixture or harness.
- Red: focused Go producer test exits 1, `selected Go4 body must exclude calendar notes`.
- Green: both producer tests pass 2/2 with zero skipped.
- Related gate: `pnpm test:release-state` passes 43/43 with zero skipped.
- Captured input exercises all seven occurrences. Selected full body and changelog require zero case-insensitive matches.
- All pre-Go tests, including the Python regression, and the raw Go input remain byte-identical to base.
- Existing checks preserve history, URLs, version objects, unrelated paths/versions and repeat-run idempotence.
- Syntax checks and `git diff --check` pass. No tests removed or assertions weakened.

Normal generation hook, final-head default-source qualification, CI and
independent review remain required. Runtime, package versions, install
examples and publication facts stay unchanged.

Raw receipts: `.claude/artifacts/rebrand-qubrics-sdk344/go-calendar-note-producer-fix-20261122/`
contains `red.log`, `green.log`, `release-state.log` and `preservation.log`.
