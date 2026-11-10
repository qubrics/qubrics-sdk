# SDK #344: Ruby source candidate

Status: source candidate, unmerged and unpublished. No #344 acceptance box is complete.

A18 specifies the five `qubrics-*` gems and the `Qubrics` module. Target next majors, derived from the measured published old versions, are core 2.0.0, sending 2.0.0, mailbox 3.0.0, management 3.0.0 and SDK 3.0.0. Local native versions remain unchanged until exact-major release PRs. Local development gems must never be published at these retained source versions.

The generator owns canonical module names, entry points and defaults. It projects Qubrics servers and title/description without changing shared OpenAPI snapshots. A17 environment/header families, credential prefixes, nil-safe schema extensions and legacy positional upload-token mapping remain.

Receipts under `/Users/rj/Desktop/GIT-REPOS/sendmux-sdk/.claude/artifacts/rebrand-qubrics-sdk344/`:

| Signal | Result | Receipt |
| --- | --- | --- |
| Ruby source check | 35 handwritten files lint clean; 56 runs, 331 assertions, no failures/errors/skips; five gems built | `ruby-check.log` |
| Final public request default regression | Old app host red; all three canonical defaults green | `ruby-defaults-red.log`, `ruby-defaults-green.log` |
| Preserved legacy upload header | Original expectation restored; 6 runs, 24 assertions, no skips | `ruby-delegated-red.log`, `ruby-delegated-green.log` |
| Final native gem build | Exit 0 after README corrections | `ruby-build-final.log` |
| Native release metadata | Exit 0 | `ruby-release-state.log` |
| Deprecated model import | Existing Ruby model compatibility test exit 0 | `ruby-model-compat.log` |

The default regression moved to the existing environment test class after the added assertion exceeded the core test class's existing length gate. The threshold was unchanged. An overbroad test rename had changed the legacy upload-header expectation; tracing the retained generator mapping established the correct original assertion. Runtime compatibility was preserved.

Fresh-reader review and one humanize pass corrected unpublished installation claims and fictional renamed-package version history in all five package READMEs. Protected names, require paths, modules, URLs and compatibility literals were checked against source. Root README lists pending release names separately from published install commands.

Two independent staged-source reviews against base `f0e8b721acf62816475f43dd87b18fe025fa0e10` reported zero additional scoped Spec findings and one Standards finding: the publication guard still reconstructed `lib/sendmux` native paths. The guard now reads the version-file declared by each release's immutable configuration. The new Qubrics case failed before the fix; Qubrics and historical Sendmux cases now pass, ignore newer working-tree configuration and still reject a wrong native version. Full existing guard file: 69 passed, zero skipped (`ruby-publication-guard-full.log`). Focused cases against the identical reviewed/released Skills v2.0.1 checker also passed 2/2 with zero skipped (`ruby-publication-guard-v201.log`). Receipts and exact diff: `ruby-publication-guard-receipt.md`. No availability fallback or duplicate legacy source tree was added.

Both synthetic publication fixture builders now seed the immutable legacy MCP project.name required by released Skills v2.0.1; releaseFixture retains that name when adding its version. This matches the PR367 fixture-origin correction, without changing any existing assertion. Commits/PRs, full CI and final combined branch integration remain.

The existing installed-gem consumer exited 0 under Ruby 3.4.1: all five local candidates installed in isolated GEM_HOME, all 20 loaded files belonged to that home, and the existing runtime tests passed 31 runs and 209 assertions with zero failures/errors/skips. Receipt: `ruby-consumer.log`. The runner confirmed workspace removal; its parent TMPDIR was also removed and absence verified. Native dependency ranges, version files, manifest and Gemfile.lock must advance together in exact-major release PRs.

All old-name pointer gems remain outstanding. Their versions require an operator decision; each must depend on its replacement, print the specified post-install message and preserve useful legacy requires/constants. Every RubyGems/PyPI/pointer publish requires exact-version operator approval and operator execution. Registry inspection remains on hold until sign-in is confirmed.

No package publish, release PR merge, registry mutation or source merge has run. Necessary caches remain in the owned worktree for normal `git worktree remove` at close-off. The detailed operator-local source receipt is `ruby-source-receipts.md`.

PR368 head `c6a27a61` completed 41 successful checks; the sole optional CodeRabbit check skipped for quota and supplied no code analysis. Go PR367 then merged at `8dbf3bff`, producing one adjacent-line conflict in `scripts/release-state-fixtures.test.mjs`: each branch renamed its own language's mutation fixture. The merge retains both canonical identities (`lib/qubrics` Ruby and `qubrics.com/go` Go); all rejection assertions remain unchanged. The existing merged native release fixtures passed 21/21 with zero skipped (`ruby-go-merged-release-fixtures.log`). No branch was rebased or force-pushed.
