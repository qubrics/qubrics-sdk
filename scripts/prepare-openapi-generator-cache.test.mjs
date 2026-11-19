import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, rmSync, existsSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFileSync, spawnSync } from "node:child_process";
import test from "node:test";

const script = new URL("./prepare-openapi-generator-cache.mjs", import.meta.url);

test("cached generator is verified before use, with no download", () => {
  const root = mkdtempSync(join(tmpdir(), "sdk344-generator-cache-"));
  try {
    mkdirSync(join(root, "codegen"));
    mkdirSync(join(root, ".tmp/openapi-generator-cache"), { recursive: true });
    mkdirSync(join(root, "node_modules/@openapitools/openapi-generator-cli"), { recursive: true });
    writeFileSync(join(root, "openapitools.json"), JSON.stringify({ "generator-cli": { version: "7.22.0" } }));
    writeFileSync(join(root, "codegen/openapi-generator.sha1"), "a9993e364706816aba3e25717850c26c9cd0d89d  7.22.0.jar\n");
    writeFileSync(join(root, "node_modules/@openapitools/openapi-generator-cli/package.json"), '{"main":"main.js"}');
    writeFileSync(join(root, "node_modules/@openapitools/openapi-generator-cli/main.js"), "");
    const cached = join(root, ".tmp/openapi-generator-cache/7.22.0.jar");
    const installed = join(root, "node_modules/@openapitools/openapi-generator-cli/versions/7.22.0.jar");
    writeFileSync(cached, "corrupt");
    const rejected = spawnSync(process.execPath, [script.pathname, "install"], { cwd: root, encoding: "utf8" });
    assert.notEqual(rejected.status, 0);
    assert.match(rejected.stderr, /SHA1 mismatch/);
    assert.equal(existsSync(installed), false);
    writeFileSync(cached, "abc");
    const output = execFileSync(process.execPath, [script.pathname, "install"], { cwd: root, encoding: "utf8" });
    assert.match(output, /Verified cached OpenAPI Generator 7.22.0/);
    assert.equal(readFileSync(installed, "utf8"), "abc");
  } finally {
    rmSync(root, { recursive: true });
  }
});
