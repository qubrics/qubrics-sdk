import assert from "node:assert/strict";
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";
import { verifyRegistryVersion } from "./check-mcp.mjs";

const repository = dirname(dirname(fileURLToPath(import.meta.url)));
const changes = {
  resource: [(registry) => { registry.remotes[0].url = "https://wrong.invalid/mcp"; }, /resource\/transport/],
  transport: [(registry) => { registry.remotes[0].type = "stdio"; }, /resource\/transport/],
  version: [(registry) => { registry.version = "0.0.0"; }, /metadata version/],
  identity: [(registry) => { registry.name = "io.github.Wrong/sendmux-mcp"; }, /Registry identity/],
  "unapproved replacement identity": [(registry) => { registry.name = "io.github.Sendmux/qubrics-mcp"; }, /Registry identity/],
  schema: [(registry) => { registry.$schema = "https://wrong.invalid/schema"; }, /Registry schema/],
  "PyPI package": [(registry) => { registry.packages.find((entry) => entry.registryType === "pypi").identifier = "sendmux-mcp"; }, /Registry package identity/],
  "PyPI version": [(registry) => { registry.packages.find((entry) => entry.registryType === "pypi").version = "9.0.0"; }, /must match pyproject/],
  "npm package": [(registry) => { registry.packages.find((entry) => entry.registryType === "npm").identifier = "wrong-mcp"; }, /npm package identity/],
};

for (const [name, [mutate, expectedError]] of Object.entries(changes)) {
  test(`registry rejects ${name} drift against the package contract`, () => {
    const root = mkdtempSync(join(tmpdir(), "sendmux-registry-contract-"));
    try {
      cpSync(join(repository, "packages/python/mcp"), root, { recursive: true, filter: (path) => !path.includes("__pycache__") });
      assert.doesNotThrow(() => verifyRegistryVersion(root), "unmodified fixture must pass before a specific rejection is tested");
      const path = join(root, "server.json");
      const registry = JSON.parse(readFileSync(path, "utf8"));
      mutate(registry);
      writeFileSync(path, JSON.stringify(registry));
      assert.throws(() => verifyRegistryVersion(root), expectedError);
    } finally {
      rmSync(root, { recursive: true, force: true });
      assert.equal(existsSync(root), false);
      console.log(`registry fixture ${root} absent`);
    }
  });
}

test("registry matches the actual package contract", () => {
  verifyRegistryVersion(join(repository, "packages/python/mcp"));
});

function withRegistry(edit, check) {
  const artifacts = join(repository, ".claude/artifacts/install-surface");
  mkdirSync(artifacts, { recursive: true });
  const root = mkdtempSync(join(artifacts, "registry-"));
  try {
    cpSync(join(repository, "packages/python/mcp"), root, { recursive: true, filter: (path) => !path.includes("__pycache__") });
    const npm = join(root, "npm");
    mkdirSync(npm);
    cpSync(join(repository, "packages/ts/mcp/package.json"), join(npm, "package.json"));
    assert.doesNotThrow(() => verifyRegistryVersion(root, npm), "unmodified fixture must pass before a specific rejection is tested");
    const path = join(root, "server.json");
    const registry = JSON.parse(readFileSync(path, "utf8"));
    edit(registry, root, npm);
    writeFileSync(path, JSON.stringify(registry));
    check(() => verifyRegistryVersion(root, npm));
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}

test("registry metadata versions independently and package order is irrelevant", () => withRegistry((registry) => {
  registry.version = "2.1.4";
  registry.packages.reverse();
}, (check) => assert.doesNotThrow(check)));

test("registry retains its existing server identity for the renamed PyPI distribution", () => withRegistry((registry) => {
  registry.packages.find((entry) => entry.registryType === "pypi").identifier = "qubrics-mcp";
}, (check) => {
  const registry = check();
  assert.equal(registry.name, "io.github.Sendmux/sendmux-mcp");
  assert.equal(registry.packages.find((entry) => entry.registryType === "pypi").identifier, "qubrics-mcp");
}));

test("registry rejects a PyPI ownership marker for an unapproved replacement server", () => withRegistry((registry, root) => {
  registry.packages.find((entry) => entry.registryType === "pypi").identifier = "qubrics-mcp";
  const path = join(root, "README.md");
  writeFileSync(path, readFileSync(path, "utf8").replace("mcp-name: io.github.Sendmux/sendmux-mcp", "mcp-name: io.github.Sendmux/qubrics-mcp"));
}, (check) => assert.throws(check, /PyPI ownership marker/)));

test("registry rejects generated contract identity that differs from native project metadata", () => withRegistry((registry, root) => {
  const path = join(root, "qubrics/mcp/mcp-contract.json");
  const contract = JSON.parse(readFileSync(path, "utf8"));
  contract.package.identity = "sendmux-mcp";
  registry.packages.find((entry) => entry.registryType === "pypi").identifier = "sendmux-mcp";
  writeFileSync(path, JSON.stringify(contract));
}, (check) => assert.throws(check, /contract identity must match native project name/)));

test("registry rejects npm ownership marker drift", () => withRegistry((_registry, _root, npm) => {
  const path = join(npm, "package.json");
  const metadata = JSON.parse(readFileSync(path, "utf8"));
  metadata.mcpName = "io.github.Sendmux/qubrics-mcp";
  writeFileSync(path, JSON.stringify(metadata));
}, (check) => assert.throws(check, /npm ownership marker/)));

test("registry rejects npm version drift even when the PyPI entry is correct", () => withRegistry((registry) => {
  registry.packages.find((entry) => entry.registryType === "npm").version = "9.0.0";
}, (check) => assert.throws(check, /npm.*version/i)));

test("registry rejects duplicate package identities", () => withRegistry((registry) => {
  registry.packages.push(registry.packages[0]);
}, (check) => assert.throws(check, /exactly one/i)));

for (const relative of ["packages/python/mcp/qubrics/mcp/mcp-contract.json", "packages/python/mcp/pyproject.toml"]) {
test(`workspace drift gate rejects changed ${relative}`, () => {
  const root = mkdtempSync(join(tmpdir(), "sendmux-contract-git-"));
  const child = (command, args) => {
    const result = spawnSync(command, args, { cwd: root, encoding: "utf8", timeout: 10_000 });
    assert.throws(() => process.kill(result.pid, 0), { code: "ESRCH" });
    console.log(`drift child ${result.pid} ESRCH`);
    assert.equal(result.error, undefined);
    return result;
  };
  try {
    const path = join(root, relative);
    mkdirSync(dirname(path), { recursive: true });
    cpSync(join(repository, relative), path);
    assert.equal(dirname(root), tmpdir().replace(/\/$/, ""));
    assert.equal(child("git", ["init", "--quiet"]).status, 0);
    assert.equal(child("git", ["add", relative]).status, 0);
    assert.equal(child(process.execPath, [join(repository, "scripts/verify-sdk-staleness.mjs")]).status, 0);
    if (relative.endsWith(".json")) {
      const contract = JSON.parse(readFileSync(path, "utf8"));
      contract.tools.count += 1;
      writeFileSync(path, JSON.stringify(contract));
    } else {
      const source = readFileSync(path, "utf8");
      const updated = source.replace(/qubrics-core>=[^,"]+,<[^"\n]+/, "qubrics-core>=2.0.0,<3.0.0");
      assert.notEqual(updated, source);
      writeFileSync(path, updated);
    }
    assert.notEqual(child(process.execPath, [join(repository, "scripts/verify-sdk-staleness.mjs")]).status, 0, `${relative} drift was ignored`);
  } finally {
    rmSync(root, { recursive: true, force: true });
    assert.equal(existsSync(root), false);
    console.log(`drift fixture ${root} absent`);
  }
});
}
