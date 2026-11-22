# Go v4 public installation facts

Refs #344. Source-only documentation follow-up to the approved Go release.

The root README still called Go v4 unpublished and installed v3 in its
current-package rows. Its Go badge also pointed to v3. The native README
carried the same unpublished warning. Update those statements to the
proven v4.0.0 module, preserving legacy v3 availability and historical
guidance.

Canonical source: https://go.dev/doc/modules/managing-source and the public
https://github.com/qubrics/qubrics-sdk/releases/tag/go/v4.0.0 . The natural
release targets approved PR329 merge c039925a50d7d36e36bcaa7d67575c74d99aa12a.

Measured 23 November 2026 at 09:58 AEDT: clean official-proxy
`go get qubrics.com/go/v4@v4.0.0` exited 0 with sumdb enabled, empty GOFLAGS,
fresh module/build caches, no local replace or direct fallback. The five
public packages built on Go 1.23.4. The shipped default-origin test passed
all three surfaces. All 108 public archive files equal the tagged Git source,
and 83 production Go files have zero calendar matches. The earlier legacy
import and redirect proof remains valid.

Module sum: h1:BNVt7MidevF7RV9QbcJ2TAOdv5eZjaWwImPcWIU1GYw=.
No module version, runtime, workflow, dependency or announcement changed.
No tag, package or Registry publication is part of this PR. Rollback is a
normal revert of the eventual source merge.

Owner receipt: SDK MAIN .claude/tasks/rebrand-qubrics-sdk344/go-v4-public-20261123.md.
Raw public consumer/default/provenance logs:
.claude/artifacts/rebrand-qubrics-sdk344/go-v4-public-20261123/.

Validation and independent review pending. Pre-existing Rust publication
statements in root README are parked outside this Go-only change.
