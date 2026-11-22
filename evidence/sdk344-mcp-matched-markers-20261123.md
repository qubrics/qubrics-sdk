# Matched-marker MCP release preparation

Refs #344 and qubrics/qubrics#1041. Operator B selected the new Registry
identity io.github.qubrics/qubrics-mcp; PR418 propagated it to source.
This preparation assigns the requested native patch versions:
sendmux-mcp 1.0.2, qubrics-mcp 3.0.1 and Registry metadata 3.0.1.

The two native package versions match their release-state entries and
descriptor references. The Python contract was regenerated through its
existing generator. It still contains 130 tools with identical names, descriptions,
schemas, annotations, origins, transports and limits. Only its package
version and pyproject build-input hash changed. No runtime, dependencies,
legacy commands or environment fallbacks changed. The package README now
uses the published install command without the stale unpublished warning.
No move announcement or post-install message was added.

Focused MCP/Registry/bridge tests passed 31/31 with zero skipped. Native
release-state validation passed. The frozen-lockfile install also passed
(raw receipt: install.log in the artifact directory below). Packed
artifact, calendar, consumer, exact-head/default and CI/review qualification
remain pending; no publication-ready or public claim is made here.

Canonical ownership rules:
https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/package-types.mdx#ownership-verification
Existing source validators require the same server name in npm mcpName,
Python README mcp-name and the committed descriptor. A published version
cannot be replaced; these new versions keep prior public files untouched.

The candidates remain unpublished. No producer tag, upload, dispatch,
Registry mutation or release-workflow change is part of this preparation.
Source rollback is a normal revert.

Owner state/receipts: SDK MAIN .claude/tasks/rebrand-qubrics-sdk344/
matched-marker-mcp-prep-20261123.md and
.claude/artifacts/rebrand-qubrics-sdk344/matched-marker-mcp-20261123/.
