# Python native release metadata (#344)

Goal: complete #344 with merged source and measured published packages. This source change fixes native release preparation; it does not authorise publication. Rollback: revert this PR.

## Confirmed cause and fix

- Release Please 17.6.0's Python strategy updates `pyproject.toml`, then searches distribution-derived `qubrics_sending/__init__.py` or `src/qubrics_sending/__init__.py`; it does not find `qubrics/sending/__init__.py` and has no Python workspace dependency updater (`node_modules/release-please/build/src/strategies/python.js:74–110`). Frozen release PR357 reproduced `generated __version__ must match project.version`, `1.6.0 !== 2.0.0` (`python-native-origin-red.log`).
- Six dependent release PRs retained ranges excluding the specified next-major replacements. The original and refreshed immutable audits, with exact heads and all ten ranges, are `python-release-audit.md` and `python-release-audit-current.md` under MAIN's task artifacts. For example, sending required `qubrics-core>=1.3.1,<2.0.0` while A18 requires core 2.0.0.
- MCP's contract records both the native version and SHA256 of its complete pyproject (`packages/python/mcp/qubrics/mcp/contract.py:96–101`). Release PR328 changed the native version without regenerating those values. The Registry identity and top-level Registry metadata version are independent and remain unchanged.
- Existing SDK `AGENTS.md` requires fresh release-head review, generation/drift preparation, correct native metadata and sequential releases. Existing generators already own generated client versions (`scripts/generate-python.mjs:96–109`) and the MCP contract (`scripts/generate-mcp-contract.mjs:14–16`). The missing owner was dependency-floor generation.
- `scripts/sync-python-dependency-floors.mjs` now derives internal ranges from release manifest versions and declared Python package identities. `generate:python` runs it first. Existing native checks enforce all Python floors, and the drift gate covers their pyprojects. No workflow, default guard, release constructor, main manifest, source package version or Registry identity changes are included in this PR.

Canonical preparation: SDK local `AGENTS.md` release rules, the existing generators, and the explicit range policy in `scripts/python-release-guardrails.mjs:101–123`. Main's synchronisation is a no-op. Each actual release remains sequential: refresh its bot head after the preceding release, generate/review/commit native outputs, qualify that exact candidate, then obtain the operator's exact-artifact publication approval.

## Measured checks

Task logs below live at `/Users/rj/Desktop/GIT-REPOS/sendmux-sdk/.claude/artifacts/rebrand-qubrics-sdk344/`.

- `pnpm test:release-state`: 41/41 passed, zero skipped (`python-native-source-tests.log`). Existing Python dependency guardrails passed (`python-dependency-guardrails-green.log`). Main's sync produced no `packages/python/` diff. Source commit `9a72fb39` passed the mandatory full `pnpm drift:check` hook (`python-native-source-commit.log`).
- New preparation test first failed with `native gate accepted dependencies excluding the new core major` (`python-dependency-preparation-red.log`); it passes after the fix and checks successful preparation plus idempotence across a major boundary. Existing future-version assertions remain enforced.
- New pyproject drift boundary first failed with `packages/python/mcp/pyproject.toml drift was ignored` (`python-metadata-drift-red.log`), then passed (`python-metadata-drift-green.log`). Existing generated-contract mutation remains covered. No assertion was relaxed or skipped.
- Both independent reviews identified the same new test-fixture defect: a fixed replacement range became a no-op at core 2.0.0. It reproduced in `python-target-drift-fixture-red.log`; changing the fixture's current upper-bound operator guarantees changed bytes at every native version. The focused case then passed (`python-target-drift-fixture-green.log`).

## Non-publishing target-version proof

In the task-owned worktree, temporarily applied only the seven operator-specified target versions to native metadata and the manifest, then ran the existing generators. This is an aggregate local preparation proof, not an immutable Release Please candidate, registry readback or publication approval. Temporary native/manifest changes are restored before the source PR.

| Distribution | Target |
| --- | --- |
| qubrics-core | 2.0.0 |
| qubrics-sending | 2.0.0 |
| qubrics-mailbox | 3.0.0 |
| qubrics-management | 3.0.0 |
| qubrics-sdk | 4.0.0 |
| qubrics-mcp | 3.0.0 |
| langchain-qubrics | 1.0.0 |

- `pnpm generate:python` and then `pnpm generate:mcp` exited 0 (`python-native-target-generation.log`, `python-native-target-contract.log`). All ten internal ranges and three generated versions match the target manifest/native metadata (`python-native-target-metadata.log`).
- MCP contract version is 3.0.0; recorded and independently measured final pyproject SHA256 are both `a8ba5ab92bb7a9418c30b16c3acb7414a743c885fd7ec3a1c39435687be8da3e` (`python-native-target-contract-readback.log`).
- An early native-test run overlapped contract generation and correctly rejected old contract 2.2.0 against native 3.0.0. After contract generation completed, `pnpm test:release-state` passed 41/41 with zero skipped (`python-native-target-tests-after-contract.log`). This was an ordering error in the proof; no code or assertion changed to clear it.
- `AGENT_TASK=rebrand-qubrics-sdk344 heavy-slot.sh pnpm build:python:dists` exited 0 (`python-native-target-dists.log`): 196 native and 10 LangChain source tests passed, zero skipped/xfailed/xpassed; all seven wheel/sdist pairs built; 14 distributions passed Twine checks. Installed MCP artifact check verified qubrics-mcp 3.0.0, child processes exited and its temporary fixture was removed.
- `AGENT_TASK=rebrand-qubrics-sdk344 heavy-slot.sh node scripts/ci-consumers.mjs python` exited 0 (`python-native-target-consumers.log`). All seven wheel and sdist targets installed across six isolated cohorts; six `pip check` results were clean, installed-file provenance matched the candidate archives, and runtime tests completed without permitted skipped/xfailed/xpassed outcomes. The consumer workspace was removed by the existing runner.
- Temporary native/manifest changes were restored to source commit `9a72fb39`. Both `git diff --stat a326bc923fff448470d908bb527afaaa35f6d739 -- python/` and the same command under `-- packages/python/` are empty. No new Python source or metadata candidate is introduced by the final source PR. Local proof distributions and Python codegen cache were deleted; actual publication candidates must be prepared and qualified afresh.

## Remaining gates

No tag, publish or registry action performed. Registry inspection remains held until the boarded sign-in is confirmed. Exact versions/artifacts require a separate operator-only ASK; PyPI/RubyGems versions cannot be reused once published, with yank as the available withdrawal. All twelve legacy pointer versions remain as settled in `pointer-version-decision.md` (SemVer 2.0.0 item 8; A10/A18).

PR368 remains held for sdk343's Windows-origin PR371. Go release PR329 (4.0.0) stays unmerged until #901's origin fix and the #902 cutover readback, then a separate hard publication ASK. #898 is closed; SITE#193, #901 and #902 remain open (read back 2026-11-11). Public install/smoke acceptance remains unmeasured and #344 is not complete.
