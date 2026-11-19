# CI OpenAPI Generator cache origin correction

Ops approved a single CI-only cache prerequisite on 19 November 2026 after
two normal Python jobs failed before client generation. PR387 job135429686136
received HTTP404 and Retry-After85876 from Maven's IAD front; PR385
job135427049615 stopped after download began and produced no generated
directory. The latter HTTP response is unconfirmed. Unchanged Python
source passed PR386 job135429049755. Raw logs and cause analysis are in
MAIN task `live-ci-generator-download-blocker-20261119.md`.

Cause on this side, per Ops: every generation job independently downloads
the same 31,343,317-byte JAR and depends on its runner IP's Maven response.
One preparation job now restores the exact-version cache, downloading once
only on a miss. Generation consumers wait for that job, restore only the
exact key, verify before use and place the JAR in the official npm wrapper's
existing `versions` directory. Consumers never download a cache miss.
The four JAR consumers are verify plus Python, PHP and Ruby language jobs;
Go and MCP generation do not use this Java wrapper. Other runtime jobs
continue independently. No release/publish/tag workflow changes.

Canonical source: official actions/cache centralised-job strategy
`https://github.com/actions/cache/blob/main/caching-strategies.md`.
Official cache v6.1.0 immutable pin:
`55cc8345863c7cc4c66a329aec7e433d2d1c52a9`.
The npm wrapper's documented storage source is
`https://github.com/OpenAPITools/openapi-generator-cli/tree/v2.32.0`.

The expected SHA1 is read directly from Maven's published
`https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.22.0/openapi-generator-cli-7.22.0.jar.sha1`:
`aa154752b82c9b84151cd4998ce2a86ed21f5bd3`. Its checked-in checksum is bound
to the version in `openapitools.json`. Every restored JAR is checked against
that independent published digest before install or Java use; mismatch or
missing cache fails loud. Both version and checksum identify the cache key;
there is no prefix fallback. A version change requires the matching vendor
checksum, never a silently accepted new JAR. This SHA1 check implements the
operator's requested Maven integrity comparison; no stronger signature
claim is made. Source rollback is normal revert.

Focused behavioural test drives the public preparation command against a
task-owned fixture: corrupted cached bytes must fail before install; known
SHA1 test bytes then install from cache without a network operation. Initial
red (command missing) and green (1/1, zero skips) are in MAIN artifacts
`codegen-cache-20261119/{red.log,green.log}`. No existing assertion weakened.
Normal PR388 CI `44488711514` at exact
`3c5e91108a1b0c276aecca5ca6b45b440fd301b2` completed SUCCESS: 35 of 35
jobs successful, no failed or skipped jobs; blocking watcher exited 0.
Seed job `135438588357` recorded a cold miss, one download, published SHA1
verification and a successful exact-key save. All four real consumers then
restored that key, verified the same SHA1 and installed the JAR into the
official wrapper's `versions/7.22.0.jar` path with `no Maven request`:

| Consumer | Successful job |
| --- | --- |
| Full verify | `135438652831` |
| Python generation | `135438652961` |
| PHP generation | `135438652902` |
| Ruby generation | `135438652887` |

The immutable run is
`https://github.com/qubrics/qubrics-sdk/actions/runs/44488711514`.
Raw seed/consumer logs and final run receipt live under MAIN artifacts
`codegen-cache-20261119/`; `pr388-python-direct.log:734,744–745` and
`ruby-cache-job.log:757,767–768` identify the restored key, checked digest
and installed path. No failed generation check was weakened or suppressed.

This PR is stacked on PR385's separately reviewed deployed-producer sync,
because ordinary CI consumes current docs main. It adds no snapshot pin or
fallback. PR388 normally merged into that parent as `b25a7cbc`; PR385 then
passed fresh normal CI `44490987561` with 35 of 35 jobs, 42 successful checks
plus completed optional CodeRabbit SKIPPED, and an empty review sweep.
Default Skills v2.0.6 verified its actual release receipt and accepted all
22 results on exact `b25a7cbc`, including live OpenAPI equality. Ops
explicitly approved its normal main merge, completed as
`1a83316982382e5ad77fc4303315f7b049ef0126` on 19 November at 09:03:40Z.
Main CI `44492953710` is watched; its result remains pending at this update.
Rollback is a normal revert of cache commit `3c5e9110` through a PR.

The two authorised Python reruns are **relief**, not the origin fix:
PR385 run `44485270880` attempt 2 and PR387 run `44486055882` attempt 2
completed successfully on unchanged heads. No further reruns authorised.
No registry upload, tag, queue or environment action occurred. Local proof
JAR copies were removed and their absence verified; the shared remote cache
is retained as the approved CI mechanism.
