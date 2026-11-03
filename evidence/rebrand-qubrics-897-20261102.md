# A15 GitHub references and approved A17 README handoff

Part of qubrics/qubrics#897. Base: 0dd32a2652f3fd7a9a8f7e2ab8976d79f1b1dc99. Current GitHub consumers, strict repository guards, package repository metadata, generated Ruby homepage source and current installation/support instructions use the canonical Qubrics repository identities. Internal package names and service hosts remain unchanged except the exact separately authorised A17 README patch.

The exact patch was applied verbatim after a successful independent check and confirmed by reverse check:
`/Users/rj/Desktop/GIT-REPOS/sendmux/.claude/artifacts/rebrand-qubrics-904/sdk-readme-a17.patch`
SHA256: `ec4d09b802194c50acbdd3c5b27bbda12e0a8033a7fa637f3b6e6374478631fc`.
No other A17 edits were invented. Runtime counterparts remain owned by #904.

Strict publication reads now target `qubrics/qubrics-sdk`. PHP split publishing accepts only exact canonical SSH/HTTPS package repository origins. Immutable npm attestations retain the exact former producer identity alongside the current identity; the dependency source must match that same identity and exact producer commit. Unrecognised identities, mixed identities and wrong commits remain rejected. Historical provenance and changelog evidence remain intact.

Existing tests at the guard seams were seen red before the fixes:
- Current Snap release: `Missing producer release tag: ts-cli-v1.2.3`, then `Snap npm provenance does not identify the CLI producer commit`.
- PHP split remote: `Split origin does not identify the expected package repository`.
- Current/historical Snap cases and wrong-commit/unknown/mixed rejection cases pass; official release construction test passes after frozen dependency installation resolved missing release-please.
- PHP split/canary tests: 20 passed, 0 failed/skipped. Existing Snap workflow and Chocolatey package-file checks pass.
- Build-dependent connections tests could not start in the fresh worktree because `@sendmux/sdk/dist/index.js` was absent; they remain for normal SDK CI after its build. No stale dist copied, no assertion weakened.
- `git apply --check`, patch application, reverse check and `git diff --check`: exit 0.

Logs and exact commands: control-plane MAIN `.claude/artifacts/rebrand-qubrics-897/sdk-state.md` and referenced logs. Independent Standards/Spec reviews found no functional source defect in the bounded A15/A17 diff.

The original normal commit was blocked by `ogen failed to infer fields discriminator` on the newer current contract. The separate approved prerequisite fixed the API schema origin, PHP generation and missing Calendar lifecycle inputs: docs80 merged `12ef5105`, API917 merged `e0462ea3`, SDK346 merged `276082cb`, all exact-head CI green. This row4 branch rebased onto `276082cb`; the original 69-file patch is preserved, with its already-shipped CI URL hunk leaving 68 remaining files. README handoff reverse check remains exit0. No older-contract substitution or bypass.

Post-merge Release Please run `41571510043` failed `Unexpected publication repository`: main `scripts/publication-guard.mjs:14,231` still requires `Sendmux/sendmux-sdk`, while GitHub identifies the renamed repo as `qubrics/qubrics-sdk`. This existing row4 origin correction targets canonical reads and preserves strict equality. No rerun, release threshold or guard bypass. Merged PRs labelled `autorelease: pending` were empty before qualification; no package version/manifest changes are in this diff. Publication remains gated separately.

No hook bypass, assertion weakening, publication, release tag or deploy performed. Full normal generation/commit hook and final exact-head CI remain required for this branch; API917 production deployment queues after898 and requires its own slot/GO. Rows2/5 stay held902.

After rebasing onto the merged generation prerequisite, focused guard/canary/PHP fixtures passed: 87 tests, no skips, exit0 (`row4-guards-green.log`); existing Snap workflow check exit0 (`row4-snap-green.log`). Final independent Standards/Spec reviews found zero issues. Original handoff patch remains verbatim and reverse-checks exit0.

Ops requested the Ruby generator path for #904's A17 upload-auth guard. Its one-line canonical homepage hunk is committed separately at `a2073b17568512abfdf004c1bd99eadeb541b8a4`, with normal full drift hook exit0; only that lease was released. The first isolated-commit attempt correctly detected the MCP provenance hash derived from other uncommitted `pyproject.toml` edits. Temporarily isolating those edits let the Ruby-only commit qualify against matching inputs; all remaining changes were then restored. The regenerated MCP contract hash accompanies its changed package metadata in the remaining commit. No current-input substitution, provenance bypass or generated-file hand edit.

The generated MCP contract was committed normally in `688af4ae13e537690ac0376ce2bfde15fefde7e2` and its lease released to #904; no other derived Python/MCP output remains claimed. Normal full drift hook exit0 is recorded in `row4-commit.log`.

CI run `41572995229` selected the stale matching docs branch `42e4027` through the existing current-input resolver (`.github/workflows/ci.yml:25-46,142-164`). That branch lacked merged docs80: Go failed discriminator inference, MCP lacked `mailboxDeleteCalendar`, and PHP lacked the two named webhook payload models. The clean owned docs branch was merged with current main and pushed at `f363ed53`; its OpenAPI inputs byte-match main `12ef5105`. Resolver and assertions remain unchanged.

The same run's Python matrix and Ruby checks enforced existing changed-package dependency floors after this PR edited their metadata (`scripts/python-release-guardrails.mjs:53-66,118-123`; `scripts/check-ruby.mjs:55-95`). LangChain's mailbox floor is corrected to the manifest's `2.0.2`; Ruby SDK mailbox/management floors to `2.0.2`/`2.0.1`, with `Gemfile.lock` regenerated by `rbenv exec bundle lock --local` (exit0). Both existing floor validators were seen red, then all Python and Ruby package floors passed (exit0 each; `row4-{python,ruby}-floor-{red,green}.log`). No policy or test weakened, no new harness. Every failed job is retained in `row4-ci-all-failed.log`.

Polish pass: skipped — exact technical-token corrections and approved verbatim handoff.
