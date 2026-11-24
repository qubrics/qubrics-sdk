# MCP Registry source preparation

Prepared `io.github.qubrics/qubrics-mcp` for #344. Versions stay npm `1.0.1`, PyPI `3.0.0` and Registry metadata `2.2.0`.

The identity contract test failed before the change. All 27/27 tests then passed with zero skips. Schema validation passed.

The built npm tgz and Python wheel/sdist carry matching ownership markers, and every runtime byte, environment fallback, all 130 tools and five legacy commands match the public packages.

Five legacy commands remain: `sendmux-mcp`, `sendmux-mcp-hosted`, `sendmux-mcp-mailbox`, `sendmux-mcp-management` and `sendmux-mcp-sending`.

Source only. Merge, native publications and Registry publication remain held. Source-only archives must never be uploaded.

Raw proof is in `.claude/artifacts/rebrand-qubrics-sdk344/mcp-registry-qubrics-source-20261122/`.
