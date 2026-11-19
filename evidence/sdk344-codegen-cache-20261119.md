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
Normal PR CI must additionally prove the actual cached 7.22.0 path is used
for real client generation; that measurement is pending.

This PR is stacked on PR385's separately reviewed deployed-producer sync,
because ordinary CI consumes current docs main. It adds no snapshot pin or
fallback. Parent source/default gates remain distinct; no merge into main
is inferred for the parent. No registry upload, tag, queue or environment
action occurs here. The authorised one-off Python reruns are labelled
**relief**, not the origin fix; no further reruns are authorised.
