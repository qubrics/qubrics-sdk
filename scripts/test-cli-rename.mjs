import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { closeSync, copyFileSync, lstatSync, mkdirSync, mkdtempSync, openSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnCommandSync } from "./windows-command-shims.mjs";

const directory = mkdtempSync(join(tmpdir(), "qubrics-cli-rename-"));
const notice = "sendmux is deprecated. Use qubrics instead.";
const version = JSON.parse(readFileSync("packages/ts/cli/package.json", "utf8")).version;
const env = { ...process.env, HOME: directory, USERPROFILE: directory, XDG_CONFIG_HOME: join(directory, ".config"), QUBRICS_CONFIG_DIR: undefined, SENDMUX_CONFIG_DIR: undefined };

try {
  for (const [binary, launcher] of [["qubrics", "run.js"], ["sendmux", "sendmux.js"]]) {
    const outputPath = join(directory, `${binary}.log`);
    const output = openSync(outputPath, "w");
    let result;
    try {
      result = spawnSync(process.execPath, [`packages/ts/cli/bin/${launcher}`, "--version"], {
        env,
        stdio: ["ignore", output, output],
      });
    } finally {
      closeSync(output);
    }
    const lines = readFileSync(outputPath, "utf8").trim().split(/\r?\n/);
    assert.equal(result.status, 0, `${binary} --version failed: ${lines.join("\n")}`);
    if (binary === "sendmux") assert.equal(lines.shift(), notice, "legacy notice must precede version output");
    assert.equal(lines.length, 1, `${binary} --version must produce one version line`);
    assert.ok(lines[0].startsWith(`@qubrics/cli/${version} `), `${binary} must run the Qubrics CLI`);
  }

  const configDir = join(directory, ".config", "sendmux");
  mkdirSync(configDir, { recursive: true });
  writeFileSync(join(configDir, "config.json"), JSON.stringify({
    defaultProfile: "existing", profiles: { existing: { apiKey: "smx_root_existing", type: "api_key" } },
  }));
  const profiles = spawnSync(process.execPath, ["packages/ts/cli/bin/run.js", "profiles:list", "--json"], { env, encoding: "utf8" });
  assert.equal(profiles.status, 0, profiles.stderr);
  assert.deepEqual(JSON.parse(profiles.stdout).data.profiles, [{ name: "existing", type: "api_key", key_kind: "root", default: true }], "Qubrics must read existing profile storage");
  assert.equal(profiles.stdout.includes("smx_root_existing"), false, "profile listing must keep credentials private");

  const nativeBin = join(directory, "bin");
  mkdirSync(nativeBin);
  mkdirSync(join(directory, "node_modules", "@qubrics", "sdk"), { recursive: true });
  writeFileSync(join(directory, "package.json"), JSON.stringify({ dependencies: { "@qubrics/sdk": "file:/candidate/sdk.tgz" }, overrides: { "@qubrics/core": "file:/candidate/core.tgz" } }));
  writeFileSync(join(directory, "node_modules", "@qubrics", "sdk", "package.json"), JSON.stringify({ version: "3.0.0" }));
  const preparePath = "packages/ts/cli/bin/prepare-tarball.mjs";
  copyFileSync(preparePath, join(nativeBin, "prepare-tarball.mjs"));
  writeFileSync(join(nativeBin, "qubrics.js"), "console.log(JSON.stringify(process.argv.slice(2))); process.exitCode = 7;\n");
  writeFileSync(join(nativeBin, "qubrics"), '#!/usr/bin/env sh\nexec node "$(dirname "$0")/qubrics.js" "$@"\n', { mode: 0o755 });
  writeFileSync(join(nativeBin, "qubrics.cmd"), '@echo off\r\nnode "%~dp0qubrics.js" %*\r\n');
  const prepared = spawnSync(process.execPath, [join(nativeBin, "prepare-tarball.mjs")], { env, encoding: "utf8" });
  assert.equal(prepared.status, 0, prepared.stderr);
  assert.deepEqual(JSON.parse(readFileSync(join(directory, "package.json"), "utf8")), { dependencies: { "@qubrics/sdk": "3.0.0" } }, "native archive metadata must remove local candidate paths");
  assert.equal(lstatSync(join(nativeBin, "sendmux")).isSymbolicLink(), false, "native alias must be portable");
  const native = spawnCommandSync(join(nativeBin, process.platform === "win32" ? "sendmux.cmd" : "sendmux"), ["--version", "argument with spaces"], { env, encoding: "utf8" });
  assert.equal(native.status, 7, "native compatibility launcher must preserve the command exit code");
  assert.equal(native.stderr.trim(), notice);
  assert.deepEqual(JSON.parse(native.stdout), ["--version", "argument with spaces"], "native compatibility launcher must preserve arguments");
} finally {
  rmSync(directory, { recursive: true, force: true });
}

console.log("CLI rename and compatibility binaries passed.");
