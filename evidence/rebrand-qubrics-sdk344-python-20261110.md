# SDK #344: Python namespace and publication guard

Goal: Own qubrics/qubrics-sdk#344 through every acceptance box, merged source and published packages.

Status: source work in progress, unmerged and unpublished. No acceptance box is complete. Registry inspection remains on the operator's sign-in hold. Every PyPI/RubyGems publish and old-name pointer release requires the operator's exact-version approval and execution.

## Canonical source and versions

A18 specifies seven new Python distribution names with the shared import package `qubrics`. The source uses native namespace components `qubrics.core`, `qubrics.sending`, `qubrics.mailbox`, `qubrics.management`, `qubrics.sdk`, `qubrics.mcp` and `qubrics.langchain`; no distribution installs a shared `qubrics/__init__.py` or requires a separate distribution named `qubrics`. See [PyPA namespace guidance](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/).

Measured old registry versions and A18's next-major rule give these release targets: `qubrics-core` 2.0.0, `qubrics-sending` 2.0.0, `qubrics-mailbox` 3.0.0, `qubrics-management` 3.0.0, `qubrics-sdk` 4.0.0, `qubrics-mcp` 3.0.0 and `langchain-qubrics` 1.0.0. `registry-audit.json` contains the original registry readback. Source native versions remain unchanged until the matching release PRs; local development artifacts built at those source versions must never be published.

The generator projects Qubrics service hosts without modifying the shared OpenAPI snapshots. Existing A17 environment and header families remain. The default hosted CORS helper recognises both first-party app origins while keeping custom origins exact. Ops settled the final old-name pointer versions: each equals its next-major replacement target, per A10/A18 and SemVer 2.0.0 item 8. Metadata-only pointers are prepared separately in PR369; historical releases retain the old imports. Registry publication remains operator-only.

## Measured source and artifact signals

All logs below live under `/Users/rj/Desktop/GIT-REPOS/sendmux-sdk/.claude/artifacts/rebrand-qubrics-sdk344/`.

| Signal | Observed result | Receipt |
| --- | --- | --- |
| Focused source defaults/runtime | 31 tests passed | `python-core-defaults-namespace.log` |
| Direct generated Configuration defaults | Old SMTP default red, all three canonical defaults green | `python-generated-default-red.log`, `python-generated-default-green.log` |
| Source check | 196 native + 10 LangChain tests, zero skipped; mypy 66/1/4 files | `python-source-final.log` |
| Distribution build | Seven wheel/sdist pairs, twine 14/14, installed MCP contract verified | `python-dists-final.log` |
| Namespace consumer fixture | Red on old distribution lookup, green with dotted imports and slash archive paths | `python-consumer-namespace-red.log`, `python-consumer-namespace-green.log` |
| Transitive candidate dependencies | Red: no matching qubrics-core; green after pip's standard --find-links candidate directory | `python-consumer-dependencies-red.log`, `python-consumer-dependencies-green.log` |
| MCP artifact/server boundary | 26 tests passed, exact existing server identity preserved | `mcp-registry-boundary-restored-green.log` |
| Immutable recovery snapshot output | Five tests passed; paths derive from producer SHA's metadata | `resolve-snapshot-path-green.log` |

The initial installed consumer found 12 failures: eight stale default/brand expectations and four real legacy-origin CORS failures. Tests for explicit legacy host identities and legacy CORS requests remain. The CORS defect was fixed in the shared origin helper; stale expectations were corrected to the spec's canonical defaults. One A2A fixture also had a second explicit resolver origin that needed the same correction. The final official consumer exited 0: all seven wheels and seven sdists installed across six isolated cohorts, six pip checks passed, candidate byte provenance matched, and 299 native plus 10 LangChain tests passed with zero skipped/xfailed. Receipt: `python-artifact-consumers-green.log`. Both child and workspace cleanup were confirmed by the existing runner. No failure was suppressed or skipped.

Mypy initially assigned two module identities to the shared namespace. Explicit package bases plus all seven package roots removed that cause. A missed `os.fsync` import was restored at its source. Contract provenance was regenerated after source changes rather than bypassed. Generated aliases retain behaviour and replacement guidance without obsolete promises of removal in the first renamed major.

Fresh-reader README review caught unqualified unpublished install commands and invented renamed-package version history. All seven package READMEs now qualify installation until publication; source migration guidance describes models rather than fictional Qubrics releases. Root README retains published install commands and lists the pending names, versions and imports separately.

## Confirmed Skills checker blocker

Ops authorised qualification against Skills v2.0.1, released at `3ad9e60baad859cb5e9701bb1f857e1ee485e178` after PR45. Reviewed head: `eca79ee190fa85844655d14b8a5af3c9eb77b606`. Checker blob: `ebb8f8a4b4e2381b32b4a84d506366724c742d8a`. Checker SHA256: `27244e3ef2f23b421c99da8adbd99d10ec8097f8cf6fe42b932caa0e5f9b6b47`. Local Git and GitHub independently matched those identities.

The exact released checker at `scripts/skill-compatibility.mjs:102` derives `qubrics_mcp` by replacing hyphens in the distribution name. This is incompatible with A18's shared native namespace path `qubrics/mcp`. The immutable SDK fixture `23c25dda42154895ae1a88c94954f77665d0fa38` produced:

```
fatal: path 'packages/python/mcp/qubrics_mcp/mcp-contract.json' does not exist in '23c25dda42154895ae1a88c94954f77665d0fa38'
```

The existing guard qualification ran three cases: legacy immutable-source acceptance passed, changed-new-snapshot rejection passed, renamed-source pinned positive acceptance failed. Exit 1, 2 passed, 1 failed, zero skipped. Receipt: `skills-3ad9e60-qualification.log`. Enforced positive regression: `scripts/publication-guard.test.mjs`, test `renamed MCP source accepts the pinned Skills checker without legacy snapshots`.

Required fix belongs at the Skills checker origin: exact immutable `sendmux-mcp` maps to `sendmux_mcp`, exact immutable `qubrics-mcp` maps to `qubrics/mcp`, unknown identity fails closed. Adding an SDK compatibility directory or choosing whichever path exists would conceal the defect and violate the canonical namespace requirement. No such workaround was added, and no checker retry or edit was performed.

The released Skills acceptance asset proves baseline SDK `8d3d749`, not this candidate. A corrected reviewed/released checker and fresh exact-candidate acceptance are still required. Ops ASK was sent with this trace and the requested origin correction. Skills source evidence: `/Users/rj/Desktop/GIT-REPOS/sendmux-skills/.claude/tasks/rebrand-qubrics-skills34/sdk344-checker-evidence.md`.

Two independent staged-source reviews against base `f0e8b721acf62816475f43dd87b18fe025fa0e10` reported zero Python Standards findings and zero additional scoped Spec findings. Receipts: `non-ts-standards-review.md` and `non-ts-spec-review.md`. The shared Ruby guard defect is handled in the Ruby candidate; it does not justify weakening this candidate's failing Skills qualification.

## Go integration and current qualification

Merged Go source `8dbf3bff43f6d7d91fa997726fb59ada60d47720` into this branch without rewriting `a326bc923fff448470d908bb527afaaa35f6d739`. The only conflict was duplicate fixture metadata in `scripts/publication-guard.test.mjs`; the resolved file is byte-identical to the Python parent. Both `git diff --stat a326bc92 -- python/` and the actual package path `git diff --stat a326bc92 -- packages/python/` are empty: Python source and metadata are unchanged.

The integration gate exposed four stale floor-test fixtures in `scripts/prepare-pypi-publish.test.mjs`: they seeded `sendmux-*` dependencies while the renamed guard requires `qubrics-*`. The failure was the missing explicit Qubrics floor, rather than the intended stale-floor rejection. Updated fixture dependency names and the corresponding error-name matcher under A18; versions, floor assertions and successful-boundary checks remain. All 13 preparation tests pass, zero skipped (`python-build-floor-fixtures-green.log`). The initial complete run is `python-go-merged-publication-fixtures.log`: 103 passed, five failed, zero skipped.

The fifth failure came from selecting stale Skills MAIN as the local fixture checker. The corrected control is the exact released v2.0.2 checker extracted from commit `ffc8c41d20eab56184d11476809a9f5f319c8781`, SHA256 `3404789467143317b39d6936c17256e62b458bfde9b03d6348cadd03e9b4a267`. Canonical positive, changed-snapshot negative and immutable legacy positive now pass 3/3 with zero skipped (`python-go-merged-v202-controls-green.log`). The full final `pnpm test:publication-guard` run passes 108/108, zero skipped (`python-go-merged-publication-final.log`). These fixture results do not certify the genuine candidate.

The v2.0.1 MCP-root defect above was corrected in v2.0.2. Genuine acceptance of clean `a326bc92` then failed on stale policy-selected public-source paths, beginning with `packages/python/mailbox/sendmux_mailbox/attachments.py`; the actual source lives under `qubrics/mailbox`. Seven stale Python paths and old console-script selectors were routed to skills34 for an origin correction. Ops reports genuine qualification of `a326bc92` in progress for the next Skills release. Per Ops, a PASS carries to a descendant only while Python package source and metadata remain unchanged; otherwise fresh genuine acceptance is mandatory before that release and the Python publish ASK. No PASS has been received here yet.

## Outstanding release work

Source review, commit, PR, merged-source CI, exact-major release PR verification, account ownership/trusted publishers, operator publications, all public installs/live smokes, old-name pointers and SITE vanity/redirect proof remain open. MCP's existing registry server identity `io.github.Sendmux/sendmux-mcp` and ownership markers remain exact; only its PyPI artifact reference becomes the A18 name `qubrics-mcp`.

No package publish, release PR merge, registry mutation or SDK source merge has run. Worktrees and their necessary build caches remain owned by this task until normal close-off.
