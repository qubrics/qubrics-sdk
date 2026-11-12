# Sending 2.0.0 public acceptance

Issue [#344](https://github.com/qubrics/qubrics-sdk/issues/344), spec A18. Operator performed the upload; Ops relayed completion on 11 November. Agent performed public reads, installation and smoke only. No upload, token mutation, environment approval or yank.

## Source and release identity

PR357 normally merged `2fee94d413783d3b28528f6ec41448d3e8d05664`, with an identical tree to approved `3fe39947b3adb885e97d0bd606b4c9fc12ed875f`. PR CI42980734859 and main CI42983125000 passed 34/34 each, zero skipped jobs. Review sweep was CLEAN with zero reviews, threads or findings; optional CodeRabbit skipped under its existing non-major policy. Release Please42983124898 producer130397949847 passed the normal default Skills v2.0.3 exact-candidate guard and tag verification. Public tag `python-sending-v2.0.0` points exactly to the merge commit.

## Public files and clean installation

At 21:38 AEDT, [PyPI JSON](https://pypi.org/pypi/qubrics-sending/2.0.0/json) and [simple index](https://pypi.org/simple/qubrics-sending/) listed exactly two 2.0.0 files, both unyanked. Independently downloaded public bytes matched operator2A's frozen inventory:

| Filename | SHA256 |
| --- | --- |
| qubrics_sending-2.0.0-py3-none-any.whl | 0bfe8844cd006f9f10f6012b8a69bc2d5334a6056bbff86bce65ed94ae876a0a |
| qubrics_sending-2.0.0.tar.gz | bec81fab5ef6b5c98234233ec4ced2b639a17810707dcee3900bb8dbb5a73cd7 |

A fresh Python3.12.8 venv installed pinned `qubrics-sending==2.0.0` from public PyPI, isolated from local source and without a download cache. Pip's installation report identified the files.pythonhosted.org wheel URL and approved SHA256. Distribution metadata and `qubrics.sending.__version__` both reported 2.0.0. Module and public `qubrics-core==2.0.0` dependency resolved inside this venv's site-packages; the public factory imported. `pip check` passed with no broken requirements.

Installed `qubrics.sending.ApiClient` made a GET only to https://app.qubrics.com/api/v1/openapi.json with TLS verification enabled and retries disabled: HTTP200, OpenAPI3.1.0,89 paths,PASS. No credentials, send or mutation. Proof venv was removed and verified gone after capture.

## Operator deferral and remaining scope

Ops confirmed at 21:41 that operator m10 deferred the release-environment approval for run42983124898/job130400152897. The already-public files make this an expected zero-file/upload-skip operation. Record operator-deferred, never re-ask or block the next package on it. Agent has not approved it or claimed the pending job ran. Mailbox, Management and MCP continue sequentially under existing2A; pointers, gems, Go and MCP Registry remain held.

Raw logs in SDK MAIN `.claude/artifacts/rebrand-qubrics-sdk344/`: `pr357-ci-42980734859.json`, `main-ci-42983125000.json`, `sending-rp-42983124898-producer.log`; `sending-public-20261111/` contains `pypi.json`, `simple.json`, two downloaded archives, `public-download-sha256.log`, `install.log`, `install-report.json`, `pip-check.log`, `import.log`, `smoke.log`. Both public checks passed first time. PyPI token retained per operator11Nov. Published versions cannot be reused; yank requires a named GO and cannot undo installed clients or caches. Three of24 agreed PyPI/RubyGems versions are public.
