# Python Sending 2.0.0 release preparation

Issue #344, spec A18. This prepares live release PR357 at `f92ae96ab66195fc60f3d30348f0399491898f28`, based on main `6352f2b835c4e08f9bb4905a828361199fed4c4d`. It grants no ref update, merge, tag or publication authority.

## Cause and canonical preparation

The bot changed the Sending manifest/native version to 2.0.0 while the generated runtime stayed 1.6.0 and SDK/LangChain still required `qubrics-sending>=1.6.0,<2.0.0`. The existing native gate reproduced the incompatible SDK bound at `scripts/python-release-guardrails.mjs:120` in `python-sending-native-before.log`.

SDK local release rules require generation at the actual release head. The existing `pnpm generate:python` invokes the dependency-floor owner, then derives generated client versions from each native pyproject (`scripts/generate-python.mjs:83-109`). Its output changes only the generated Sending `__version__` to 2.0.0 and the SDK/LangChain Sending bounds to `>=2.0.0,<3.0.0`. No generated runtime file was hand-edited. No generator, workflow, fallback or assertion changed.

## Measured independent checks

Logs are under SDK MAIN `.claude/artifacts/rebrand-qubrics-sdk344/`.

- `pnpm test:release-state`: 41/41 passed, zero failed/skipped/cancelled/todo (`python-sending-native-green.log`). This clears the reproduced native-bound failure and covers native/generated version equality.
- `OPENAPI_INPUT_DIR=packages/python/mcp/qubrics/mcp/openapi pnpm canary:openapi`: exit 0, live OpenAPI specs match committed snapshots (`python-sending-canary.log`).
- Official `pnpm build:python:dists` through the existing heavy slot: exit 0, 196 native and 10 LangChain source tests, zero skipped/xfailed/xpassed, all 14 wheel/sdist archives passed Twine, installed MCP contract and cleanup passed (`python-sending-dists.log`). Other built versions are proof fixtures, not proposed publications.
- Official `node scripts/ci-consumers.mjs python` through the existing heavy slot: exit 0. Seven wheel and sdist packages resolved across six clean cohorts, all six `pip check` results passed, installed-file provenance matched the selected archives, and installed runtime tests passed with no permitted skipped/xfailed/xpassed outcomes (`python-sending-consumers.log`). Its temporary workspace was removed by the runner.
- Sending-only `PYTHON_PATHS_RELEASED` selection through `pnpm prepare:publish:pypi`: exit 0, exactly two Sending archives selected (`python-sending-pypi-selection.log`). Exact Sending 2.0.0 PyPI endpoint returned 404 before the packet was prepared.
- Independent Spec review: 0 findings. Independent Standards review: 0 documented violations, 0 judgement smells. Both reviewed the preparation and core-public evidence without rerunning green tests or touching registries.

The root README now records the already-published core pair. Its publication and clean public proof are in [core public acceptance](rebrand-qubrics-sdk344-core-public-20261111.md). README copy passed the fresh-reader critique, one humanize pass and protected-token check. Package names, versions and import contracts were preserved.

## Unchanged default guard is blocked upstream

The latest Skills release selected normally is v2.0.4. Its actual tag is `861d30e87dcebe7e644325010f591dcd3a751b0e`, but the sole downloaded release acceptance asset names `104b9569050f48ab9d1367a16eef82fa71f24488`. The unchanged SDK action at `.github/actions/skill-release-checks/action.yml:65` rejects this exact mismatch: `Approved skills tag differs from the acceptance receipt`. Downloaded asset SHA256 is `968bf30c1f640e751a2e60f09798e190b16464cae118e74ee13d480c899be884`, matching GitHub's asset digest. Raw input and red trace are retained under `skills-default-v2.0.4/` in MAIN artifacts.

Ops routed the confirmed release-input defect to Skills owner. No exact new SDK candidate PASS, PR CI result, ref update, merge or publication is claimed. Requalification requires changed genuine released input, followed by the unchanged default binding and exact candidate guard. No fallback or pin is introduced here.

Source rollback is a normal revert. Publication is operator-only with separately approved exact versions and artifact hashes. PyPI versions cannot be reused, even after withdrawal; yank does not undo installations or caches. No yank is authorised. All other release holds remain in force.
