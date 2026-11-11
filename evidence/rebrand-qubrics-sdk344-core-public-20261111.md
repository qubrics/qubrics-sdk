# Python core 2.0.0 public acceptance

Issue: https://github.com/qubrics/qubrics-sdk/issues/344. Spec A18.

Operator confirmed the uploads and environment approval as `m10 done` at 17:25 AEDT. Ops reconciled the sequence and authorised read-only public installation and smoke verification. The agent performed no upload, token mutation, environment approval or yank. Token revocation remains on the operator board.

## Exact public bytes

Release source: approved PR356 head `dc1d9f72e7a38c4f4f2c88c7c8592a0ce75378cd`, normally merged as `6352f2b8` with an identical tree. Main CI `42967562873` succeeded, 34/34. Release Please `42967562886` succeeded; its later PyPI job selected no unpublished files and skipped uploading.

Each of the four files downloaded from PyPI matches the approved frozen inventory:

| Filename | SHA256 |
| --- | --- |
| `qubrics_core-2.0.0-py3-none-any.whl` | `10a04096064e7177f0a654f736de0bca5de78b14eb15ccc37a6fad89d65a01dd` |
| `qubrics_core-2.0.0.tar.gz` | `c7309faf34a32af1c612123c0e15f7bd943a44f214051dd9e3e2bf1f251fec72` |
| `sendmux_core-2.0.0-py3-none-any.whl` | `24cd6b556a06e845622b9ae44f22e608308875c45a546d61e2f2d36afd01d6fe` |
| `sendmux_core-2.0.0.tar.gz` | `6038b6c418df2148e26e07f3d192273dd04cb35142df0617fc5ef4282d3837f7` |

Public records: https://pypi.org/pypi/qubrics-core/2.0.0/json and https://pypi.org/pypi/sendmux-core/2.0.0/json. No extra files or yanks were observed.

## Clean public installations

Two separate Python 3.12 virtual environments installed the pinned versions from public PyPI. The installation reports identify `files.pythonhosted.org` downloads and the matching wheel hashes, without local source or wheel selection.

- `qubrics-core==2.0.0` installed with its runtime dependency. Import resolved to the venv's `site-packages/qubrics/core/__init__.py`. The helper and read-only request smoke returned HTTP 200 from `https://app.qubrics.com/api/v1/openapi.json`, OpenAPI `3.1.0`, 89 paths, result `PASS`.
- `sendmux-core==2.0.0` installed the real `qubrics-core==2.0.0` through `qubrics-core<3.0.0,>=2.0.0`. Installed metadata is Inactive. No legacy import bridge is installed, as decided for the metadata-only final pointer. Import of `qubrics.core` resolved to this second venv, result `PASS`.
- `python -m pip check` exited 0 in both environments: `No broken requirements found.`

## Evidence and limits

Command logs live under SDK MAIN `.claude/artifacts/rebrand-qubrics-sdk344/`: `core-public-four-download-sha256-20261111.log`, `core-public-install.log`, `core-public-install-report.json`, `core-public-smoke.log`, `pointer-public-install.log`, `pointer-public-install-report.json`, and `pointer-public-smoke.log`. The public smoke ran after Ops' resume GO. The two pip dependency checks were read back at 17:44 AEDT.

This proves the first two of 24 agreed PyPI/RubyGems versions. It does not qualify any remaining package or satisfy the held Go cutover checks. Published versions cannot be reused. Yank is the withdrawal mechanism, requires a named operator GO, and cannot undo existing installations.
