import { readFileSync, rmSync, writeFileSync } from "node:fs";

const manifestPath = new URL("../package.json", import.meta.url);
const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
manifest.dependencies["@qubrics/sdk"] = JSON.parse(readFileSync(new URL("../node_modules/@qubrics/sdk/package.json", import.meta.url), "utf8")).version;
delete manifest.overrides;
writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);

// Replace oclif's symlink alias so portable archives also show the deprecation.
const legacy = new URL("./sendmux", import.meta.url);
rmSync(legacy, { force: true });
writeFileSync(legacy, '#!/usr/bin/env sh\necho "sendmux is deprecated. Use qubrics instead." >&2\nexec "$(dirname "$0")/qubrics" "$@"\n', { mode: 0o755 });
writeFileSync(new URL("./sendmux.cmd", import.meta.url), '@echo off\r\necho sendmux is deprecated. Use qubrics instead. 1>&2\r\ncall "%~dp0qubrics.cmd" %*\r\nexit /b %errorlevel%\r\n');
