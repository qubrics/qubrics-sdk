# Pending Go release-note producer correction

Status: source PR preparation only; activation and publication require separate approval.

The existing producer omitted the pending Go path/version and recognised only
the Python release-note phrase. The correction reuses the same plugin for
exactly Go 4.0.0, with three path-specific wording replacements in both the
generated changelog entry and PR-body release notes. Existing assertions,
version checks, error handling and workflow entry points are retained.

Canonical trace at base `5fbe78d9f6f60efb531b32c58576144e0c0f65a4`:
`.github/workflows/release-please.yml:89–102` calls
`scripts/python-release-notes.mjs:7–20`, which updates both generated outputs.
The regression fixture captures PR329 at
`6b44445f986e3e627a011ab2bfe5ce000846cee1`; its input was compared with the
captured PR body and matched exactly.

Validation:

- New test: `Go release-note producer neutralises captured Go4 notes without changing other releases`.
- Red: `pnpm exec node --test --test-name-pattern='Go release-note producer' scripts/release-state-fixtures.test.mjs`, exit 1, `candidate 0 body must contain the scoped notes`.
- Green: the same file with `--test-name-pattern='release-note producer'`, exit 0, 2/2 passed, zero skipped.
- Related gate: `pnpm test:release-state`, exit 0, 43/43 passed, zero skipped.
- Syntax checks for both edited scripts and `git diff --check`: exit 0.
- Existing Python/Go phrase-boundary test is unchanged. New coverage checks both outputs, unrelated paths/versions, historical text, version object identity, PR-body framing and repeat-run idempotence.
- Tests removed: none. Tests exercise the plugin's public `run()` seam, using real release-note constructors.

The three replacements preserve the expected technical text and commit links.
No runtime or package-version change requires an install example or README update.

Raw receipts are local under
`.claude/artifacts/rebrand-qubrics-sdk344/go-note-producer-fix-20261122/`:
`red.log`, `green.log`, `release-state.log`, `captured-fixture.log` and `polish.md`.
Normal generation hook, CI on the final commit and independent review remain required.
