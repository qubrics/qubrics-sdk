# Four Python replacement artifact previews

Issue #344, spec A18. Ops requested an exact GO packet for four replacement versions after independent Sending proof. Core alone has publication approval (decisions:415). No bot ref, merge, tag, upload, environment approval, publisher or token mutation occurred here. PyPI All-projects token retained per operator 11 Nov for future publishing.

These are local artifact previews from authentic separate release heads, prepared serially with existing generators. They are not a combined release candidate or permission to publish. PR357 remains held on the Skills owner's default-release binding correction. Every actual release still requires refreshed exact source, normal default candidate acceptance, green CI/review, separately approved normal merge and green main/producer/tag evidence. Source or approved-byte changes require a fresh ASK.

## Prepared sources

| Package | Live bot source | Local preparation |
| --- | --- | --- |
| qubrics-sending 2.0.0 | f92ae96ab66195fc60f3d30348f0399491898f28 | 9510177d1cf309262bfa856975e64624c5aecf35 |
| qubrics-mailbox 3.0.0 | a1cfeec0f788034042f34db2846fef2139322d2b | d2cf4bda686b61aeeccde51f6f33d363f7919e94 |
| qubrics-management 3.0.0 | fe2c7963ddc16423decb9b3165d26c5d686f836d | 79c6bff5f4f322113fd4b7f9f08a596d10124556 |
| qubrics-mcp 3.0.0 | 8b956cc15cfb3919bb4d04fac3b16a96cd4f1d7c | 467e86e95ce78d27341f3d0c496398946e4729f1 |

Sending's full independent checks and core public proof are recorded in the adjacent evidence files. Its token-decision-only successor `0e5fbb00` has no `python/` or `packages/python/` differences from the archive source. Against accepted baseline `a326bc92`, Sending's `python/` diff is empty, but `packages/python/` has 11 files, +53/-11. Fresh exact acceptance is required; no baseline PASS is carried.

Mailbox's generator changed only generated `__version__` to3.0.0 and SDK/LangChain Mailbox bounds to `>=3.0.0,<4.0.0`. Management's generator changed only generated `__version__` to3.0.0 and SDK's corresponding bound. MCP's existing generator changed its contract package version and full-pyproject provenance hash for native3.0.0. No generated file was hand-edited, no assertion changed, and no workflow/fallback/pin was added.

For each of those three previews: native release gate41/41, zero skipped/failed/cancelled/todo; both wheel/sdist builds and Twine checks passed; mandatory commit drift passed. Each proposed wheel installed with real public core2.0.0 in its own clean venv, imported from its installed namespace at the correct version and passed `pip check`. Independent batched Spec review0 and Standards review0.

MCP's installed source-generation `python -m qubrics.mcp.contract --check` failed because that source-only command reads checkout `pyproject.toml` at `contract.py:180`, absent from a wheel. No code was changed to silence it. The documented existing artifact check at `scripts/check-mcp-artifacts.py:98` uses shipped `load_contract()`: the official check passed both archives, loaded the installed3.0.0 contract, verified source/native metadata, exited both child processes and removed its fixture. The fully dependency-resolved wheel's `load_contract()` also returned PASS. The original wrong-command trace remains in `python-mcp-packet-contract.log`.

## Frozen bytes

SDK MAIN `.claude/artifacts/rebrand-qubrics-sdk344/surface-publish-packet-20261111/pypi/` holds exactly these eight files and `SHA256SUMS`. Verification returned eight `OK` results. These bytes, rather than a later unmeasured runner rebuild, are the requested approval subject.

| Filename | SHA256 |
| --- | --- |
| qubrics_sending-2.0.0-py3-none-any.whl | 0bfe8844cd006f9f10f6012b8a69bc2d5334a6056bbff86bce65ed94ae876a0a |
| qubrics_sending-2.0.0.tar.gz | bec81fab5ef6b5c98234233ec4ced2b639a17810707dcee3900bb8dbb5a73cd7 |
| qubrics_mailbox-3.0.0-py3-none-any.whl | c911ba6315702ff6c3a050a5c1a188dff38a2f1c1d2be3020a8eb9113137b23d |
| qubrics_mailbox-3.0.0.tar.gz | d69e1086a84c4e50117f18d003a0b2466d9c0975268f6883e80061f0e6bfc7f1 |
| qubrics_management-3.0.0-py3-none-any.whl | 58865525e424782a716e1e0d6797c1580a6ace1566f2e2ca60d45a854d03b046 |
| qubrics_management-3.0.0.tar.gz | ddf4248a8f23d5b0e1c3639cf10e2ccdced01bdafcc32e407d9bfad1f1240bc4 |
| qubrics_mcp-3.0.0-py3-none-any.whl | b0d9ffcef58a43dcb932c9187b7f570d327f30544847304184adbad2b29d6464 |
| qubrics_mcp-3.0.0.tar.gz | ff1aef5b69205086239f9ff5d3caf29bacdd0e111cccfb24805ffaf06a122087 |

Public project/version lookups for all four returned404. This does not prove registry name ownership. Execution request order is Sending, Mailbox, Management, MCP, one package at a time, with independent download/hash readback and clean public acceptance before the next. All old-name pointers remain a separate ASK. MCP Registry identity/top-level version remain independent; its protected metadata-publishing job stays held.

Bulk logs in MAIN artifacts use prefixes `python-{sending,mailbox,management,mcp}-packet-*` and `python-sending-*`; the exact private operator packet is MAIN `.claude/tasks/rebrand-qubrics-sdk344/publish-ask-four-surfaces-20261111.md`. Default binding input/red trace is under `skills-default-v2.0.4/`.

There is no full registry rollback. Published versions cannot be reused. Yank does not undo installed consumers/caches and requires a named operator GO. Source rollback is a normal revert. No new version is invented. #344 remains open: only the two core versions are public and measured, all remaining publication/cutover clauses remain held.
