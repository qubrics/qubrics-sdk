# Python MCP pointer command compatibility

Operator 5B holds `sendmux-mcp 3.0.0` publication until the final pointer
preserves the five console commands from public 2.2.0. Source correction
only; no upload, tag, queue, workflow or environment approval.

## Confirmed cause and native red

Fresh Python 3.12 venv installed `sendmux-mcp==2.2.0` from PyPI without
cache. Its actual installed console-script metadata names `sendmux-mcp`,
`sendmux-mcp-hosted`, `sendmux-mcp-mailbox`, `sendmux-mcp-management` and
`sendmux-mcp-sending`, pointing to the corresponding `sendmux_mcp` functions.
Upgrading that venv to the previously prepared local 3.0.0 wheel removed
all five executable files. The pointer's native pyproject had no
`[project.scripts]` table, so its wheel had no console entry points.
The replacement installs only the differently named `qubrics-mcp*` scripts.

The native installed-metadata/executable check exited 1:
`AssertionError: Upgrade removed all five legacy console commands`.
Both missing entry-point and absent executable lists contain exactly those
five commands. Prior qualification covered dependency and import
behaviour but omitted the old executable interface; that was the escape.

## Minimal origin correction

Add five console-script declarations to
`release-pointers/pypi/sendmux-mcp/pyproject.toml`. No wrapper or copied
runtime is needed. Existing canonical declarations in
`packages/python/mcp/pyproject.toml:32-37` name the same implementation
functions: `qubrics.mcp.cli:main`, `qubrics.mcp.hosted:run_hosted`, and
`qubrics.mcp.cli:main_mailbox`, `main_management`, `main_sending`.
Definitions are `qubrics/mcp/cli.py:20-45` and `hosted.py:154` within that
package. The native build and actual installed entry-point loading both
verify these module paths; none was inferred from a name.

The dependency-only payload, version, dependency range, Inactive
classification and neutral public text remain unchanged. There is no
move announcement, legacy Python import bridge or additional runtime code.

## Actual upgrade and command startup green

Native `python -m build` builds an sdist and then a wheel from that sdist;
Twine accepts both. A second fresh venv installs public 2.2.0, then
upgrades to the fixed local wheel with `pip --isolated --no-cache-dir`
and explicit public index. Installed pointer metadata reports 3.0.0 and
the public replacement reports `qubrics-mcp 3.0.0`; all five entry points
load actual callable functions from the installed public replacement.

Each old executable was then invoked without command-line flags, with
only legacy `SENDMUX_*` settings selecting local HTTP transport, port 0,
loopback host, fixture credentials and a fixture local bearer token.
All five printed `Application startup complete` and a listening
`http://127.0.0.1:<ephemeral port>` URL. Each owned child received SIGTERM,
printed `Finished server process`, and was reaped. These are actual
executables and servers, not a mocked CLI. No upstream tool/API call,
production request or telemetry credential was supplied.

`pip check` exits 0: `No broken requirements found.` Existing
`pnpm test:python-release-guardrails` exits 0. The seven-line metadata
change needs no new test harness; the requested native upgrade/startup
proof exercises the installed public interface directly.

## Environment compatibility

No additional source correction was needed. `config.py:26-30` already
reads a non-empty `QUBRICS_*` value first, then the original `SENDMUX_*`
name. CLI surface selection uses that helper (`cli.py:85`), as do local
configuration (`config.py:116-154`) and hosted configuration
(`hosted.py:75-102`). The installed public package was tested directly:
legacy keys/surfaces/host/port/transport/app URL/timeout/bearer/resource URL,
empty-new-name fallback, canonical-name precedence and explicit-key
precedence all pass. The five real server starts also prove old
host/port/transport/key variables reach the existing commands.

Other prepared PyPI and npm pointers were audited independently against
actual prior public archives; the parent release packet carries their
specific version, hash, console/bin and environment evidence. No source
change for a sibling is claimed by this PR.

Raw receipts under MAIN:
`.claude/artifacts/rebrand-qubrics-sdk344/pypi-mcp-pointer-compat-20261120/`
contain old-entrypoints.json, upgrade-before-red.log, public install and
upgrade logs, build-local.log, archive-inspection.json,
legacy-command-starts.log, installed-env-fallback.log, pip-check.log and
release-guardrails.log. No public source/package files are substituted
for registry-installed dependencies. Source rollback: normal PR revert.
Publication remains held for new exact-file approval; no version was
uploaded here.
