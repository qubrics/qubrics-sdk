# SDK producer snapshot sync

PR385's previous verify job failed because docs Sending metadata was ahead
of the live producer. Ops authorised fresh regeneration after docs75 proved
both producer releases live and docs synced, on 19 November 2026 at 18:45 AEDT.

Origin receipt:
`sendmux-docs/.claude/artifacts/rebrand-qubrics-docs75/JOINT-PRODUCER-RUNTIME-PROOF-20261119.md`.
SMTP v1.2.128 source is `b5cf2f1ba707fd72c165b5e4490d0d0c376a7cc0`;
App v1.8.363 source is `141db5f009b976e6807e1c5f3511d47f00e51ff8`.
GitHub docs main measured `0775e2f21428b215165fd25a0bf1894dcf339d46`.

The local inputs were fetched from that measured docs-main commit through
the GitHub API. CI still selects docs main normally: no workflow pin,
fallback, snapshot restoration, assertion change or retry was added.
The existing `pnpm canary:openapi --docs-dir <input>` exited 0 against
the default live URLs: both public documents equal these inputs.

Input SHA256:

- App: `ba45a5411d151e2e74497d859c5967d12f601a5ec25a4e1da66ec2e8a5bfb23c`.
- Sending: `d2c32e1371929ab99e49c5a92a09800373dc07839a0be8926ba91ef6a14b57f4`.

Compared with the previously committed snapshots, App changes three
callback examples. Sending changes eleven display/example/advertised-host
and OAuth URL values. Paths, operation IDs, request/response schemas and
authentication requirements are unchanged. All generated outputs came
from the existing `pnpm drift:check` commands. Its initial final staleness
failure listed the newly generated files pending staging, as intended.
Final diff: seventeen generated files, 58 insertions and 58 deletions.
Temporary PHP formatter differences disappeared in the same generator run;
no PHP source remains changed. Python `python/`, native package metadata,
lockfile, generators and workflows remain unchanged.

Go/Python/Ruby Sending changes are comments. TypeScript's generated default
host now directly advertises `https://smtp.qubrics.com/api/v1`. MCP snapshots
and contract descriptions/examples, plus Rust provenance hashes, bind the
same current inputs. Held MCP/Rust packages remain unpublished. No registry,
release-queue, tag, environment approval or main merge occurs here.

Source rollback is a normal revert. Any later package publication still
needs its exact-file operator approval and public
readback. Previously frozen Sending gem hashes are superseded by regeneration
and must be rebuilt and re-approved.

Receipts under SDK MAIN
`.claude/artifacts/rebrand-qubrics-sdk344/producer-sync-20261119/`:
`docs-current/`, `input-leaf-diff.json`, `install.log`, `live-canary.log`,
`regenerate.log` and `default/`. Full default exact-candidate acceptance and
normal PR CI are subsequent gates; this source commit makes no claim that
those gates have already passed.
