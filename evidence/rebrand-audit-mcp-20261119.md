# npm MCP display branding

Tracks qubrics/qubrics #1092. Source prepared; merge and the next eligible package release remain coordinated by the parent rebrand task.

## Cause and change

`packages/ts/mcp/package.json:4` supplies the npm description and the package README supplies its title and setup prose. Both retained Sendmux display copy. Change those descriptions to Qubrics and point the guide link at the canonical docs.

Preserve `sendmux-mcp`, its executable, `io.github.Sendmux/sendmux-mcp`, the fixed compatibility endpoint `https://mcp.sendmux.ai/mcp`, and the released Python package link. Runtime files, versions, dependency metadata and release configuration are unchanged.

## Verification

- Live npm response before publication: `sendmux-mcp` 1.0.0 still has the old description; retained as `.claude/artifacts/rebrand-audit-fixes-ecosystem/npm-before.json` in the owning local checkout.
- GitHub's ordinary GFM Markdown response renders the Qubrics title and prose; retained as `mcp-readme-render.html` in that artifact directory.
- `pnpm --filter sendmux-mcp build` passed its executable syntax check.
- `pnpm --filter sendmux-mcp pack --pack-destination .claude/artifacts/rebrand-audit-fixes-ecosystem` passed. Inspection of the resulting tarball confirms the Qubrics title/description and unchanged package name, version, executable and MCP ownership marker.
- `git diff --check` passed. No runtime logic changed, so no new tests were added. Full package CI remains the release gate.
- Read-only `node scripts/verify-sdk-staleness.mjs` passed; no Rust changes exist. Fresh-reader critique and one humanize pass preserved the exact compatibility names and existing claims.
- Operator approved one scoped commit-hook relief because the unconditional pre-commit command regenerates held Rust provenance. Scoped build, package inspection, ordinary render, whitespace and read-only staleness checks passed first; required PR CI remains the gate. No Rust or generated-runtime file changed.

## Release and rollback

Existing lane: the `ts-mcp` component in `release-please-config.json` prepares the next eligible release. `.github/workflows/release-please.yml` guards the immutable producer, runs `publish-npm` via `pnpm publish:npm:ts`, and follows with the existing `publish-mcp-registry` job. Existing publication and registry holds remain in force; this PR bypasses none.

Source rollback: revert this PR. npm rollback anchor: existing `sendmux-mcp@1.0.0`; restore the `latest` dist-tag to that version if needed. Published versions remain immutable. Verify the exact new registry version, README and description after the coordinated release before closing #1092.
