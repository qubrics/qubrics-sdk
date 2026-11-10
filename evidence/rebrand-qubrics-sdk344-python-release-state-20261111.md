# SDK #344: Python initial release overrides

Python source PR370 merged normally at `c1abb91ead9e8ccae94ddc446fb759d64e12c946`. Head `b9ea6630` completed 42 successful checks; optional CodeRabbit review and the conditional ownership diagnostic were skipped. Broad and final fixture Spec/Standards reviews found zero findings. Local publication tests passed 108/108, zero skipped; mandatory generator drift hook passed.

Both `git diff --stat a326bc92 c1abb91e -- python/` and the actual `-- packages/python/` are empty. `a326bc92` remains an ancestor. The default full candidate guard first failed on released Skills v2.0.2's old public-source selector. After Skills v2.0.3 was released at `ed0e59a35755980f7f78f81488b324af9878ac00`, Ops authorised one job rerun with that changed input. Main Release Please `42820478809` attempt2 passed its default exact `c1abb91e` guard and completed successfully; every registry-publish job was skipped. No fallback, workflow change, release PR merge or manual publisher was used. Exact native log: SDK MAIN `.claude/artifacts/rebrand-qubrics-sdk344/python-main-release-please-v203-job.log`.

Release Please refreshed all seven intended initial release PRs:

| PR | Package | Initial version |
| --- | --- | --- |
| 356 | qubrics-core | 2.0.0 |
| 357 | qubrics-sending | 2.0.0 |
| 326 | qubrics-mailbox | 3.0.0 |
| 327 | qubrics-management | 3.0.0 |
| 358 | qubrics-sdk | 4.0.0 |
| 328 | qubrics-mcp | 3.0.0 |
| 355 | langchain-qubrics | 1.0.0 |

The SDK's local release rules require removing each one-time `release-as` override immediately after its initial PR exists. This change removes only those seven Python override keys. Package names, native versions, manifest entries, dependency bounds and generated source remain unchanged. The breaking source commit and existing initial release PRs preserve next-major intent; future releases must not be repeatedly forced to the same version.

The existing native release-state suite passed 21/21, zero skipped (`python-initial-release-state-fixtures.log`). No new tests, harness, gate changes or assertion changes were needed for the seven-key removal. The default merged-source guard's actual receipt is bound to `c1abb91e`, Skills `ed0e59a3` and candidateDigest `a84de5803ad9cfcf14e5d1eaeb47b74d732e9bf85eaf09b5e2997829b22bfa68`. Its planned `candidates`, `releases` and `tags` were empty; verified release outputs were `releases_created=false`, `paths_released=[]`.

The packages are unpublished. Registry ownership/sign-in, exact release-PR artifacts and genuine qualification remain required before the operator-only exact-version publish ASK. All PyPI/RubyGems versions are one-way allocations and cannot be reused after publication; yank only. Go PR329 remains unmerged pending #901 merge and #902 cutover readback. Ruby's Windows origin defect belongs to sdk343; it is not fixed by a passing rerun elsewhere. Main CI at c1abb91e remains under observation, including an explicitly traced transient Packagist audit timeout.
